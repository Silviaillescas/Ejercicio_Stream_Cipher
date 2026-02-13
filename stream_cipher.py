import hashlib

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

if __name__ == "__main__":
    ks1 = generar_keystream("clave123", 16)
    ks2 = generar_keystream("clave123", 16)
    ks3 = generar_keystream("otra_clave", 16)
    ks4 = generar_keystream("clave123", 5)


    print("Keystream 1:", ks1.hex())
    print("Keystream 2:", ks2.hex())
    print("Misma clave produce lo mismo:", ks1 == ks2)
    print("Clave distinta produce distinto:", ks1 != ks3)
    print("Longitud 5 bytes:", len(ks4), ks4.hex())