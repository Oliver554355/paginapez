# Command & Control (C2) y persistencia

Esta es la pregunta de "cómo se controlan" las herramientas de ataque una vez
comprometen un sistema.

## Qué es un C2

Una vez que el malware se ejecuta en la máquina víctima, normalmente no actúa
de forma completamente autónoma: se conecta a un servidor remoto controlado
por el atacante para recibir órdenes y enviar datos. Ese servidor (y el
protocolo que usa) es el **Command & Control**.

## Patrones habituales de comunicación

- **Beaconing**: el implante en la víctima "llama a casa" cada cierto
  intervalo (ej. cada 60s) preguntando "¿hay órdenes para mí?", en vez de que
  el servidor inicie la conexión — así funciona incluso detrás de NAT/firewall,
  porque la conexión sale desde dentro.
- **Jitter**: se añade aleatoriedad al intervalo de beaconing para que el
  tráfico no tenga un patrón perfectamente periódico, más difícil de detectar.
- **Canales de comunicación disfrazados de tráfico legítimo**:
  - HTTPS normal (indistinguible de navegación web sin inspección profunda).
  - DNS tunneling (los datos viajan codificados en subdominios de consultas
    DNS, un tráfico que casi nunca se bloquea).
  - Servicios legítimos como infraestructura ("living off trusted sites"):
    usar Telegram, Discord, GitHub Gists o Slack como "buzón" de órdenes,
    porque esos dominios rara vez están bloqueados.
- **Dominios de respaldo / DGA (Domain Generation Algorithm)**: el malware
  genera muchos nombres de dominio posibles algorítmicamente; el atacante
  solo necesita registrar uno para retomar el control si el dominio principal
  es bloqueado.

## Persistencia (sobrevivir a un reinicio)

- Windows: claves de registro `Run`/`RunOnce`, tareas programadas, servicios,
  DLL hijacking.
- Linux/macOS: `cron`, `systemd` units, `.bashrc`/`.profile`, LaunchAgents.
- Más sigiloso: modificar el firmware/bootloader (muy raro, muy avanzado) o
  crear cuentas de usuario adicionales con acceso remoto.

## Movimiento lateral

Tras el primer punto de apoyo, el atacante busca escalar: robar credenciales
en memoria (`Mimikatz`-style), reutilizar tickets Kerberos, o explotar
confianza entre máquinas (SSH keys, shares compartidos) para llegar a
sistemas más valiosos (controladores de dominio, bases de datos).

## Cómo se detecta y se corta (perspectiva defensiva)

- **Monitorización de tráfico saliente**: la mayoría de redes vigilan lo que
  entra, pero el C2 se detecta vigilando **conexiones salientes** inusuales
  (beaconing periódico, volúmenes anómalos, destinos con mala reputación).
- **DNS logging y análisis**: consultas DNS a dominios recién registrados o
  con patrones tipo DGA son una señal fuerte.
- **EDR con detección de comportamiento**: procesos inusuales iniciando
  conexiones de red (ej. `notepad.exe` abriendo un socket).
- **Segmentación de red y "zero trust"**: limitar qué puede hablar con qué,
  para que incluso si un equipo cae, el movimiento lateral sea difícil.
- **Threat intelligence / listas de bloqueo**: compartir indicadores de
  compromiso (IPs, dominios, hashes de C2 conocidos) entre organizaciones.
- **Plan de respuesta a incidentes**: aislar la máquina comprometida de la
  red (no solo "limpiarla") en cuanto se detecta beaconing, para cortar el
  canal de control antes de que se ejecute la orden final (ej. cifrado
  masivo).
