# Ciberseguridad para curiosos: cómo funcionan los ataques y cómo defenderse

Este repositorio es un proyecto **educativo y defensivo**. El objetivo es entender,
a nivel conceptual y con demos seguras que corren en local, cómo funcionan las
técnicas de ataque más comunes, cómo las controlan quienes las usan, y sobre
todo **cómo prevenirlas y detectarlas**.

No es una colección de herramientas de ataque listas para usar contra terceros.
Ningún demo aquí se conecta a sistemas ajenos ni exfiltra datos: todo corre
contra `localhost` o contra datos de ejemplo incluidos en el propio repo.

> ⚠️ Usa este contenido solo en sistemas propios, entornos de laboratorio o con
> autorización explícita (por ejemplo, un pentest contratado o un CTF). Atacar
> sistemas de terceros sin permiso es ilegal en la mayoría de países.

## Estructura

- **`docs/`** — explicación de cada familia de ataques: qué es, cómo funciona
  técnicamente, cómo lo "controla" un atacante (C2, persistencia, etc.) y cómo
  detectarlo/prevenirlo desde el lado defensivo.
- **`demos/`** — ejemplos prácticos, pequeños y seguros, para ver los conceptos
  en acción sin poner en riesgo a nadie.

## Índice de documentación

1. [Phishing e ingeniería social](docs/01-phishing.md)
2. [Malware: virus, gusanos, troyanos, ransomware](docs/02-malware.md)
3. [Ataques de red: escaneo, MITM, DDoS](docs/03-network-attacks.md)
4. [Ataques a contraseñas](docs/04-password-attacks.md)
5. [Ataques web: XSS, SQLi, CSRF](docs/05-web-attacks.md)
6. [Ingeniería social en profundidad](docs/06-social-engineering.md)
7. [Command & Control (C2) y persistencia](docs/07-command-and-control.md)
8. [Defensa en profundidad: guía general de prevención](docs/08-defensas-generales.md)
9. [Instalar Kali Linux en el disco (laptop dedicado)](docs/09-instalar-kali.md)
10. [Anti-forense: cómo intentan no dejar rastro (y cómo se detecta igual)](docs/10-anti-forense-y-deteccion.md)
11. [Ataques a redes WiFi](docs/11-ataques-wifi.md)

## Demos incluidas

| Demo | Qué enseña | Cómo correrla |
|---|---|---|
| [`demos/phishing-awareness/`](demos/phishing-awareness/) | Cómo luce un login falso y qué señales lo delatan | Abrir `index.html` en el navegador |
| [`demos/password-security/`](demos/password-security/) | Por qué el hashing+salt importa, y qué tan rápido cae una contraseña débil | `python3 demos/password-security/demo.py` |
| [`demos/web-vulnerabilities/`](demos/web-vulnerabilities/) | SQL injection real (contra una BD SQLite local) vs. consultas parametrizadas | `python3 demos/web-vulnerabilities/sqli_demo.py` |
| [`demos/web-vulnerabilities/webapp/`](demos/web-vulnerabilities/webapp/) | XSS almacenado e IDOR reales en el navegador, vulnerable vs. corregido | `pip install flask && python3 demos/web-vulnerabilities/webapp/app.py` → abrir `http://127.0.0.1:5000/` |
| [`demos/network-recon/`](demos/network-recon/) | Cómo funciona un escaneo de puertos y qué ve un atacante | `python3 demos/network-recon/port_scanner.py` (por defecto solo escanea `localhost`) |

Cada demo tiene su propio `README`/comentarios explicando qué hace y qué mirar.
