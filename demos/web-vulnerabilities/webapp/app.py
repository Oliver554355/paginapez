#!/usr/bin/env python3
"""
Demo educativa en el navegador: XSS almacenado e IDOR, versión vulnerable
vs. versión corregida, corriendo en local (localhost:5000).

No usa base de datos externa ni se conecta a Internet. Todo el "login" es
falso (solo para simular sesiones de dos usuarios distintos, Alice y Bob) —
no es un sistema de autenticación real, es exclusivamente para ver el bug.

Requiere Flask:
    pip install flask
    python3 app.py
    -> abre http://127.0.0.1:5000/

Rutas:
    /vulnerable/comentarios   XSS almacenado real (el <script> se ejecuta)
    /seguro/comentarios       misma función, pero escapando la salida
    /vulnerable/factura/<id>  IDOR: ves facturas de cualquier usuario
    /seguro/factura/<id>      misma función, pero comprobando propiedad
"""
from flask import Flask, request, session, redirect, url_for, render_template_string
from markupsafe import Markup, escape

app = Flask(__name__)
app.secret_key = "solo-para-esta-demo-local-no-usar-en-produccion"

# --- "Base de datos" en memoria, solo para la demo ---
USERS = {1: "Alice", 2: "Bob"}
INVOICES = {
    101: {"owner_id": 1, "total": "€42.00", "detalle": "Suscripción mensual"},
    102: {"owner_id": 2, "total": "€99.90", "detalle": "Renovación anual"},
}
comments_vulnerable = []
comments_safe = []

BASE = """
<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>{{ title }}</title>
<style>
  body{font-family:system-ui,Arial;max-width:640px;margin:40px auto;padding:0 16px;color:#222}
  nav a{margin-right:14px}
  .warn{background:#fff3cd;border:1px solid #ffe08a;padding:10px;border-radius:6px;margin:14px 0}
  .ok{background:#e7f7e7;border:1px solid #9ed49e;padding:10px;border-radius:6px;margin:14px 0}
  textarea,input{width:100%;box-sizing:border-box;padding:8px;margin-top:6px}
  button{margin-top:10px;padding:8px 14px}
  .comment{border-bottom:1px solid #eee;padding:8px 0}
  code{background:#f3f3f3;padding:1px 4px;border-radius:3px}
</style></head><body>
<nav>
  <a href="/">Inicio</a>
  <a href="/vulnerable/comentarios">XSS vulnerable</a>
  <a href="/seguro/comentarios">XSS corregido</a>
  <a href="/vulnerable/factura/101">IDOR vulnerable</a>
  <a href="/seguro/factura/101">IDOR corregido</a>
</nav>
<hr>
{{ body|safe }}
</body></html>
"""


def render(title, body):
    return render_template_string(BASE, title=title, body=body)


@app.route("/")
def index():
    user = session.get("user_id")
    quien = USERS.get(user, "nadie (no has 'iniciado sesión')")
    body = f"""
    <h1>Demo: XSS e IDOR</h1>
    <p>Sesión actual: <strong>{quien}</strong></p>
    <p><a href="/login/1">Entrar como Alice</a> · <a href="/login/2">Entrar como Bob</a> · <a href="/logout">Salir</a></p>
    <ul>
      <li><a href="/vulnerable/comentarios">/vulnerable/comentarios</a> — XSS almacenado real</li>
      <li><a href="/seguro/comentarios">/seguro/comentarios</a> — mismo formulario, salida escapada</li>
      <li><a href="/vulnerable/factura/101">/vulnerable/factura/101</a> — abre la factura de Alice estando logueado como Bob</li>
      <li><a href="/seguro/factura/101">/seguro/factura/101</a> — mismo caso, con comprobación de propiedad</li>
    </ul>
    <p>Explicación en <code>docs/05-web-attacks.md</code>.</p>
    """
    return render("Demo XSS/IDOR", body)


@app.route("/login/<int:user_id>")
def login(user_id):
    if user_id in USERS:
        session["user_id"] = user_id
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))


# ---------------------------------------------------------------------
# XSS almacenado: vulnerable vs. seguro
# ---------------------------------------------------------------------

