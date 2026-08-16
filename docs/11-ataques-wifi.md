# Ataques a redes WiFi

## Por qué WiFi es un objetivo distinto a una red cableada

En una red cableada, un atacante necesita acceso físico al cable o al switch.
En WiFi, la señal viaja por el aire y sale del edificio — cualquiera dentro
del alcance de la señal puede **capturar el tráfico** sin necesitar conectar
nada físicamente, aunque no pueda leerlo sin romper el cifrado.

## 1. Captura del handshake y crackeo offline (WPA2-Personal)

**Cómo funciona**: cuando un dispositivo se conecta a una red WiFi protegida
con WPA2-PSK, ocurre un intercambio de 4 mensajes (el "4-way handshake") que
deriva la clave de sesión a partir de la contraseña de la red (PSK) y unos
valores aleatorios. Un atacante:

1. Pone su tarjeta WiFi en **modo monitor** para capturar todo el tráfico del
   canal, no solo el dirigido a él.
2. Captura ese handshake cuando un dispositivo legítimo se conecta (o fuerza
   una reconexión, ver sección de deautenticación abajo).
3. Con el handshake capturado, el ataque ya **no necesita seguir cerca de la
   red** — lo hace offline, probando contraseñas candidatas (diccionario o
   fuerza bruta) contra el handshake capturado, herramientas como
   `aircrack-ng` o `hashcat`.
4. Si la contraseña de la red está en el diccionario o es débil, la
   recupera.

**Por qué funciona**: la seguridad de WPA2-Personal depende **enteramente**
de la fortaleza de la contraseña — el protocolo en sí es sólido, pero si la
contraseña es `12345678` o una palabra de diccionario, cae igual que
cualquier otro hash débil (ver `docs/04-password-attacks.md`).

**Variante más rápida: ataque PMKID.** Algunos routers filtran un valor
(PMKID) en el primer mensaje del handshake sin necesitar que ningún
dispositivo se conecte durante la captura — el atacante ni siquiera necesita
esperar a una víctima activa.

### Defensa

- **Contraseña larga y aleatoria** (20+ caracteres, tipo passphrase) — el
  ataque offline se vuelve inviable en la práctica si la contraseña no está
  en ningún diccionario y es demasiado larga para fuerza bruta.
- **WPA3-Personal (SAE)** en vez de WPA2: SAE reemplaza el intercambio
  vulnerable a crackeo offline por un protocolo (Dragonfly) resistente a
  ataques de diccionario offline, aunque la contraseña sea débil.
- En entornos empresariales, usar **WPA2/WPA3-Enterprise (802.1X)** con
  usuario/contraseña o certificados individuales por persona, en vez de una
  única contraseña compartida — así comprometer una credencial no compromete
  la red completa, y se puede revocar acceso a una sola persona.

## 2. Ataques de deautenticación (deauth)

**Cómo funciona**: los frames de gestión 802.11 (como "desconéctate") en
redes WPA2 clásicas **no están autenticados**, así que cualquiera dentro del
alcance de la señal puede enviar paquetes de deautenticación falsificados
haciéndose pasar por el punto de acceso, forzando a un dispositivo a
desconectarse. Se usa para:
- Forzar una reconexión y así capturar el handshake (sección anterior).
- Como denegación de servicio pura: mantener a alguien desconectado
  repetidamente.

### Defensa

- **802.11w (Protected Management Frames / PMF)**: autentica también los
  frames de gestión, así un deauth falsificado se descarta porque no viene
  firmado por el punto de acceso real. Es obligatorio en WPA3 y opcional
  (pero recomendable activar) en WPA2 si el hardware lo soporta.
- Monitorización con un IDS inalámbrico (WIDS) que alerte ante ráfagas
  anómalas de frames de deautenticación.

## 3. Punto de acceso falso (Evil Twin / Rogue AP)

**Cómo funciona**: el atacante crea un punto de acceso con el mismo SSID
(nombre) que una red legítima o conocida (ej. "Aeropuerto_WiFi_Gratis"), a
veces con señal más fuerte para que los dispositivos se conecten
automáticamente (muchos dispositivos recuerdan redes abiertas por nombre y
se conectan solas). Una vez conectada la víctima:
- El atacante controla todo el tráfico no cifrado (MITM, ver
  `docs/03-network-attacks.md`).
- Puede mostrar un portal cautivo falso pidiendo la contraseña real de la
  red WiFi original, o credenciales de otro servicio (variante de phishing).

### Defensa

- Evitar redes abiertas para cosas sensibles; si es necesario usarlas, ir
  siempre con **VPN activa**.
- Desactivar la conexión automática a redes guardadas cuando sea posible, o
  al menos revisar periódicamente la lista de redes "recordadas" en el
  dispositivo.
- Del lado de quien administra la red legítima: WIDS que detecte SSIDs
  duplicados/no autorizados operando cerca de las instalaciones.

## 4. WPS (WiFi Protected Setup) — PIN de 8 dígitos

**Cómo funciona**: WPS permite conectar dispositivos con un PIN de 8 dígitos
en vez de la contraseña completa, pensado para facilidad de uso. El fallo de
diseño: el router valida el PIN en dos mitades independientes (4 dígitos +
3, el octavo es checksum), así que en vez de probar 10^8 combinaciones, un
atacante solo necesita probar como máximo 10^4 + 10^3 — un espacio mucho más
pequeño, factible por fuerza bruta en horas con herramientas como `reaver`.

### Defensa

- **Desactivar WPS por completo** en la configuración del router — la
  mayoría de fabricantes lo trae activado por defecto y muy pocos usuarios
  lo necesitan realmente.

## 5. Redes abiertas / sin cifrado

**Cómo funciona**: sin ningún cifrado, todo el tráfico no protegido a nivel
de aplicación (HTTP plano, DNS) es legible por cualquiera en el mismo canal
con una tarjeta en modo monitor — ni siquiera hace falta "romper" nada.

### Defensa

- No usar redes abiertas para nada sensible sin VPN.
- Si administras una red que debe ser abierta (ej. un negocio), sepárala con
  **aislamiento de clientes** (client isolation) para que los dispositivos
  conectados no puedan verse entre sí, y en una VLAN separada de tu red
  interna.

## Checklist defensivo general (para tu propia red)

- [ ] WPA3-Personal si el router y los dispositivos lo soportan; si no,
      WPA2-Personal con contraseña larga y aleatoria (nunca WEP, roto desde
      hace más de 20 años).
- [ ] WPS desactivado.
- [ ] Firmware del router actualizado (las vulnerabilidades del propio
      router, no solo del protocolo, son un vector común).
- [ ] Red de invitados separada (VLAN distinta) para visitas e IoT, sin
      acceso a tus dispositivos principales.
- [ ] Contraseña de administración del router cambiada del valor por
      defecto.
- [ ] 802.11w / PMF activado si el hardware lo permite.

## Nota legal

Auditar una red WiFi (capturar handshakes, probar WPS, montar un AP de
prueba) sin ser el dueño de esa red o sin autorización explícita por escrito
es ilegal en la mayoría de países, incluso si "solo estás practicando". Haz
esto contra tu propio router en casa, o en laboratorios donde tú controlas
tanto el punto de acceso como los clientes.
