# Cómo intentan saltarse la verificación en dos pasos (2FA) y cómo evitarlo

El 2FA reduce muchísimo el riesgo de una contraseña filtrada, pero no es
infalible — cada método de 2FA tiene puntos débiles distintos. Conocerlos
es clave tanto para elegir bien qué tipo de 2FA usar como para reconocer
cuándo alguien intenta explotarlos contra ti.

## 1. Phishing en tiempo real con proxy inverso (AiTM — Adversary in the Middle)

**Cómo funciona**: herramientas como Evilginx colocan un proxy entre la
víctima y el sitio real. La víctima entra a la página falsa, escribe su
usuario/contraseña, y **también su código OTP** — el proxy los reenvía en
tiempo real al sitio legítimo, y captura la **cookie de sesión** ya
autenticada que el sitio real devuelve. El atacante importa esa cookie y
queda dentro de la cuenta, sin necesitar el código de nuevo.

Es el método más efectivo hoy contra OTP por SMS/apps tipo Google
Authenticator, porque no "rompe" el 2FA — simplemente se sienta en medio de
un login legítimo y se roba el resultado.

**Defensa**: **passkeys/FIDO2 (WebAuthn)**. Este método de 2FA está atado
criptográficamente al dominio real — el navegador se niega a completar el
desafío si el dominio no coincide exactamente, así que un proxy en un
dominio falso no puede capturar nada útil, aunque la víctima intente
"iniciar sesión" ahí. Es la única categoría de 2FA verdaderamente resistente
a este ataque.

## 2. SIM swapping

**Cómo funciona**: el atacante engaña o soborna a un empleado de la
operadora telefónica (o explota un proceso débil de verificación) para
transferir el número de teléfono de la víctima a una SIM que él controla.
A partir de ahí, recibe los SMS de OTP y los códigos de recuperación de
cuenta enviados por SMS.

**Defensa**: no usar SMS como único factor de recuperación de cuentas
importantes; usar apps de autenticación (TOTP) o passkeys en vez de SMS
siempre que el servicio lo permita; pedir a tu operadora un PIN adicional
o bloqueo específico contra portabilidad no autorizada, si lo ofrecen.

## 3. "MFA fatigue" / push bombing

**Cómo funciona**: cuando el 2FA es una notificación push ("¿eres tú? Sí/No")
en vez de un código, el atacante que ya tiene la contraseña dispara muchas
solicitudes de login seguidas, de madrugada o durante horas de trabajo,
esperando que la víctima apruebe una por cansancio, confusión o sin pensar.

**Defensa**: usar apps de MFA con **verificación de número/contexto**
(mostrar la ubicación/dispositivo que originó la solicitud, y requerir
escribir un número que aparece en pantalla, no solo tocar "Aprobar"), y
formar a los usuarios para que un push inesperado sea señal de alerta
inmediata (cambiar contraseña, reportarlo), nunca "aprobar para que pare".

## 4. Ingeniería social directa (vishing al soporte / a la víctima)

**Cómo funciona**: dos variantes comunes:
- Llamar al **soporte técnico** del servicio haciéndose pasar por la
  víctima ("perdí mi teléfono, no puedo generar el código"), pidiendo
  desactivar el 2FA o resetear la cuenta por otra vía.
- Llamar a la **víctima** haciéndose pasar por el banco/soporte ("estamos
  viendo actividad sospechosa, léame el código que le acaba de llegar para
  verificar su identidad") — el código que la víctima "verifica" es en
  realidad el que el atacante generó al intentar entrar en ese momento.

**Defensa**: procesos de soporte con verificación de identidad robusta
(no solo "responder una pregunta de seguridad"), y sobre todo: **ningún
servicio legítimo pide leer un código OTP por teléfono**. Un código que te
llega sin que tú hayas iniciado el proceso, seguido de alguien pidiéndotelo
por teléfono, es 100% un ataque.

## 5. Robo de sesión / cookies (sin tocar el 2FA en absoluto)

**Cómo funciona**: si el atacante obtiene la cookie de sesión ya
autenticada de otra forma (malware infostealer en el dispositivo de la
víctima, XSS que exfiltra `document.cookie`, ver
`docs/05-web-attacks.md`), el 2FA nunca entra en juego — la sesión ya pasó
esa verificación antes de ser robada.

**Defensa**: cookies de sesión `HttpOnly` y `Secure`, tiempos de expiración
de sesión razonables, revocar sesiones activas al detectar actividad
anómala, y "re-autenticación" (pedir contraseña/2FA de nuevo) para acciones
sensibles aunque la sesión siga activa.

## 6. Fuerza bruta / reutilización de códigos TOTP débiles

**Cómo funciona**: menos común, pero posible si un servicio no limita
intentos: un código TOTP de 6 dígitos es solo 1 millón de combinaciones,
válido durante ~30 segundos — sin rate limiting, es forzable en ese margen.

**Defensa**: rate limiting estricto y bloqueo tras pocos intentos fallidos
de código 2FA, igual que con contraseñas.

## 7. Códigos de respaldo (backup codes) mal protegidos

**Cómo funciona**: casi todo servicio con 2FA da códigos de respaldo por si
pierdes el dispositivo — si esos códigos quedan guardados en texto plano
(una nota, una captura de pantalla en la nube, un archivo sin cifrar), son
un salto directo al 2FA sin romper nada técnico.

**Defensa**: tratar los códigos de respaldo con el mismo cuidado que una
contraseña — guardarlos en un gestor de contraseñas cifrado, nunca en texto
plano accesible.

## Resumen: qué tipo de 2FA elegir

De menos a más resistente frente a estos ataques:

1. **SMS** — vulnerable a SIM swapping y a phishing AiTM. Mejor que nada,
   pero el más débil.
2. **App TOTP** (Google Authenticator, Authy) — inmune a SIM swapping,
   pero sigue siendo vulnerable a phishing en tiempo real (AiTM).
3. **Push con verificación de número** — mejor que push simple, sigue
   siendo vulnerable a AiTM si el usuario aprueba sin verificar.
4. **Passkeys / FIDO2 (WebAuthn)** — resistente a phishing por diseño,
   porque está atado criptográficamente al dominio real. Es el estándar
   recomendado hoy para cuentas de alto valor.

Ver también [`docs/01-phishing.md`](01-phishing.md) para el contexto
completo de por qué el phishing con proxy inverso rompe el 2FA tradicional,
y [`docs/04-password-attacks.md`](04-password-attacks.md) para la primera
línea de defensa (contraseñas fuertes y únicas) que hace que ni siquiera
llegue a necesitarse saltarse el 2FA.
