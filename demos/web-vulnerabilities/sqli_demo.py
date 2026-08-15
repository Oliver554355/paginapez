#!/usr/bin/env python3
"""
Demo educativa de SQL Injection: versión vulnerable vs. versión segura,
contra una base de datos SQLite creada en memoria, en local.

No se conecta a ningún servidor ni base de datos real de terceros.

Uso:
    python3 sqli_demo.py
"""
import sqlite3


def setup_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            clave TEXT,
            es_admin INTEGER
        )
    """)
    conn.executemany(
        "INSERT INTO usuarios (nombre, clave, es_admin) VALUES (?, ?, ?)",
        [
            ("alice", "s3cr3t!", 0),
            ("bob", "hunter2", 0),
            ("admin", "S3curePasswordNoAdivinable!", 1),
        ],
    )
    conn.commit()
    return conn


def login_vulnerable(conn, nombre, clave):
    """VULNERABLE: concatena la entrada del usuario directamente en el SQL."""
    query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}' AND clave = '{clave}'"
    print(f"  SQL ejecutado: {query}")
    cur = conn.execute(query)
    return cur.fetchone()


def login_seguro(conn, nombre, clave):
    """SEGURO: usa una consulta parametrizada (prepared statement)."""
    query = "SELECT * FROM usuarios WHERE nombre = ? AND clave = ?"
    print(f"  SQL ejecutado: {query}   con parámetros = ({nombre!r}, {clave!r})")
    cur = conn.execute(query, (nombre, clave))
    return cur.fetchone()


def main():
    conn = setup_db()

    print("=" * 70)
    print("1) Login normal con credenciales correctas (ambas versiones funcionan)")
    print("=" * 70)
    print("Vulnerable:", login_vulnerable(conn, "alice", "s3cr3t!"))
    print("Seguro:    ", login_seguro(conn, "alice", "s3cr3t!"))

    print("\n" + "=" * 70)
    print("2) Ataque: intentar entrar como 'admin' sin conocer la contraseña")
    print("   payload de usuario: admin' -- ")
    print("=" * 70)

    payload_nombre = "admin' -- "
    payload_clave = "cualquier-cosa"

    print("\n[Versión VULNERABLE]")
    resultado = login_vulnerable(conn, payload_nombre, payload_clave)
    if resultado and resultado[3] == 1:
        print(f"  -> ¡BYPASS EXITOSO! Entró como admin sin contraseña: {resultado}")
    else:
        print(f"  -> No entró: {resultado}")

    print("\n[Versión SEGURA]")
    try:
        resultado = login_seguro(conn, payload_nombre, payload_clave)
        print(f"  -> {'BYPASS (no debería pasar)' if resultado else 'Bloqueado correctamente: sin resultados'}")
    except sqlite3.Error as e:
        print(f"  -> Error de BD (no bypass): {e}")

    print("\n" + "=" * 70)
    print("Por qué funciona el ataque en la versión vulnerable:")
    print("=" * 70)
    print("""
    El payload "admin' -- " convierte la consulta en:

        SELECT * FROM usuarios WHERE nombre = 'admin' -- ' AND clave = '...'

    Todo después de "--" es un comentario SQL, así que la comprobación de
    clave desaparece por completo. En la versión parametrizada, el driver
    de la base de datos trata "admin' -- " como un simple valor de texto
    literal (nunca como parte del SQL), así que no hay ningún usuario
    llamado literalmente "admin' -- " y el login falla.

    Ver docs/05-web-attacks.md para más detalle y otras variantes de SQLi.
    """)


if __name__ == "__main__":
    main()
