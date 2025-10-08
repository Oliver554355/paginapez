<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>SIMULACIÓN DE PRUEBA - Página de Login (Demo)</title>
<style>
  body{font-family:system-ui,Segoe UI,Roboto,Arial;margin:0;background:#f4f6f8;display:flex;align-items:center;justify-content:center;height:100vh}
  .card{background:white;padding:24px;border-radius:10px;box-shadow:0 6px 20px rgba(0,0,0,0.08);width:360px}
  h1{font-size:18px;margin:0 0 12px}
  .badge{display:inline-block;background:#ffcc00;color:#000;padding:6px 10px;border-radius:6px;font-weight:700;margin-bottom:12px}
  label{display:block;font-size:13px;margin-top:10px}
  input{width:100%;padding:10px;border-radius:6px;border:1px solid #dfe6ee;margin-top:6px}
  button{margin-top:14px;width:100%;padding:10px;border-radius:8px;border:0;background:#0066cc;color:#fff;font-weight:600}
  .result{margin-top:12px;padding:10px;border-radius:8px;background:#f0f7ff;color:#003366;display:none}
  .help{font-size:13px;color:#556; margin-top:8px}
  .warning{color:#990000;font-weight:700;margin-top:8px}
</style>
</head>
<body>
  <div class="card" role="main">
    <span class="badge">SIMULACIÓN / PRUEBA</span>
    <h1>Inicio de sesión — DEMO</h1>
    <p class="help">Esta página es una demostración. No introduzcas contraseñas reales. Al enviar se mostrará información educativa.</p>

    <form id="demoForm" onsubmit="handleSubmit(event)">
      <label for="user">Usuario o correo</label>
      <input id="user" name="user" type="text" placeholder="tucorreo@ejemplo.com" autocomplete="off" required />
      <label for="pass">Contraseña</label>
      <input id="pass" name="pass" type="password" placeholder="••••••••" autocomplete="off" required />
      <button type="submit">Iniciar sesión</button>
    </form>

    <div id="result" class="result" role="status" aria-live="polite"></div>

    <p class="warning">Nota: esta es una <strong>simulación educativa</strong>. No se ha enviado ni guardado tu contraseña en ningún servidor.</p>
    <p class="help">Consejos rápidos para detectar phishing: verifica el dominio en la barra de direcciones, busca HTTPS y certificado válido, desconfía de mensajes con urgencia o enlaces acortados.</p>
  </div>

<script>
  function handleSubmit(e){
    e.preventDefault();
    const u = document.getElementById('user').value || '[sin usuario]';
    const r = document.getElementById('result');
    r.style.display = 'block';
    r.innerHTML = `<strong>SIMULACIÓN COMPLETADA</strong><br>Has introducido: <em>${escapeHtml(u)}</em>.<br><br>Esto es solo una prueba. Recuerda: nunca introducir contraseñas reales en formularios sospechosos.`;
    document.getElementById('demoForm').reset();
  }
  function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
</script>
</body>
</html>
