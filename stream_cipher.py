import hashlib
from typing import Union


def _seed_to_uint32(seed: str) -> int:
    """
    Convierte la clave en un número entero de 32 bits.

    Como la clave es un texto, primero se transforma usando SHA-256
    para obtener un valor binario fijo. Luego se toman solo los primeros
    4 bytes para trabajar con un entero de 32 bits.
    """
    hash_bytes = hashlib.sha256(seed.encode()).digest()
    return int.from_bytes(hash_bytes[:4], "big")


def generar_keystream(seed: str, longitud: int) -> bytes:
    """
    Genera un keystream pseudoaleatorio usando un generador lineal congruencial.

    La misma clave siempre producirá exactamente el mismo keystream.

    Parámetros:
        seed: clave que inicializa el generador
        longitud: cantidad de bytes que se desean generar

    Retorna:
        Secuencia de bytes pseudoaleatorios
    """

    if longitud < 0:
        raise ValueError("La longitud debe ser un número positivo.")

    # Parámetros del generador LCG (mod 2^32)
    a = 1664525
    c = 1013904223
    modulo = 2**32

    # Inicia el estado interno usando la clave
    estado = _seed_to_uint32(seed)

    keystream = bytearray()

    for _ in range(longitud):
        # Fórmula del LCG
        estado = (a * estado + c) % modulo

        # Extrae un byte del estado
        byte_generado = (estado >> 24) & 0xFF
        keystream.append(byte_generado)

    return bytes(keystream)

def _xor_bytes(data: bytes, keystream: bytes) -> bytes:
    """
    Hace XOR byte a byte entre data y keystream.
    """
    if len(keystream) < len(data):
        raise ValueError("El keystream debe ser al menos del mismo tamaño que el mensaje.")
    return bytes(d ^ k for d, k in zip(data, keystream))


def cifrar(mensaje: Union[str, bytes], seed: str) -> bytes:
    """
    Cifra un mensaje usando XOR con un keystream generado desde la seed.

    - Si el mensaje viene como str, se convierte a bytes con UTF-8.
    - Devuelve el ciphertext como bytes.
    """
    if isinstance(mensaje, str):
        mensaje_bytes = mensaje.encode("utf-8")
    else:
        mensaje_bytes = mensaje

    ks = generar_keystream(seed, len(mensaje_bytes))
    return _xor_bytes(mensaje_bytes, ks)


def descifrar(ciphertext: bytes, seed: str) -> bytes:
    """
    Descifra aplicando el mismo XOR con el mismo keystream.
    (En XOR, cifrar y descifrar es la misma operación.)
    """
    ks = generar_keystream(seed, len(ciphertext))
    return _xor_bytes(ciphertext, ks)


if __name__ == "__main__":
    ks1 = generar_keystream("clave123", 16)
    ks2 = generar_keystream("clave123", 16)
    ks3 = generar_keystream("otra_clave", 16)

    print("Keystream 1:", ks1.hex())
    print("Keystream 2:", ks2.hex())
    print("Misma clave produce lo mismo:", ks1 == ks2)
    print("Clave distinta produce distinto:", ks1 != ks3)

    ks4 = generar_keystream("clave123", 5)
    print("Longitud 5 bytes:", len(ks4), ks4.hex())

    # --- Prueba 1.2 y 1.3 (cifrar/descifrar) ---
    mensaje = "Hola hola"
    seed = "clave123"

    ciphertext = cifrar(mensaje, seed)
    plaintext_recuperado = descifrar(ciphertext, seed).decode("utf-8")

    print("\nMensaje original:", mensaje)
    print("Ciphertext (hex):", ciphertext.hex())
    print("Descifrado:", plaintext_recuperado)
    print("¿Se recupera el original?:", plaintext_recuperado == mensaje)

    intento_malo = descifrar(ciphertext, "otra_clave")
    try:
        intento_malo_texto = intento_malo.decode("utf-8")
    except UnicodeDecodeError:
        intento_malo_texto = "<bytes no válidos en UTF-8>"

    print("\nDescifrado con clave incorrecta:", intento_malo_texto)
