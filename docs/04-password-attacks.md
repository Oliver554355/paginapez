# Ataques a contraseñas

## Técnicas principales

- **Fuerza bruta**: probar todas las combinaciones posibles. Lento contra
  contraseñas largas, pero trivial contra PINs de 4 dígitos.
- **Diccionario**: probar contraseñas comunes (`123456`, `password`,
  filtraciones previas) — mucho más rápido que fuerza bruta pura porque la
  gente reutiliza patrones predecibles.
- **Credential stuffing**: usar pares usuario/contraseña filtrados de OTRA
  brecha, probándolos en muchos sitios distintos, aprovechando que la gente
  reutiliza contraseñas.
- **Password spraying**: en vez de probar muchas contraseñas contra un
  usuario, se prueban unas pocas contraseñas comunes contra MUCHOS usuarios,
  para evitar bloqueos por intentos fallidos.
- **Rainbow tables**: tablas precalculadas de hash→contraseña para revertir
  hashes rápidamente, si no se usó "salt".

## Por qué el hashing (bien hecho) importa

Un sistema serio nunca guarda la contraseña en texto plano, sino un **hash**
(función unidireccional). Pero no todos los hashes son iguales:

- `MD5`/`SHA1` sin salt: rápidos de calcular → un atacante con GPU puede
  probar miles de millones de hashes por segundo. **Inseguros para
  contraseñas.**
- Con **salt** (un valor aleatorio único por usuario, añadido antes del
  hash): impide usar rainbow tables precalculadas, porque cada hash es único
  incluso si dos usuarios comparten contraseña.
- Algoritmos diseñados para contraseñas — **bcrypt, scrypt, Argon2** — son
  deliberadamente lentos y costosos en memoria, para que probar millones de
  combinaciones por segundo sea inviable incluso con hardware potente.

El demo `demos/password-security/demo.py` compara en la práctica cuánto tarda
un ataque de diccionario contra un hash rápido (SHA-256 sin salt) vs. uno
lento (bcrypt), usando solo datos locales de ejemplo.

## Defensa

- Usar **Argon2/bcrypt/scrypt** con salt para almacenar contraseñas (nunca
  hashes rápidos genéricos).
- **MFA** (idealmente FIDO2/passkeys) para que una contraseña filtrada no sea
  suficiente para entrar.
- **Rate limiting y bloqueo progresivo** de intentos de login por IP/usuario.
- **Política de longitud** en vez de complejidad forzada: una frase larga
  (`correcto-caballo-batería-grapa`) es más fuerte y memorable que
  `P@ssw0rd1`.
- **Gestor de contraseñas** para no reutilizar contraseñas entre sitios —
  así una brecha en un sitio no compromete el resto.
- Monitorizar filtraciones (ej. Have I Been Pwned) para forzar cambio de
  contraseña si aparece en una brecha conocida.
