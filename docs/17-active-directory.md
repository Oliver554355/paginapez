# Ataques a Active Directory

Active Directory (AD) es el sistema de gestión de identidades más usado en
redes corporativas Windows: centraliza usuarios, grupos, permisos y
políticas en un **Controlador de Dominio (DC)**. Es también, por eso mismo,
el objetivo favorito en máquinas "hard"/"insane" de HTB y en pentests
reales — comprometer AD suele significar comprometer toda la red.

Requiere haber leído [`docs/07-command-and-control.md`](07-command-and-control.md)
(persistencia/movimiento lateral) y
[`docs/12-herramientas-y-tecnicas.md`](12-herramientas-y-tecnicas.md)
(BloodHound, Mimikatz, CrackMapExec) como base.

## Conceptos previos rápidos

- **Kerberos** es el protocolo de autenticación de AD: en vez de mandar la
  contraseña, un usuario obtiene un **TGT** (Ticket Granting Ticket) del DC,
  y con ese TGT pide **TGS** (Ticket Granting Service tickets) para acceder
  a servicios específicos, cada uno cifrado con el hash de la cuenta del
  servicio.
- Cada usuario/equipo tiene un hash NTLM derivado de su contraseña,
  almacenado en el DC.
- **LLMNR/NBT-NS**: protocolos de resolución de nombres de respaldo, activos
  por defecto, que responden aunque no sean la fuente autoritativa — la
  raíz de uno de los ataques más comunes contra AD (ver más abajo).

## 1. Enumeración inicial

Antes de atacar nada, mapear la estructura:

```bash
# Enumeración anónima/con credenciales básicas
crackmapexec smb <IP> -u '' -p ''
ldapsearch -x -H ldap://<DC-IP> -b "dc=empresa,dc=htb"

# BloodHound: recolecta relaciones de permisos y las grafica
bloodhound-python -u usuario -p contraseña -d empresa.htb -c all -ns <DC-IP>
```

BloodHound es la herramienta clave aquí: convierte una maraña de permisos
en un grafo donde se ve visualmente "este usuario de bajo nivel tiene, sin
saberlo, un camino de 3 saltos hasta Domain Admin" — encontrar esos caminos
cortos es el objetivo de toda esta fase.

## 2. LLMNR/NBT-NS Poisoning + Relay (con Responder)

**Cómo funciona**: cuando un equipo Windows falla al resolver un nombre por
DNS normal, cae de vuelta a LLMNR/NBT-NS (broadcast en la red local),
preguntando "¿alguien es `\\servidor-typo\`?". La herramienta `Responder`
escucha esas consultas y **responde afirmativamente a todo**, haciéndose
pasar por el recurso que sea. El equipo víctima entonces envía su hash NTLM
(en un desafío-respuesta) directamente al atacante.

**Variante más peligrosa: NTLM Relay.** En vez de solo capturar el hash
para crackearlo offline, la herramienta (`ntlmrelayx`) lo **reenvía en vivo**
a otro servicio de la red (ej. otro servidor por SMB) mientras la
autenticación sigue en curso, autenticándose como la víctima sin necesitar
conocer ni crackear la contraseña.

### Defensa
- **Deshabilitar LLMNR y NBT-NS** por GPO en toda la red (rara vez se
  necesitan si el DNS interno está bien configurado).
- **SMB Signing obligatorio** en todos los equipos — impide el relay porque
  cada mensaje SMB debe estar firmado con la clave real de la sesión.

## 3. Kerberoasting

**Cómo funciona**: cualquier usuario autenticado del dominio puede pedir un
TGS para **cualquier** cuenta de servicio (Service Principal Name, SPN)
registrada — es una función normal de Kerberos. Ese TGS viene cifrado con
el hash NTLM de la cuenta de servicio. El atacante solicita TGS para todas
las cuentas de servicio que encuentre, y los crackea **offline** (como en
`docs/04-password-attacks.md`) buscando la contraseña de esas cuentas.

```bash
GetUserSPNs.py empresa.htb/usuario:contraseña -dc-ip <IP> -request
hashcat -m 13100 tgs_hashes.txt rockyou.txt
```

Es efectivo porque las cuentas de servicio suelen tener contraseñas
antiguas, nunca rotadas, y a menudo con privilegios altos.

### Defensa
- Contraseñas largas y aleatorias (25+ caracteres) para cuentas de
  servicio — vuelve el crackeo offline inviable.
- **gMSA (group Managed Service Accounts)**: cuentas de servicio con
  contraseña gestionada y rotada automáticamente por AD, sin que ningún
  humano la conozca ni pueda hacerla débil.

## 4. AS-REP Roasting

**Cómo funciona**: variante relacionada — si una cuenta tiene desactivada
la **preautenticación Kerberos** (una opción de configuración, poco común
pero existe), cualquiera puede solicitar datos de autenticación para esa
cuenta sin conocer su contraseña, y esos datos vienen cifrados con el hash
de la cuenta — crackeable offline igual que un Kerberoast.

