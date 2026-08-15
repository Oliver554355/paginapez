# Ataques de red

## Escaneo de puertos y reconocimiento

**Qué es**: antes de atacar, un atacante (o un pentester autorizado) mapea qué
máquinas están vivas, qué puertos tienen abiertos y qué servicio/versión
corre en cada uno (`nmap` es la herramienta de referencia).

**Cómo funciona**: se envían paquetes TCP/UDP a un rango de puertos y se
interpreta la respuesta:
- Puerto abierto → respuesta SYN-ACK (en un handshake TCP).
- Puerto cerrado → RST.
- Filtrado (firewall) → sin respuesta / ICMP unreachable.

El demo `demos/network-recon/port_scanner.py` implementa esto de forma
simplificada, **limitado a `localhost` por defecto**.

**Defensa**: firewall con "default deny" (solo abrir lo necesario), IDS/IPS
que detecten patrones de escaneo (muchos puertos distintos desde la misma IP
en poco tiempo), y no exponer servicios de administración (SSH, RDP,
paneles) directamente a Internet — usar VPN.

## Man-in-the-Middle (MITM)

**Qué es**: el atacante se sitúa entre la víctima y el destino real,
pudiendo leer o modificar el tráfico.

**Técnicas comunes**:
- **ARP spoofing** en redes LAN: el atacante envía respuestas ARP falsas
  para que el tráfico de la víctima pase por su máquina.
- **Rogue Wi-Fi / Evil Twin**: un punto de acceso falso con el mismo nombre
  que uno legítimo ("WiFi_Cafeteria_Free"), para que los dispositivos se
  conecten automáticamente.
- **DNS spoofing**: responder falsamente a consultas DNS para redirigir a un
  sitio malicioso.
- **SSL stripping**: forzar que la conexión baje de HTTPS a HTTP para poder
  leer el tráfico en claro.

**Defensa**: HTTPS con HSTS (evita el downgrade a HTTP), certificate pinning
en apps móviles, VPN en redes públicas, y en redes corporativas, protecciones
como Dynamic ARP Inspection en los switches.

## Denegación de servicio (DoS/DDoS)

**Qué es**: saturar un servicio (ancho de banda, CPU, conexiones) para que
dejen de responder a usuarios legítimos.

**Cómo funciona a alto nivel** (sin entrar en herramientas de ataque):
- **Volumétrico**: inundar el ancho de banda con tráfico (a menudo
  amplificado vía DNS/NTP/memcached mal configurados).
- **Agotamiento de protocolo**: abusar del handshake TCP (SYN flood) para
  agotar las conexiones que el servidor puede mantener a medio abrir.
- **Capa de aplicación**: peticiones HTTP "legítimas" pero masivas que
  agotan CPU/DB del backend.
- **Botnets**: para lograr volumen, los atacantes usan miles de dispositivos
  comprometidos (IoT, servidores) controlados vía C2 — ver
  [Command & Control](07-command-and-control.md).

**Defensa**: rate limiting, WAF/CDN que absorban tráfico (Cloudflare y
similares), auto-scaling, filtrado en el borde de la red (ISP/upstream), y
"SYN cookies" para mitigar SYN floods a nivel de sistema operativo.

> Este repo no incluye herramientas de ataque de denegación de servicio: es
> una de las categorías con más riesgo de daño real e ilegal si se usa sin
> autorización explícita.
