#!/usr/bin/env python3
"""
Demo educativa: por qué el algoritmo de hashing importa.

Compara cuánto tarda un ataque de diccionario contra:
  1. SHA-256 sin salt (rápido de calcular -> vulnerable)
  2. bcrypt (deliberadamente lento -> resistente)

Todo corre 100% en local contra datos de ejemplo. No se conecta a ningún
sistema ni contraseña real de terceros.

Uso:
    python3 demo.py
    (si no tienes bcrypt instalado: pip install bcrypt)
"""
import hashlib
import time
import itertools
import string

# Diccionario de ejemplo: contraseñas comunes (dominio público, muy conocidas)
COMMON_PASSWORDS = [
    "123456", "password", "123456789", "qwerty", "abc123",
    "111111", "letmein", "monkey", "dragon", "iloveyou",
    "admin", "welcome", "hunter2", "trustno1", "correcto123",
]

TARGET_PASSWORD = "hunter2"  # la "víctima" de este demo, elegida a propósito


def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def crack_sha256(target_hash: str, wordlist):
    start = time.perf_counter()
    attempts = 0
    for candidate in wordlist:
        attempts += 1
        if sha256_hash(candidate) == target_hash:
            elapsed = time.perf_counter() - start
            return candidate, attempts, elapsed
    return None, attempts, time.perf_counter() - start


def crack_bcrypt(target_hash: bytes, wordlist):
    import bcrypt
    start = time.perf_counter()
    attempts = 0
    for candidate in wordlist:
        attempts += 1
        if bcrypt.checkpw(candidate.encode(), target_hash):
            elapsed = time.perf_counter() - start
            return candidate, attempts, elapsed
    return None, attempts, time.perf_counter() - start


def main():
    print("=" * 70)
    print("DEMO: ataque de diccionario contra distintos algoritmos de hash")
    print("=" * 70)
    print(f"\nContraseña 'víctima' (elegida para este demo): {TARGET_PASSWORD!r}")
    print(f"Diccionario de prueba: {len(COMMON_PASSWORDS)} contraseñas comunes\n")

    # --- SHA-256 sin salt ---
    sha_hash = sha256_hash(TARGET_PASSWORD)
    print(f"Hash SHA-256 (sin salt): {sha_hash}")
    found, attempts, elapsed = crack_sha256(sha_hash, COMMON_PASSWORDS)
    print(f"-> Encontrada: {found!r} en {attempts} intentos, {elapsed*1000:.3f} ms\n")

    # SHA-256 real permite cientos de millones de hashes/segundo con GPU:
    # con 10 caracteres alfanuméricos, un atacante con hardware dedicado
    # puede llegar a probar todo el espacio en horas/días, no años.
    hashes_per_sec_gpu = 5_000_000_000  # orden de magnitud típico para SHA-256 con GPUs
    keyspace = len(string.ascii_letters + string.digits) ** 8  # 8 caracteres alfanuméricos
    seconds = keyspace / hashes_per_sec_gpu
    print(f"Referencia: fuerza bruta de 8 caracteres alfanuméricos contra SHA-256")
    print(f"sin salt, con una GPU moderna (~{hashes_per_sec_gpu:,} hashes/s):")
    print(f"  tiempo estimado ≈ {seconds/3600:.2f} horas para cubrir todo el espacio\n")

    # --- bcrypt ---
    try:
        import bcrypt
    except ImportError:
        print("(bcrypt no está instalado — instala con 'pip install bcrypt' para ver la comparación)")
        return

    bcrypt_hash = bcrypt.hashpw(TARGET_PASSWORD.encode(), bcrypt.gensalt(rounds=12))
    print(f"Hash bcrypt (con salt, cost=12): {bcrypt_hash.decode()}")
    found, attempts, elapsed = crack_bcrypt(bcrypt_hash, COMMON_PASSWORDS)
    print(f"-> Encontrada: {found!r} en {attempts} intentos, {elapsed*1000:.1f} ms")
    print(f"   (bcrypt hace ~{attempts/elapsed:.0f} intentos/seg en esta máquina,")
    print(f"    frente a millones/seg de SHA-256 sin salt -> ataques de diccionario")
    print(f"    y fuerza bruta se vuelven muchísimo más caros)\n")

    print("Conclusión: el diccionario encuentra la contraseña igual de rápido")
    print("en NÚMERO DE INTENTOS en ambos casos (porque la contraseña es débil),")
    print("pero el COSTO por intento con bcrypt hace que atacar millones de")
    print("hashes robados sea inviable en la práctica. Ver docs/04-password-attacks.md")


if __name__ == "__main__":
    main()
