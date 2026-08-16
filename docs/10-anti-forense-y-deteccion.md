# Anti-forense: cómo intentan no dejar rastro (y cómo se los detecta igual)

Este documento es la contraparte de
[`docs/07-command-and-control.md`](07-command-and-control.md): una vez el
atacante tiene acceso, intenta que su actividad no aparezca en logs ni en un
análisis forense posterior. A nivel conceptual, para que sepas qué debe
vigilar un defensor — no es una guía operativa paso a paso.

## Técnicas que usan (a nivel conceptual)

- **Borrar o modificar logs**: eliminar entradas del Visor de Eventos de
  Windows, `/var/log/auth.log` en Linux, o logs de aplicaciones, para que no
  quede registro del acceso o los comandos ejecutados.
- **Timestomping**: cambiar las marcas de tiempo (creación/modificación) de
  un archivo malicioso para que se mezcle con archivos legítimos del sistema
  y no destaque en un análisis cronológico.
- **"Living off the land" (LOLBins)**: usar herramientas que ya vienen con
  el sistema operativo (PowerShell, `certutil`, `wmic`, `bash`) en vez de
  subir herramientas propias — así no hay un "archivo malicioso nuevo" que
  detectar, solo uso (inusual) de programas legítimos.
- **Operar solo en memoria (fileless malware)**: ejecutar código sin
  escribirlo nunca a disco, para que un análisis forense del disco duro no
  encuentre el binario después del reinicio.
- **Anonimizar el origen**: usar VPNs, Tor, o servidores intermedios
  comprometidos (para que el log de la víctima muestre esa IP intermedia, no
  la real del atacante) y así dificultar la atribución.
- **Infraestructura desechable**: dominios/servidores que se usan una vez y
  se abandonan, para que rastrear el C2 no lleve a nada reutilizable.
- **Cifrar el tráfico de C2**: para que aunque alguien capture el tráfico de
  red, no pueda leer las órdenes ni los datos exfiltrados.
- **Limpieza final**: al terminar, borrar herramientas subidas, revertir
  cambios de configuración, y en el peor caso (ransomware), destruir shadow
  copies y backups locales para impedir la recuperación sin pagar.

## Por qué NO es tan fácil como parece (y aquí es donde gana el defensor)

Cada técnica de arriba tiene un punto débil que el lado defensivo explota:

| Técnica del atacante | Por qué falla o se detecta |
|---|---|
| Borrar logs locales | Si los logs se envían en tiempo real a un servidor centralizado (SIEM/syslog remoto), borrarlos en la máquina comprometida no borra la copia ya enviada — el atacante necesitaría comprometer también el SIEM. |
| Timestomping | Cambia timestamps "normales" (mtime/atime), pero deja rastro en metadatos de bajo nivel del sistema de archivos (ej. `$MFT` en NTFS, journals) que las herramientas forenses sí revisan. |
| LOLBins | El *contenido* del binario es legítimo, pero el **contexto de ejecución** no lo es — un EDR con detección de comportamiento marca cosas como "Word abrió PowerShell con una cadena codificada en base64", aunque `powershell.exe` sea 100% legítimo. |
| Fileless / solo en memoria | Sobrevive mientras la máquina esté encendida — un volcado de memoria (memory forensics) en ese momento, o un EDR que inspeccione procesos en vivo, sí lo detecta. Además, para persistir tras un reinicio casi siempre necesita dejar *algo* en disco (aunque sea una línea de registro). |
| Anonimizar el origen (VPN/Tor) | Oculta la IP, pero no borra los **patrones de comportamiento**: horarios de actividad, estilo de código, infraestructura reutilizada entre campañas, errores operativos — así es como se han identificado atacantes reales pese a usar Tor. |
| Limpieza al final | Si hay backups **inmutables y fuera de alcance** del atacante (air-gapped u offline), la limpieza/destrucción local no los afecta. |

## La lección defensiva central

**No confíes en que el log solo viva en la máquina que puede ser
comprometida.** La estrategia de detección que realmente funciona es:

1. **Centralizar logs fuera del alcance del atacante** (SIEM, syslog remoto,
   almacenamiento append-only) — así "borrar el rastro" requeriría
   comprometer un sistema aparte, con sus propios controles.
2. **Detectar comportamiento, no solo firmas** — un EDR moderno no busca
   "el archivo malicioso conocido", busca secuencias de acciones anómalas
   (proceso hijo inesperado, conexión saliente rara, acceso a `lsass.exe`).
3. **Vigilar la red, no solo el host** — el tráfico de red hacia el C2 deja
   rastro aunque el host esté "limpio" (ver
   [`docs/07-command-and-control.md`](07-command-and-control.md)).
4. **Backups verdaderamente aislados** — la única garantía real contra
   "borraron todo, incluidos mis backups" es que el atacante nunca haya
   podido alcanzarlos en primer lugar (offline, air-gapped, o con
   permisos de solo-escritura desde los sistemas de producción).
5. **Honeypots y canary tokens**: archivos o credenciales señuelo que nadie
   legítimo debería tocar — si algo interactúa con ellos, es una alerta de
   alta confianza, sin importar cuánto se haya cuidado el atacante en el
   resto del sistema.

## Nota legal

Estas técnicas, usadas para acceder o permanecer sin autorización en un
sistema ajeno, son delito independientemente de qué tan "limpio" se haga —
no ocultar rastro no legaliza el acceso no autorizado. El valor de conocerlas
es exclusivamente defensivo: son exactamente lo que un equipo de respuesta a
incidentes / threat hunting debe saber buscar. Ver
[`docs/08-defensas-generales.md`](08-defensas-generales.md) para el marco
legal y ético general de este repo.
