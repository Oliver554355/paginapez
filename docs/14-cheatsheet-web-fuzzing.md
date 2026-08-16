# Cheat sheet: fuzzing web con ffuf y gobuster

Comparación y comandos de referencia rápida. Ver también
[`docs/12-herramientas-y-tecnicas.md`](12-herramientas-y-tecnicas.md) para
dónde encajan estas herramientas dentro del flujo completo, y
[`docs/13-metodologia-htb.md`](13-metodologia-htb.md) (paso 2, enumeración
HTTP) para cuándo usarlas en una máquina real.

## ffuf vs. Gobuster vs. dirb — diferencias

| | **ffuf** | **Gobuster** | **dirb** |
|---|---|---|---|
| Lenguaje | Go | Go | C |
| Velocidad | Muy rápido | Muy rápido | Notablemente más lento |
| Qué puede fuzzear | Cualquier parte de la petición: rutas, subdominios/vhosts, parámetros GET/POST, headers, cookies — usas `FUZZ` como marcador en cualquier lugar | Modos fijos: `dir` (rutas), `dns` (subdominios), `vhost`, `s3` (buckets) — menos flexible pero más directo | Solo rutas/directorios |
| Filtrado de resultados | Muy potente: por código de status, tamaño de respuesta, líneas, palabras, tiempo de respuesta — clave para filtrar falsos positivos | Filtrado básico por status code | Casi nada, bastante ruido |
| Recursividad | Sí, configurable | Sí (`-r` en modo dir) | Sí por defecto (y eso lo hace lento) |
| Mantenimiento | Activo, el más moderno de los tres | Activo | Prácticamente abandonado |

**Recomendación**: usa **ffuf** por defecto (más versátil, mejor filtrado de
ruido). **Gobuster** como alternativa simple y directa. **dirb** solo si no
tienes las otras dos a mano.

## ffuf

```bash
# Fuzzing de directorios/archivos básico
ffuf -u http://10.10.10.10/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Con extensiones comunes (php, html, txt, bak)
ffuf -u http://10.10.10.10/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt \
     -e .php,.html,.txt,.bak

# Filtrar ruido: excluir código 404, o por tamaño de respuesta (-fs) si el
# "no encontrado" real da 200 pero con un tamaño de página fijo
ffuf -u http://10.10.10.10/FUZZ -w wordlist.txt -fc 404
ffuf -u http://10.10.10.10/FUZZ -w wordlist.txt -fs 1234

# Recursivo (sigue fuzzeando dentro de directorios que encuentra)
ffuf -u http://10.10.10.10/FUZZ -w wordlist.txt -recursion -recursion-depth 2

# Fuzzing de subdominios / vhosts (usando el header Host)
ffuf -u http://10.10.10.10/ -H "Host: FUZZ.empresa.htb" -w subdomains.txt -fs 1234

# Fuzzing de parámetro POST (útil para login, formularios)
ffuf -u http://10.10.10.10/login -w wordlist.txt \
     -X POST -d "username=admin&password=FUZZ" -H "Content-Type: application/x-www-form-urlencoded" \
     -fc 401

# Dos wordlists a la vez (usuario Y contraseña, ej. fuerza bruta de login)
ffuf -u http://10.10.10.10/login -w users.txt:USER -w passwords.txt:PASS \
     -X POST -d "username=USER&password=PASS" -fc 401

# Controlar velocidad/hilos (si el servidor rate-limitea o quieres ser más sigiloso)
ffuf -u http://10.10.10.10/FUZZ -w wordlist.txt -t 40 -rate 100

# Guardar resultados
ffuf -u http://10.10.10.10/FUZZ -w wordlist.txt -o resultados.json -of json
```

## Gobuster

```bash
# Modo dir: directorios/archivos
gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt

# Con extensiones y excluyendo 404
gobuster dir -u http://10.10.10.10 -w wordlist.txt -x php,html,txt,bak -b 404

# Recursivo
gobuster dir -u http://10.10.10.10 -w wordlist.txt -r

# Solo mostrar ciertos status codes
gobuster dir -u http://10.10.10.10 -w wordlist.txt -s 200,204,301,302,403

# Modo dns: subdominios
gobuster dns -d empresa.htb -w subdomains.txt

# Modo vhost: virtual hosts (máquinas con varios sitios en la misma IP)
gobuster vhost -u http://empresa.htb -w subdomains.txt --append-domain

# Con autenticación básica o cookie de sesión
gobuster dir -u http://10.10.10.10 -w wordlist.txt -U usuario -P contraseña
gobuster dir -u http://10.10.10.10 -w wordlist.txt -c "session=abc123"

# Más hilos / guardar salida
gobuster dir -u http://10.10.10.10 -w wordlist.txt -t 50 -o resultados.txt
```

## Wordlists recomendadas

Vienen con SecLists (`sudo apt install seclists` en Kali):

- Para empezar rápido: `/usr/share/wordlists/dirb/common.txt`
- Más exhaustivo: `/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt`
- Subdominios: `/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt`

## Nota legal

Igual que el resto de este repo: usa estos comandos solo contra tus propios
sistemas, laboratorios legales (HackTheBox, TryHackMe) o con autorización
explícita por escrito. Ver
[`docs/08-defensas-generales.md`](08-defensas-generales.md).
