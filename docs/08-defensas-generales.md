# Defensa en profundidad: guía general

Resumen de los principios que se repiten en todos los documentos anteriores,
más el camino recomendado si quieres seguir esto en serio, como hacker de
sombrero blanco.

## Principios que aparecen una y otra vez

1. **Defensa en capas**: ningún control es perfecto; se combinan varios
   (firewall + EDR + MFA + backups) para que el fallo de uno no comprometa
   todo.
2. **Menor privilegio**: cada cuenta/proceso/servicio con solo el acceso que
   necesita, nada más — así el daño de una brecha queda contenido.
3. **Reducir superficie de ataque**: apagar/desinstalar lo que no se usa,
   cerrar puertos innecesarios, deshabilitar macros y protocolos legacy.
4. **Parchear rápido**: la mayoría de incidentes explotan vulnerabilidades
   conocidas y ya parcheadas, no días-cero.
5. **Detectar, no solo prevenir**: asume que algo va a fallar — invierte en
   poder *ver* qué pasa (logs, EDR, monitorización de red) y responder rápido.
6. **Backups probados y aislados**: la única defensa real garantizada contra
   ransomware es poder restaurar sin pagar.
7. **El factor humano importa más que la tecnología**: la mejor protección
   técnica no sirve si alguien da su contraseña por teléfono. Formación
   continua > un curso anual.
8. **Autenticación fuerte**: MFA (idealmente passkeys/FIDO2) en todo lo que
   importe, contraseñas únicas por sitio vía gestor de contraseñas.

## El marco mental de un pentester ético

1. **Reconocimiento (recon)**: entender el objetivo (con autorización) —
   qué expone a Internet, qué tecnologías usa.
2. **Enumeración**: mapear en detalle (puertos, servicios, versiones,
   usuarios) — ver `docs/03-network-attacks.md`.
3. **Explotación**: usar una vulnerabilidad para conseguir acceso — ver
   `docs/05-web-attacks.md`, `docs/04-password-attacks.md`.
4. **Post-explotación**: qué se podría hacer con ese acceso (persistencia,
   movimiento lateral) — ver `docs/07-command-and-control.md`, siempre
   documentando, nunca causando daño real en un pentest autorizado.
5. **Reporte**: lo más importante del trabajo — explicar el hallazgo, el
   impacto real, y **cómo arreglarlo**, en un lenguaje que el equipo técnico
   pueda accionar.

## Cómo seguir aprendiendo (legal y práctico)

- **Laboratorios legales**: TryHackMe, HackTheBox, PortSwigger Web Security
  Academy (gratis y excelente para XSS/SQLi), OWASP Juice Shop (app
  intencionalmente vulnerable para practicar en local).
- **CTFs**: competiciones tipo captura-la-bandera, diseñadas para practicar
  sin tocar sistemas reales de nadie.
- **Certificaciones de referencia**: eJPT/PJPT (nivel entrada), OSCP (el
  estándar práctico de la industria), CEH (más teórico).
- **Bug bounty**: plataformas como HackerOne/Bugcrowd, donde empresas
  autorizan explícitamente a buscar vulnerabilidades en su infraestructura a
  cambio de recompensa — la forma legal de "hackear de verdad" sistemas de
  terceros.
- **Monta tu propio laboratorio**: máquinas virtuales aisladas (VirtualBox +
  Kali Linux + una VM víctima deliberadamente vulnerable como Metasploitable)
  para practicar todo lo de este repo con las manos, sin riesgo legal.

## La línea legal, en una frase

Todo lo de este repo es legítimo para **aprender, defender, o atacar
sistemas propios/autorizados explícitamente**. En el momento en que el
objetivo es un sistema de un tercero sin su permiso por escrito, deja de ser
un ejercicio de seguridad y pasa a ser un delito, sin importar cuán "curioso"
sea el motivo.
