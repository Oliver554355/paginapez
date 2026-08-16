# Más vectores de ataque web

Continuación de [`docs/05-web-attacks.md`](05-web-attacks.md) (que cubre
SQLi, XSS, CSRF, IDOR y deserialización insegura). Aquí el resto de
técnicas más relevantes para atacar/auditar una aplicación web.

## Command Injection (inyección de comandos de sistema)

**Qué es**: cuando la app ejecuta un comando del sistema operativo
incluyendo entrada del usuario sin sanitizar.

```python
# VULNERABLE: si la app hace ping a una IP que el usuario ingresa
os.system(f"ping -c 4 {ip_usuario}")
# payload: "8.8.8.8; cat /etc/passwd" -> ejecuta AMBOS comandos
```

**Defensa**: evitar invocar el shell con entrada del usuario. Si es
inevitable, usar APIs que pasen argumentos como lista (no como string
concatenado, ej. `subprocess.run(["ping","-c","4",ip], shell=False)`), y
validar la entrada contra una lista blanca estricta (ej. solo IPs con
formato válido).

## Path Traversal / LFI / RFI

**Path Traversal**: manipular una ruta de archivo para salir del
directorio esperado usando `../`.
```
GET /descargar?archivo=../../../../etc/passwd
```

**Local File Inclusion (LFI)**: cuando la app además *incluye/ejecuta* el
archivo leído (común en PHP con `include($_GET['pagina'])`), no solo lo
muestra — si el atacante logra que un archivo con código PHP quede en el
servidor (ej. subiendo un log envenenado), puede lograr ejecución de código.

**Remote File Inclusion (RFI)**: variante donde la app incluye un archivo
desde una URL externa controlada por el atacante, si la configuración lo
permite — ejecución de código directa.

**Defensa**: nunca construir rutas de archivo concatenando entrada de
usuario directamente; usar una lista blanca de archivos permitidos o un ID
que mapee internamente a la ruta real, y canonicalizar/validar que la ruta
resultante siga dentro del directorio esperado.

## SSRF (Server-Side Request Forgery)

**Qué es**: la aplicación hace una petición HTTP a una URL que el usuario
controla (ej. "genera una miniatura de esta imagen desde esta URL"), y el
atacante la apunta a recursos internos que normalmente no serían
alcanzables desde fuera.

```
POST /generar-miniatura
url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
```
(en entornos cloud, esa IP interna expone metadatos, a veces incluyendo
credenciales temporales del servidor).

**Defensa**: lista blanca estricta de dominios/IPs permitidos para
peticiones salientes, bloquear rangos de IP privados/internos (RFC1918,
link-local) a nivel de red, y no confiar en validaciones solo del lado de
la aplicación (un atacante puede usar redirecciones HTTP para saltarlas).

## XXE (XML External Entity)

**Qué es**: si un parser XML mal configurado procesa entidades externas,
un XML malicioso puede leer archivos locales del servidor o hacer
peticiones SSRF:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<usuario>&xxe;</usuario>
```

**Defensa**: deshabilitar el procesamiento de entidades externas (DTD) en
el parser XML — la mayoría de librerías modernas lo permiten con una sola
opción de configuración, y debería ser el valor por defecto en cualquier
endpoint que reciba XML de fuentes no confiables.

## SSTI (Server-Side Template Injection)

**Qué es**: cuando entrada del usuario se pasa a un motor de plantillas
(Jinja2, Twig, Freemarker) y se renderiza como plantilla en vez de como
texto plano, permitiendo ejecutar código en el motor de plantillas —y en
varios motores, desde ahí, código arbitrario del sistema.

```
{{ 7*7 }}   -> si la respuesta muestra "49", el input se está interpretando
               como plantilla, no como texto
