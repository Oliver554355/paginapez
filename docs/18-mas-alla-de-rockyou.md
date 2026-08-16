# Más allá de rockyou.txt: cómo generan wordlists reales los atacantes

`rockyou.txt` (14 millones de contraseñas filtradas en la brecha de
RockYou de 2009) es el wordlist que aparece en todos los tutoriales porque
es gratis, viene preinstalado en Kali, y funciona bien contra contraseñas
genéricas de práctica. Pero un ataque dirigido de verdad casi nunca se
queda ahí — usa wordlists construidas específicamente para el objetivo.
Complementa [`docs/04-password-attacks.md`](04-password-attacks.md).

## 1. Wordlists generadas desde el propio objetivo (OSINT)

- **CeWL**: rastrea el sitio web de la empresa objetivo y extrae todas las
  palabras que aparecen — nombres de producto, jerga interna, nombres de
  empleados mencionados — para armar un wordlist específico de esa
  organización.
  ```bash
  cewl https://empresa.com -d 3 -m 5 -w wordlist_empresa.txt
  ```
- **CUPP (Common User Passwords Profiler)**: genera contraseñas candidatas
  a partir de datos personales de una persona específica (nombre, apellido,
  fecha de nacimiento, nombre de mascota, pareja) — la gente arma
  contraseñas con datos de su propia vida de forma muy predecible.
- Perfiles de redes sociales, biografías corporativas, nombres de
  proyectos internos filtrados en repositorios públicos de código — todo
  alimenta el mismo wordlist dirigido.

## 2. Compilaciones de brechas reales (no solo una)

`rockyou.txt` es una sola brecha de hace 15 años. Los atacantes serios
combinan **docenas de brechas** distintas (recopilaciones como "COMB" —
Compilation of Many Breaches — con miles de millones de credenciales de
brechas de LinkedIn, Adobe, Yahoo, y cientos más), porque:
- Cubren contraseñas más recientes y de más servicios.
- Permiten **credential stuffing** directo: si alguien reutilizó la misma
  contraseña que usó en otro sitio ya filtrado, no hace falta "adivinar"
  nada, solo probar el par usuario+contraseña ya conocido.

## 3. Reglas de mutación (rule-based attacks), no solo la lista tal cual

En vez de probar solo las palabras del diccionario literalmente, se les
aplican **reglas de transformación** para cubrir las variantes típicas que
la gente usa al "reforzar" una contraseña de diccionario:

```
password       -> Password1  Password!  P4ssw0rd  password123  drowssap
```

Hashcat trae reglas ya armadas y muy efectivas (`best64.rule`,
`OneRuleToRuleThemAll.rule`) que capturan los patrones más comunes:
mayúscula inicial, número al final, sustituciones leet (`a`→`4`, `e`→`3`),
símbolo al final, palabra al revés.

```bash
hashcat -m 0 hashes.txt rockyou.txt -r rules/best64.rule
```

Esto multiplica un wordlist de 14 millones en cientos de millones de
candidatos derivados, cubriendo muchas más contraseñas reales sin
necesitar un diccionario más grande.

## 4. Ataques de máscara (mask attacks)

Cuando se conoce (u observa) la **política de contraseñas** del objetivo
(ej. "mínimo 8 caracteres, una mayúscula, un número, un símbolo"), en vez
de probar todo el espacio de contraseñas posibles, se define un patrón
exacto que las cumple y se prueba solo eso:

```bash
# Mayúscula + 5 minúsculas + 2 dígitos: patrón típico de contraseña "generada" corporativa
hashcat -m 0 hashes.txt -a 3 ?u?l?l?l?l?l?d?d
```

Reduce drásticamente el espacio de búsqueda comparado con fuerza bruta
pura, porque explota lo predecible de cómo la gente cumple una política de
contraseñas en vez de generarla realmente al azar.

## 5. Ataques híbridos (wordlist + máscara)

Combina ambos: toma una palabra base del diccionario y le agrega un patrón
al final (`palabra` + `?d?d?d?d` para años, por ejemplo), capturando el
patrón muy común de "palabra conocida + número/año":

```bash
hashcat -m 0 hashes.txt -a 6 wordlist.txt ?d?d?d?d
# prueba: empresa2023, empresa2024, verano2024, etc.
```

Muy efectivo contra patrones estacionales corporativos
(`Verano2024!`, `Empresa2025`) que muchas organizaciones terminan usando
sin darse cuenta al forzar "cambia tu contraseña cada 90 días".

## 6. Password spraying con listas curadas (no rockyou completo)

Para [`docs/04-password-attacks.md`](04-password-attacks.md#técnicas-principales)
(password spraying: pocas contraseñas contra muchos usuarios, para evitar
bloqueos), usar las 14 millones de rockyou sería absurdo — se usan listas
muy cortas y curadas de las contraseñas realmente más comunes en el
contexto (`Password123!`, `Bienvenido1!`, `<NombreEmpresa>2024!`),
maximizando probabilidad de acierto con el mínimo de intentos por usuario.

## Por qué esto importa para la defensa

Todas estas técnicas explotan un mismo hecho: **la aleatoriedad humana es
muy baja**. La gente no genera contraseñas al azar, genera variaciones
predecibles de palabras conocidas. La defensa real no es "que rockyou.txt
no tenga tu contraseña" — es romper la predictibilidad:

- **Verificar contraseñas nuevas contra listas de brechas conocidas** al
  registrarlas (la API de "Have I Been Pwned Passwords" permite esto sin
  enviar la contraseña en texto plano, usando k-anonimato con hash
  parcial) — rechazar cualquier contraseña que ya aparezca filtrada.
- **Longitud sobre complejidad forzada**: una passphrase larga y aleatoria
  (`correcto-caballo-batería-grapa`) no sigue ningún patrón de mutación
  predecible; una política de "mayúscula+número+símbolo" en cambio
  **empuja** a la gente hacia patrones muy predecibles (`Palabra1!`), que es
  justo lo que capturan las reglas de mutación de arriba.
- **No forzar rotación periódica sin motivo**: es la causa directa de
  patrones estacionales predecibles (`Verano2024!` → `Otoño2024!`).
- **MFA** (ver `docs/16-bypass-2fa.md`) como red de seguridad cuando, pese
  a todo, una contraseña cae.
- **Rate limiting y detección de spraying**: alertar sobre intentos
  fallidos distribuidos entre muchos usuarios distintos desde el mismo
  origen en poco tiempo, no solo bloquear por intentos repetidos en una
  sola cuenta.
