# Phishing

## Qué es

Un ataque de **ingeniería social** que suplanta una identidad confiable (un
banco, una empresa, un compañero de trabajo) para engañar a la víctima y
conseguir credenciales, datos sensibles o que ejecute una acción (pagar,
instalar algo, hacer clic).

## Cómo funciona técnicamente

1. **Pretexto**: un correo, SMS ("smishing"), llamada ("vishing") o mensaje en
   redes que imita a una fuente legítima, normalmente con urgencia o miedo
   ("tu cuenta será bloqueada").
2. **Señuelo**: un enlace a una página que clona visualmente el login real
   (dominio parecido, certificado válido pero de otro dominio, o incluso
   HTTPS legítimo en un dominio typosquatted como `paypa1.com`).
3. **Captura**: el formulario envía usuario/contraseña (o tarjeta, OTP, etc.)
   al servidor del atacante en vez del real.
4. **Uso inmediato**: muchos kits de phishing reenvían las credenciales en
   tiempo real a un bot de Telegram/Discord o a un panel web, para usarlas
   antes de que la víctima cambie la contraseña.
5. **Variantes avanzadas**: *phishing con proxy inverso* (Evilginx y
   similares) que se sitúan en medio de la sesión real y roban también la
   cookie de sesión, saltándose incluso el 2FA por OTP.

## Cómo lo "controla" el atacante

- **Kits de phishing**: paquetes prearmados (HTML clonado + backend de
  captura) que se despliegan en hosting barato o comprometido.
  El demo `demos/phishing-awareness/` muestra la parte visual de esto, pero
  **sin backend real**: no envía nada a ningún servidor.
- **Paneles de administración**: para campañas grandes, el atacante usa un
  panel donde ve qué víctimas cayeron, desde qué IP, con qué user-agent.
- **Infraestructura desechable**: dominios y hosting que se abandonan tras
  horas o días para dificultar el rastreo (dominios registrados minutos antes
  del envío de la campaña).

## Cómo detectarlo y prevenirlo

- **Verifica el dominio real**, no solo que diga "https" — pasa el ratón
  sobre el enlace antes de hacer clic, o mira la URL completa en el móvil.
- **Desconfía de la urgencia**: "tu cuenta se bloqueará en 24h" es una técnica
  clásica de presión.
- **2FA resistente a phishing**: usa llaves FIDO2/WebAuthn (passkeys) en vez
  de solo OTP por SMS/app, porque los proxies inversos pueden interceptar OTP
  pero no pueden clonar una llave física.
- **Gestor de contraseñas**: autocompleta solo en el dominio real, así que si
  no autocompleta en una página "idéntica", es una señal de alerta.
- **Filtros de correo (SPF/DKIM/DMARC)** del lado de la organización para
  reducir el spoofing del remitente.
- **Simulaciones internas de phishing** (como el demo incluido) para entrenar
  a empleados a reconocer las señales, sin exponer datos reales.
- **Reportar y aislar**: si caíste, cambia la contraseña inmediatamente,
  revisa sesiones activas/cookies y activa 2FA.