### Defensa
- Preautenticación Kerberos activada (es el valor por defecto; auditar
  periódicamente que nadie la haya desactivado por error).

## 5. Pass-the-Hash / Pass-the-Ticket

**Pass-the-Hash**: en muchos servicios Windows (SMB, WMI), **no hace falta
la contraseña en texto plano** — el hash NTLM por sí solo es suficiente
para autenticarse. Si el atacante obtuvo el hash (con Mimikatz de un equipo
comprometido, o con Responder), puede autenticarse en otros equipos que
compartan esa cuenta/contraseña sin nunca crackearlo.

**Pass-the-Ticket**: lo mismo pero con un TGT/TGS de Kerberos robado de la
memoria de un proceso — se "inyecta" en la sesión propia y se usa como si
fuera el usuario legítimo, sin tocar contraseñas ni hashes en absoluto.

### Defensa
- No reutilizar la misma contraseña de administrador local en todos los
  equipos (usar **LAPS** — Local Administrator Password Solution — que
  genera y rota una contraseña única por máquina).
- Principio de menor privilegio: que las cuentas de administrador de
  dominio nunca inicien sesión en estaciones de trabajo normales, solo en
  servidores que realmente lo requieran (modelo de "tiers" administrativos).

## 6. Golden Ticket / Silver Ticket / DCSync

Técnicas de post-explotación avanzada, tras ya haber comprometido cuentas
con privilegios altos:

- **Golden Ticket**: con el hash de la cuenta `krbtgt` (la que firma TODOS
  los tickets Kerberos del dominio), el atacante puede forjar TGTs válidos
  para cualquier usuario, con cualquier permiso, válidos durante años —
  acceso total y persistente al dominio.
- **Silver Ticket**: igual pero para un servicio específico (con el hash de
  la cuenta de ese servicio, no de `krbtgt`), más sigiloso porque no pasa
  por el DC en cada uso.
- **DCSync**: abusa de permisos de replicación de AD para pedirle al DC
  "sincronízame" los hashes de cualquier cuenta, incluida `krbtgt`, sin
  necesitar acceso directo al disco del controlador de dominio.

### Defensa
- Este nivel de compromiso significa que el dominio entero debe
  considerarse comprometido — la única remediación real es **rotar el hash
  de `krbtgt` (dos veces)** y una reconstrucción cuidadosa, no un simple
  cambio de contraseña.
- Prevención: restringir estrictamente qué cuentas tienen permisos de
  replicación (`Replicating Directory Changes`), y monitorizar solicitudes
  DCSync desde cuentas que no sean controladores de dominio — es una señal
  de compromiso de altísima confianza.

## 7. Abuso de delegación (delegation abuse)

**Cómo funciona**: la delegación Kerberos permite que un servicio actúe
"en nombre de" un usuario ante otro servicio (ej. un servidor web que
consulta una base de datos como el usuario que inició sesión). Mal
configurada (delegación no restringida, o delegación restringida con
permisos excesivos), un atacante que compromete ese servicio intermedio
puede hacerse pasar ante otros servicios como **cualquier usuario que se
haya autenticado alguna vez** en el servicio comprometido — incluyendo
administradores de dominio.

### Defensa
- Evitar delegación no restringida por completo — usar delegación
  restringida (o "basada en recursos") y solo donde sea estrictamente
  necesario.
- Marcar las cuentas administrativas como "sensibles, no se pueden delegar"
  (`Account is sensitive and cannot be delegated`).

## Checklist defensivo general para AD

- [ ] LLMNR/NBT-NS deshabilitados, SMB signing obligatorio.
- [ ] LAPS desplegado (contraseñas de admin local únicas por equipo).
- [ ] Modelo de tiers: cuentas de administrador de dominio nunca inician
      sesión en estaciones de trabajo normales.
- [ ] Contraseñas largas/aleatorias o gMSA para cuentas de servicio.
- [ ] Preautenticación Kerberos activada en todas las cuentas.
- [ ] Delegación no restringida eliminada; auditoría periódica de
      configuraciones de delegación.
- [ ] Monitorización de solicitudes DCSync fuera de los DCs, y de patrones
      de Kerberoasting (muchas solicitudes TGS en poco tiempo desde una
      cuenta).
- [ ] `krbtgt` con rotación periódica de contraseña (no solo tras un
      incidente).

## Practicar (legal)

Las máquinas "hard"/"insane" de HTB con Active Directory, y salas
dedicadas en TryHackMe ("Attacktive Directory", "Reset AD"), son el lugar
para aplicar todo esto — ver
[`docs/13-metodologia-htb.md`](13-metodologia-htb.md) para el flujo
general, y nunca contra un dominio real sin autorización explícita
(`docs/08-defensas-generales.md`).
