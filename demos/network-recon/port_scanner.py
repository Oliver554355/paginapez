#!/usr/bin/env python3
"""
Demo educativa: escáner de puertos TCP básico.

Por defecto SOLO escanea 'localhost' (tu propia máquina), para que puedas
ver cómo funciona un escaneo sin apuntar a ningún sistema ajeno.

Si quieres escanear otro host, hazlo ÚNICAMENTE contra sistemas de tu
propiedad o con autorización explícita por escrito (ver docs/08-defensas-generales.md).
Escanear sistemas de terceros sin permiso puede ser ilegal.

Uso:
    python3 port_scanner.py                  # escanea localhost, puertos comunes
    python3 port_scanner.py --host 127.0.0.1 --ports 1-1024
    python3 port_scanner.py --host <IP_PROPIA_AUTORIZADA> --ports 1-1024 --i-have-authorization
"""
import argparse
import socket
import sys
import time

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-alt", 8443: "HTTPS-alt",
}

LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


def parse_ports(spec: str):
    if "-" in spec:
        start, end = spec.split("-", 1)
        return range(int(start), int(end) + 1)
    return [int(spec)]


def scan_port(host, port, timeout=0.3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        return result == 0
    except socket.error:
        return False
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description="Escáner de puertos TCP educativo")
    parser.add_argument("--host", default="localhost", help="host a escanear (por defecto: localhost)")
    parser.add_argument("--ports", default=",".join(str(p) for p in COMMON_PORTS),
                         help="puerto único, rango 'inicio-fin', o lista separada por comas")
    parser.add_argument("--i-have-authorization", action="store_true",
                         help="confirma que tienes autorización explícita para escanear un host que no es localhost")
    args = parser.parse_args()

    if args.host not in LOCAL_HOSTS and not args.i_have_authorization:
        print(f"ERROR: '{args.host}' no es localhost.")
        print("Este demo solo escanea hosts ajenos si confirmas autorización explícita:")
        print(f"  añade --i-have-authorization  (solo si el host es tuyo o tienes permiso por escrito)")
        sys.exit(1)

    if "," in args.ports:
        ports = [int(p) for p in args.ports.split(",")]
    else:
        ports = list(parse_ports(args.ports))

    print(f"Escaneando {args.host} — {len(ports)} puerto(s)...\n")
    start = time.perf_counter()
    open_ports = []

    for port in ports:
        if scan_port(args.host, port):
            service = COMMON_PORTS.get(port, "?")
            open_ports.append((port, service))
            print(f"  [ABIERTO] puerto {port:<6} ({service})")

    elapsed = time.perf_counter() - start
    print(f"\nEscaneo completado en {elapsed:.2f}s. {len(open_ports)} puerto(s) abierto(s) de {len(ports)} probado(s).")

    if open_ports:
        print("\nQué vería un atacante aquí: cada puerto abierto es un servicio")
        print("potencialmente atacable. Ver docs/03-network-attacks.md para cómo")
        print("se defiende esto (firewall default-deny, no exponer admin a Internet, etc).")


if __name__ == "__main__":
    main()
