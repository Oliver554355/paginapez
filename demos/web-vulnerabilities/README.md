# Demos de vulnerabilidades web

- **`sqli_demo.py`** — SQL injection contra SQLite en memoria, versión
  vulnerable (bypass de login como admin) vs. versión con consultas
  parametrizadas. No requiere dependencias externas.

  ```
  python3 sqli_demo.py
  ```

- **`webapp/`** — app Flask con dos vulnerabilidades reales, en el
  navegador, cada una con su versión vulnerable y su versión corregida:
  - **XSS almacenado**: un formulario de comentarios donde `/vulnerable/...`
    ejecuta el HTML/JS que escribas, y `/seguro/...` lo escapa.
  - **IDOR**: una ruta de "factura" donde `/vulnerable/...` te deja ver la
    factura de cualquier usuario solo cambiando el ID en la URL, y
    `/seguro/...` comprueba que la factura pertenezca al usuario en sesión.

  ```
  pip install flask
  python3 webapp/app.py
  # abre http://127.0.0.1:5000/
  ```

  Todo corre en memoria, en local, sin base de datos externa ni conexión a
  Internet. El "login" del demo es solo para simular dos usuarios (Alice y
  Bob) y ver el efecto del IDOR — no es un sistema de autenticación real.

Ver `docs/05-web-attacks.md` para la explicación conceptual de cada
vulnerabilidad y sus defensas.
