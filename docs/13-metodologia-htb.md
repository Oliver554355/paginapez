# Metodología para máquinas de HackTheBox (y CTFs similares)

Guía paso a paso de cómo abordar una máquina de HTB desde cero hasta la
flag de root/administrator, aplicando el marco de
[`docs/08-defensas-generales.md`](08-defensas-generales.md#el-marco-mental-de-un-pentester-ético)
con las herramientas de [`docs/12-herramientas-y-tecnicas.md`](12-herramientas-y-tecnicas.md).

## 0. Preparación

- Conecta la VPN de HTB (`sudo openvpn <tu-archivo>.ovpn`) y confirma que
  haces ping a la IP de la máquina.
- Crea una carpeta de trabajo por máquina, con subcarpetas para escaneos,
  exploits descargados, y notas — te va a ahorrar caos cuando lleves varias
  máquinas hechas. Ejemplo:
  ```
  mkdir -p ~/htb/<nombre-maquina>/{scans,exploits,notas}
  ```
- Toma notas desde el primer comando, no al final — herramientas como
  Obsidian, CherryTree o simplemente un `notas.md` sirven. El "por qué"
  de cada paso vale tanto como el resultado, para cuando quieras repetir el
  proceso en otra máquina o escribir un writeup.

## 1. Reconocimiento: escaneo de puertos completo

Primero un escaneo rápido de **todos** los puertos (no solo los top 1000),
porque muchas máquinas de HTB esconden el servicio interesante en un puerto
no estándar:

```bash
nmap -p- --min-rate=1000 -T4 <IP> -oN scans/todos-los-puertos.txt
```

Con los puertos abiertos encontrados, un escaneo de detección de versión y
scripts por defecto **solo sobre esos puertos**:

```bash
nmap -p<puertos-encontrados> -sC -sV -oN scans/detalle.txt <IP>
```

`-sC` corre scripts NSE por defecto (detecta cosas como listados anónimos de
FTP, información de SMB, certificados TLS con nombres útiles) y `-sV`
identifica versión exacta del servicio — clave para el paso 3.

Si hay un puerto UDP relevante sospechado (poco común pero pasa), un escaneo
UDP aparte (`-sU`), que es mucho más lento.

## 2. Enumeración por servicio

Con la lista de puertos/servicios, profundiza en cada uno. Los más comunes:

- **HTTP/HTTPS (80/443)**:
  - Mira el código fuente y las cookies desde el navegador primero, a mano.
  - `whatweb <IP>` o `wappalyzer` para identificar tecnología (CMS, framework).
  - `gobuster dir -u http://<IP> -w <wordlist>` para rutas ocultas
    (`/admin`, `/backup`, `/.git`, paneles de login).
  - Si hay subdominios en juego, añádelos a `/etc/hosts` y prueba
    `gobuster vhost` también.
- **SMB (139/445)**: `smbclient -L //<IP>/ -N` (login nulo) y
  `enum4linux -a <IP>` — muy común encontrar shares con permisos abiertos.
- **FTP (21)**: prueba login anónimo (`anonymous`/sin contraseña) antes que
  nada.
- **SSH (22)**: normalmente no es el vector de entrada directo, pero la
  versión importa para buscar CVEs conocidos.
- **Bases de datos expuestas (MySQL/PostgreSQL/Redis/MongoDB)**: revisa si
  aceptan conexión sin autenticación o con credenciales por defecto.

## 3. Buscar vulnerabilidades conocidas

Con el servicio y versión exacta identificados en el paso 1:

```bash
searchsploit <servicio> <versión>
```

y cruza con búsquedas manuales ("`<servicio> <versión>` exploit", CVE en
Google/GitHub). La mayoría de máquinas "fáciles" de HTB explotan una
vulnerabilidad pública conocida de una versión desactualizada — el valor
del ejercicio está en identificarla y aplicarla correctamente, no en
descubrir un 0-day.

## 4. Conseguir el punto de apoyo inicial (foothold)

Con la vulnerabilidad identificada, consigue ejecución de comandos o una
shell — puede ser:
- Explotar una vulnerabilidad web (XSS/SQLi/subida de archivos insegura —
  ver `docs/05-web-attacks.md`) a través de Burp Suite.
- Un exploit público adaptado (revisa siempre el código de un exploit
  descargado antes de correrlo, para entender qué hace).
- Credenciales encontradas en la enumeración (un archivo de config
  expuesto, un share de SMB legible, credenciales por defecto).

Una vez tienes ejecución de comandos, **estabiliza la shell** a una TTY
completa (para poder usar `Ctrl+C`, autocompletado, editores):

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
# luego, en tu terminal de atacante:
# Ctrl+Z, stty raw -echo; fg, y export TERM=xterm
```

## 5. Enumeración local y escalación de privilegios

Ya dentro como usuario de bajo privilegio, busca el camino a root/admin:

- **Linux**: corre `linpeas.sh` (o revisa a mano) — busca binarios SUID
  inusuales, entradas de `sudo -l`, cron jobs escribibles, versión de kernel
  con CVE conocido, credenciales en archivos de configuración o historial de
  bash.
- **Windows**: `winpeas.exe`, `PowerUp.ps1` — busca servicios con permisos
  débiles, tareas programadas, `AlwaysInstallElevated`, credenciales
  guardadas, tokens de proceso con privilegios altos.
- **Active Directory** (en máquinas más avanzadas): BloodHound para mapear
  el camino de escalación (ver `docs/12-herramientas-y-tecnicas.md`).

Este paso es donde más tiempo se pasa realmente — es normal tardar más en
escalar privilegios que en conseguir el foothold inicial.

## 6. Captura la flag y documenta

- Lee la flag (`user.txt`, `root.txt`/`system.txt` según la plataforma).
- **Escribe el writeup mientras lo tienes fresco**: qué encontraste en cada
  fase, qué comando exacto funcionó y por qué, qué intentaste que NO
  funcionó (a veces es lo más útil para la próxima vez). Es lo que de verdad
  fija el aprendizaje, más que resolver la máquina en sí.

## Errores comunes de quien empieza

- Saltar directo a herramientas automatizadas de explotación sin entender
  qué hacen — te bloqueas en cuanto algo no sale exactamente como en un
  tutorial.
- No hacer el escaneo de **todos** los puertos (`-p-`) y perderse el
  servicio real en un puerto no estándar.
- No leer el código fuente de un exploit descargado antes de ejecutarlo.
- Rendirse antes de la escalación de privilegios — conseguir el foothold es
  solo la mitad del ejercicio.
- No tomar notas — repetir investigación que ya hiciste hace una semana.

## Recordatorio

HTB es exactamente el tipo de entorno para el que se autorizó este
aprendizaje — máquinas diseñadas para ser atacadas. Las mismas técnicas
contra un sistema real sin autorización siguen las reglas de
[`docs/08-defensas-generales.md`](08-defensas-generales.md).
