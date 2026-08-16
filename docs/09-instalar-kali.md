# Instalar Kali Linux directo en el disco (reemplazando todo)

> ⚠️ **Esto borra TODO el contenido actual del disco de tu laptop.** No es
> reversible una vez confirmas el particionado en el instalador. Sigue el
> checklist de backup antes de continuar. Si tienes dudas, es más seguro
> practicar primero con una VM (ver más abajo) antes de hacer esto.

## 0. Checklist antes de empezar (no te lo saltes)

- [ ] **Backup completo** de todo lo que quieras conservar (documentos,
      fotos, proyectos) a un disco externo o la nube. Verifica que el backup
      abre bien, no solo que "se copió".
- [ ] Anota las **redes WiFi guardadas**, licencias de software, y cualquier
      archivo que solo exista en ese disco.
- [ ] Confirma que tu laptop **carga y arranca sin problemas** ahora mismo
      (si tiene fallos de hardware, arréglalos antes, no durante la
      instalación).
- [ ] Ten un cargador conectado durante todo el proceso — que se apague a
      mitad de la instalación puede dejar el disco en un estado roto.
- [ ] Anota el modelo exacto de tu laptop y busca si el chip WiFi es
      compatible con modo monitor (relevante si planeas auditoría WiFi) —
      búscalo como "`<modelo de tu laptop>` wifi chipset kali linux monitor
      mode".

## 1. Descargar la imagen oficial

Desde **kali.org/get-kali** (nunca de un mirror no oficial), la imagen
"Installer" (no la "Live", que es para USB sin instalar) para tu
arquitectura (casi seguro `amd64` si es un laptop normal de los últimos
años).

**Verifica el checksum** del archivo descargado contra el que publica la
web oficial, para asegurarte de que no se corrompió ni fue alterado:

```bash
sha256sum kali-linux-*-installer-amd64.iso
# compara el resultado con el SHA256 publicado en kali.org
```

## 2. Crear el USB booteable

- **Windows/Mac**: usa [Rufus](https://rufus.ie/) (Windows) o
  [balenaEtcher](https://etcher.balena.io/) (multiplataforma) — seleccionas
  la ISO y el USB, y escribe la imagen.
- **Linux**: `sudo dd if=kali-linux-*.iso of=/dev/sdX bs=4M status=progress && sync`
  (reemplaza `/dev/sdX` por tu USB real — comprueba con `lsblk` primero,
  **si te equivocas de disco aquí puedes borrar el disco equivocado**).

Necesitas un USB de al menos 8GB, que se borrará por completo.

## 3. Configurar el arranque desde USB

1. Reinicia el laptop y entra a la BIOS/UEFI (normalmente `F2`, `F10`,
   `F12`, `Del` o `Esc` justo al encender — depende de la marca).
2. Si tu laptop tiene **Secure Boot**, puede que necesites desactivarlo
   temporalmente para bootear el instalador (varía según el hardware).
3. Cambia el **orden de arranque** para que priorice el USB, o usa el menú
   de arranque rápido (Boot Menu) para elegirlo una sola vez.

## 4. Instalar

1. Arranca desde el USB y elige **"Graphical Install"**.
2. Sigue los pasos normales: idioma, teclado, nombre de host, usuario no-root
   (Kali moderno ya no recomienda usar root como usuario diario), contraseña
   fuerte.
3. En el paso de **particionado**, elige **"Usar el disco completo"** — esto
   es lo que borra todo lo que había antes. Si tienes dudas en este paso,
   detente aquí y confirma tu backup antes de continuar.
4. Se recomienda activar **cifrado de disco (LVM encriptado)** en este paso
   — así si te roban el laptop, los datos no son legibles sin tu contraseña.
5. Instala el gestor de arranque **GRUB** en el disco principal cuando lo
   pida.
6. Termina la instalación y reinicia (retira el USB cuando lo indique).

## 5. Primeros pasos después de instalar

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y kali-linux-headless   # o kali-linux-default para el set completo de herramientas
```

- Confirma que el usuario que creaste **no es root** por defecto (usa `sudo`
  para tareas administrativas) — es la configuración recomendada desde Kali
  2020.1.
- Verifica WiFi/Bluetooth funcionando: `ip a`, `nmcli device wifi list`.
- Si vas a usar herramientas de red inalámbrica, revisa que tu chip soporte
  modo monitor: `iw list | grep -A 10 "Supported interface modes"`.

## 6. Después de instalar: úsalo bien

- Todo lo que hagas desde aquí sigue las reglas de
  [`docs/08-defensas-generales.md`](08-defensas-generales.md): solo contra
  sistemas propios o con autorización explícita por escrito.
- Empieza practicando contra las demos de este mismo repo
  (`demos/web-vulnerabilities/webapp/`, tu propio `port_scanner.py`) o
  laboratorios legales como TryHackMe/HackTheBox/OWASP Juice Shop.
- Mantén el sistema actualizado (`sudo apt update && sudo apt upgrade`)
  regularmente — Kali también es un sistema Linux normal que necesita
  parches.

## Alternativa más segura para aprender: VM en vez de disco completo

Si en algún momento prefieres no tener el disco 100% dedicado a Kali, la
alternativa reversible es correrlo como máquina virtual con VirtualBox
(imagen oficial ya lista en kali.org/get-kali, sección "Virtual Machines") —
mismo Kali, mismas herramientas, pero sin tocar el disco físico y pudiendo
borrarlo con solo eliminar la VM.
