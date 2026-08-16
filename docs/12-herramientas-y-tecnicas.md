# Técnicas y herramientas: el panorama general

Este documento conecta todo lo anterior: organiza las herramientas reales
que usa la industria (tanto atacantes como pentesters autorizados) según la
fase del ataque en la que se usan, siguiendo el marco de
[`docs/08-defensas-generales.md`](08-defensas-generales.md#el-marco-mental-de-un-pentester-ético).
Es un mapa de "qué existe y para qué sirve", no un manual de uso — cada
herramienta merece su propia documentación oficial antes de tocarla.

## 1. Reconocimiento (OSINT) — antes de tocar el objetivo

Recolectar información pública, sin interactuar directamente con los
sistemas del objetivo.

- **theHarvester**: recolecta correos, subdominios y nombres desde motores
  de búsqueda y fuentes públicas.
- **Shodan / Censys**: buscadores de dispositivos y servicios expuestos a
  Internet (routers, cámaras, servidores mal configurados).
- **Google dorking**: búsquedas avanzadas en Google (`site:`, `filetype:`,
  `intitle:`) para encontrar archivos o páginas expuestas por error.
- **LinkedIn/redes sociales**: mapear organigrama y empleados — base de la
  ingeniería social (`docs/06-social-engineering.md`).
- **whois / dig / nslookup**: información de registro de dominios y DNS.

## 2. Escaneo y enumeración

Ya interactuando con el objetivo, para mapear qué expone.

- **Nmap**: el escáner de puertos y servicios de referencia (ver
  `docs/03-network-attacks.md` y `demos/network-recon/port_scanner.py`, una
  versión simplificada del mismo concepto).
- **Masscan**: como Nmap pero optimizado para escanear rangos enormes muy
  rápido.
- **Wireshark / tcpdump**: captura y análisis de tráfico de red, paquete a
  paquete.
- **Nikto**: escáner de vulnerabilidades web conocidas en servidores.
- **Gobuster / ffuf / dirb**: fuerza bruta de rutas y subdominios ocultos
  (`/admin`, `/backup`, etc.) probando listas de palabras.
- **BloodHound**: mapea relaciones de permisos en Active Directory para
  encontrar rutas de escalación de privilegios (ej. "este usuario de bajo
  nivel tiene, sin saberlo, un camino de 3 pasos hasta Domain Admin").

## 3. Explotación

- **Metasploit Framework**: la plataforma más conocida para desarrollar y
  ejecutar exploits contra vulnerabilidades conocidas, con una base de datos
  enorme de módulos ya escritos.
- **Burp Suite / OWASP ZAP**: proxies para interceptar, modificar y repetir
  peticiones HTTP — la herramienta central para probar XSS, IDOR, lógica de
  negocio rota, etc. (ver `docs/05-web-attacks.md` y
  `demos/web-vulnerabilities/webapp/`).
- **sqlmap**: automatiza la detección y explotación de SQL injection (el
  mismo bug que `demos/web-vulnerabilities/sqli_demo.py` muestra a mano).
- **Aircrack-ng suite**: captura y crackeo de redes WiFi (ver
  `docs/11-ataques-wifi.md`).
- **John the Ripper / Hashcat**: crackeo de hashes de contraseñas offline —
  el mismo concepto que `demos/password-security/demo.py`, pero optimizado
  con GPU y reglas de mutación de palabras mucho más sofisticadas.
- **Social Engineering Toolkit (SET)**: automatiza la creación de campañas
  de phishing/pretexting para pruebas autorizadas.

## 4. Post-explotación y movimiento lateral

- **Mimikatz**: extrae credenciales (contraseñas, hashes, tickets Kerberos)
  de la memoria de un Windows comprometido.
- **Cobalt Strike / Sliver**: plataformas de C2 comercial/open-source usadas
  en pruebas de red team para simular un adversario avanzado persistente
  (ver `docs/07-command-and-control.md`).
- **PowerShell Empire**: framework de post-explotación basado en PowerShell,
  aprovechando "living off the land" (`docs/10-anti-forense-y-deteccion.md`).
- **CrackMapExec / NetExec**: automatiza pruebas de credenciales y
  enumeración a través de muchas máquinas de una red Windows a la vez.

## 5. Ingeniería inversa y análisis de malware (para el lado defensivo)

- **Ghidra / IDA Pro**: descompiladores/desensambladores para analizar qué
  hace un binario sin tener el código fuente — esencial para analistas de
  malware, no solo atacantes.
- **x64dbg / GDB**: depuradores para ejecutar un binario paso a paso y
  observar su comportamiento.
- **Cuckoo Sandbox / entornos aislados (VM sin red)**: para detonar malware
  de forma controlada y observar qué hace, sin riesgo de que se propague.

## 6. Forense y respuesta a incidentes (lado defensivo)

- **Volatility**: análisis forense de volcados de memoria RAM — encuentra
  procesos, conexiones de red y artefactos que ya no están en disco (útil
  contra malware "fileless", ver `docs/10-anti-forense-y-deteccion.md`).
- **Autopsy / Sleuth Kit**: análisis forense de discos e imágenes de disco.
- **YARA**: reglas para identificar patrones de malware conocido en
  archivos o memoria — lo usan tanto antivirus como analistas manuales.
- **SIEM (Splunk, Wazuh, ELK/Elastic)**: centraliza y correlaciona logs de
  toda una organización para detectar patrones de ataque (el punto central
  de la sección "Por qué no es tan fácil" en
  `docs/10-anti-forense-y-deteccion.md`).

## Cómo se relaciona todo esto con este repo

Cada categoría de arriba tiene su versión simplificada, explicada y segura
en `demos/`, para que veas el concepto sin necesitar instalar el arsenal
completo desde el día uno:

| Categoría real | Demo equivalente en este repo |
|---|---|
| Escaneo (Nmap) | `demos/network-recon/port_scanner.py` |
| Crackeo de contraseñas (Hashcat/John) | `demos/password-security/demo.py` |
| SQLi (sqlmap) | `demos/web-vulnerabilities/sqli_demo.py` |
| Proxy web / XSS (Burp Suite) | `demos/web-vulnerabilities/webapp/` |
| Ingeniería social (SET) | `demos/phishing-awareness/` |

La ruta natural desde aquí: entender el concepto con las demos de este repo
→ practicar con la herramienta real en un laboratorio legal (TryHackMe,
HackTheBox, tu propio Kali) → nunca contra sistemas sin autorización (ver
`docs/08-defensas-generales.md`).