```

**Defensa**: nunca renderizar plantillas construidas con entrada de
usuario; pasar la entrada como **dato** a una plantilla fija, nunca como
la plantilla en sí.

## Ataques de subida de archivos (file upload)

**Qué es**: si una app permite subir archivos sin validar bien tipo/
contenido, un atacante sube un archivo ejecutable (ej. un `.php` disfrazado
de imagen) a una carpeta accesible por web, y luego lo ejecuta visitando su
URL.

**Defensa**: validar el **contenido real** del archivo (no solo la
extensión o el `Content-Type`, que el atacante controla), renombrar
archivos subidos con un ID aleatorio, servirlos desde un dominio/carpeta
sin permiso de ejecución de código, y idealmente desde un almacenamiento
separado (bucket de objetos) en vez del mismo servidor de aplicación.

## Ataques a JWT (JSON Web Tokens)

**Qué es**: fallos comunes en implementaciones de autenticación con JWT:
- **`alg: none`**: algunas librerías aceptan tokens que declaran no tener
  firma — un atacante arma un token con los claims que quiera y lo pone
  como "sin firma".
- **Confusión de algoritmo (RS256→HS256)**: si el servidor no fija el
  algoritmo esperado, un atacante puede firmar un token con HMAC usando la
  clave **pública** RSA del servidor (que es... pública) como secreto.
- **Secreto débil**: si el token usa HS256 con un secreto corto/adivinable,
  se puede crackear offline y firmar tokens arbitrarios.

**Defensa**: fijar explícitamente el algoritmo esperado del lado del
servidor (nunca confiar en el `alg` que declara el propio token), usar
secretos largos y aleatorios, y preferir algoritmos asimétricos (RS256) con
las claves correctamente separadas.

## Open Redirect

**Qué es**: un parámetro que redirige al usuario a una URL controlada por
él (`/redirigir?url=...`), usado en phishing para que un enlace parezca del
dominio legítimo pero termine en un sitio malicioso.

**Defensa**: lista blanca de destinos permitidos, o rutas relativas
internas en vez de aceptar URLs completas arbitrarias.

## Clickjacking

**Qué es**: la página víctima se carga dentro de un `<iframe>` invisible
superpuesto sobre una página del atacante, engañando al usuario para que
haga clic en algo que cree que es otra cosa (ej. "dar like" en realidad
ejecuta "transferir dinero").

**Defensa**: header `X-Frame-Options: DENY` (o `Content-Security-Policy:
frame-ancestors 'none'`) para impedir que la página se cargue dentro de un
iframe ajeno.

## Errores de configuración (Security Misconfiguration)

La categoría más común en la práctica, no por ser sofisticada sino por lo
frecuente: `.git/` expuesto en producción, paneles de administración sin
autenticación adicional, mensajes de error verbosos que revelan stack
traces o rutas internas, credenciales por defecto sin cambiar, CORS
configurado con `Access-Control-Allow-Origin: *` en endpoints que requieren
autenticación, backups (`.bak`, `.zip`) accesibles públicamente.

**Defensa**: checklist de hardening antes de desplegar a producción,
escaneo automatizado (Nikto, `demos` de este repo) que busque exactamente
estos descuidos, y nunca desplegar con configuración de desarrollo/debug.

## Vulnerabilidades específicas de APIs (BOLA, mass assignment)

- **BOLA (Broken Object Level Authorization)**: es IDOR aplicado a APIs —
  `GET /api/usuarios/123` sin verificar que el usuario autenticado tenga
  permiso sobre el recurso `123`.
- **Mass assignment**: un endpoint que acepta un JSON completo y lo mapea
  directamente a un modelo de base de datos, permitiendo que el atacante
  incluya campos que no debería poder controlar (ej. `"es_admin": true` en
  un registro de usuario, si el backend no filtra qué campos acepta).

**Defensa**: autorización explícita por objeto en cada endpoint (no
asumir que "estar autenticado" es suficiente), y listas blancas explícitas
de qué campos puede escribir cada endpoint, nunca deserializar el JSON
completo directamente a un modelo con privilegios.

## Cómo practicar todo esto (legal)

- **PortSwigger Web Security Academy** (gratis): laboratorios específicos
  para cada uno de estos vectores, con explicación paso a paso.
- **OWASP Juice Shop**: app deliberadamente vulnerable con casi todos estos
  bugs juntos, pensada para practicar.
- El demo de este repo (`demos/web-vulnerabilities/webapp/`) cubre XSS e
  IDOR con código legible; es un buen punto de partida antes de saltar a
  los laboratorios más grandes.