def comments_page(title, comments, vulnerable: bool):
    if vulnerable:
        rendered = "".join(f'<div class="comment"><b>{c["nombre"]}</b>: {c["mensaje"]}</div>' for c in comments)
        warn = ('<div class="warn"><b>VULNERABLE:</b> el mensaje se inserta tal cual en el HTML. '
                'Prueba a escribir un nombre o mensaje con '
                '<code>&lt;script&gt;alert(document.cookie)&lt;/script&gt;</code> y verás que se ejecuta.</div>')
    else:
        rendered = "".join(
            f'<div class="comment"><b>{escape(c["nombre"])}</b>: {escape(c["mensaje"])}</div>' for c in comments
        )
        warn = ('<div class="ok"><b>CORREGIDO:</b> el mismo payload de arriba se escapa y se muestra '
                'como texto plano en vez de ejecutarse.</div>')

    form = f"""
    {warn}
    <form method="post">
      <label>Nombre</label><input name="nombre" required>
      <label>Mensaje</label><textarea name="mensaje" required></textarea>
      <button type="submit">Publicar</button>
    </form>
    <h3>Comentarios</h3>
    {rendered or '<p><em>Sin comentarios todavía.</em></p>'}
    """
    return render(title, f"<h1>{title}</h1>{form}")


@app.route("/vulnerable/comentarios", methods=["GET", "POST"])
def comentarios_vulnerable():
    if request.method == "POST":
        comments_vulnerable.append({
            "nombre": request.form["nombre"],
            # Markup() marca la cadena como "segura" sin escaparla -> el bug típico
            "mensaje": Markup(request.form["mensaje"]),
        })
    return comments_page("Comentarios (VULNERABLE a XSS)", comments_vulnerable, vulnerable=True)


@app.route("/seguro/comentarios", methods=["GET", "POST"])
def comentarios_seguro():
    if request.method == "POST":
        comments_safe.append({
            "nombre": request.form["nombre"],
            "mensaje": request.form["mensaje"],
        })
    return comments_page("Comentarios (corregido)", comments_safe, vulnerable=False)


# ---------------------------------------------------------------------
# IDOR: vulnerable vs. seguro
# ---------------------------------------------------------------------

def render_invoice(inv_id, inv):
    dueño = USERS.get(inv["owner_id"], "?")
    return f"""
    <h1>Factura #{inv_id}</h1>
    <p>Propietario: <strong>{dueño}</strong></p>
    <p>Total: {inv['total']}</p>
    <p>Detalle: {inv['detalle']}</p>
    """


@app.route("/vulnerable/factura/<int:inv_id>")
def factura_vulnerable(inv_id):
    inv = INVOICES.get(inv_id)
    if not inv:
        return render("Factura no encontrada", "<p>No existe esa factura.</p>"), 404
    warn = ('<div class="warn"><b>VULNERABLE (IDOR):</b> esta ruta nunca comprueba si la factura '
            'pertenece al usuario de la sesión actual — solo comprueba que exista el ID.</div>')
    return render("Factura (VULNERABLE a IDOR)", warn + render_invoice(inv_id, inv))


@app.route("/seguro/factura/<int:inv_id>")
def factura_segura(inv_id):
    inv = INVOICES.get(inv_id)
    if not inv:
        return render("Factura no encontrada", "<p>No existe esa factura.</p>"), 404

    user_id = session.get("user_id")
    if user_id != inv["owner_id"]:
        body = (f'<div class="warn"><b>403 — Acceso denegado:</b> la factura #{inv_id} no pertenece a tu '
                f'sesión actual ({USERS.get(user_id, "sin sesión")}). Esta ruta SÍ comprueba propiedad.</div>'
                f'<p><a href="/login/{inv["owner_id"]}">Entrar como {USERS[inv["owner_id"]]}</a> para ver esta factura legítimamente.</p>')
        return render("Acceso denegado", body), 403

    ok = '<div class="ok"><b>CORREGIDO:</b> se comprobó que la factura pertenece al usuario en sesión.</div>'
    return render("Factura (corregido)", ok + render_invoice(inv_id, inv))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
