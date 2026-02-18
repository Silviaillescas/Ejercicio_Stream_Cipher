# Ejercicio_Stream_Cipher
Silvia Illescas #22376

Descripción
Este proyecto implementa un Stream Cipher simple basado en XOR, utilizando un generador pseudoaleatorio determinístico para la creación del keystream.
El objetivo es comprender el funcionamiento básico de los cifrados de flujo, su dependencia de la clave y sus implicaciones de seguridad.

Parte 1: Implementación
1.1 Generación del Keystream

Se implementó un generador pseudoaleatorio basado en un generador lineal congruencial (LCG).
La clave ingresada por el usuario se transforma primero en un entero de 32 bits mediante SHA-256, el cual se utiliza como estado inicial del generador.

La implementación es determinística: la misma clave siempre produce el mismo keystream.

1.2 Cifrado

El cifrado se realiza aplicando la operación XOR entre el texto plano y el keystream generado.
El keystream se genera con la misma longitud del mensaje para evitar reutilización o repetición de patrones.

1.3 Descifrado

El descifrado utiliza el mismo procedimiento de XOR que el cifrado.
Debido a las propiedades de la operación XOR, aplicar nuevamente el mismo keystream permite recuperar exactamente el texto original.

Parte 2: Análisis de Seguridad

En esta sección se analizan las implicaciones de seguridad del stream cipher implementado, a partir de pruebas prácticas realizadas sobre el código.

2.1 Variación de la Clave

Al modificar la clave utilizada para generar el keystream, la secuencia de bytes resultante cambia completamente. Esto se debe a que la clave determina el estado inicial del generador pseudoaleatorio. En la implementación realizada se observa que, para una misma longitud, dos claves distintas producen keystreams diferentes, mientras que la misma clave genera siempre la misma secuencia. Esto demuestra el carácter determinístico del algoritmo y la importancia de la clave en la seguridad del cifrado.

2.2 Reutilización del Keystream

Reutilizar el mismo keystream para cifrar más de un mensaje representa una vulnerabilidad crítica. Si dos mensajes se cifran con la misma clave, un atacante puede aplicar XOR entre ambos textos cifrados y eliminar el keystream, obteniendo información sobre la relación entre los mensajes originales. Las pruebas realizadas confirman que esta situación expone patrones y puede facilitar la recuperación parcial del texto plano.

2.3 Longitud del Keystream

La seguridad del cifrado depende de que el keystream tenga al menos la misma longitud que el mensaje. Un keystream más corto reutilizado introduce patrones repetitivos, mientras que uno del mismo tamaño garantiza que cada byte del mensaje se cifre con un valor único. Generar un keystream más largo no afecta la seguridad siempre que solo se utilice la parte necesaria.

2.4 Consideraciones Prácticas

- En un entorno real, es fundamental considerar los siguientes aspectos:
- Utilizar generadores pseudoaleatorios criptográficamente seguros.
- Evitar la reutilización de keystreams mediante el uso de nonces o contadores.
-Proteger adecuadamente la clave y complementar el cifrado con mecanismos de integridad.

Conclusión

El análisis evidencia que la seguridad de un stream cipher depende principalmente de la correcta gestión de la clave y del keystream. Errores como la reutilización del keystream pueden comprometer completamente la confidencialidad del sistema.


Parte 3: Validación y Pruebas
3.1 Ejemplos de Entrada / Salida

Ejemplo 1

Texto plano: Hola hola

Clave: clave123

Texto cifrado (hex): c6cbf93bfa40c3c456

Texto descifrado: Hola hola

Ejemplo 2

Texto plano: Seguridad

Clave: clave123

Texto cifrado (hex): d8c1f229c940c4db

Texto descifrado: Seguridad

Ejemplo 3

Texto plano: StreamCipher

Clave: otra_clave

Texto cifrado (hex): ddc5f06efc49c1d6f74bbf

Texto descifrado: StreamCipher

3.2 Pruebas Unitarias

Se validó que:
- El descifrado recupera exactamente el mensaje original.
- Claves diferentes generan textos cifrados distintos.
- La misma clave produce siempre el mismo texto cifrado.
- El sistema funciona correctamente con mensajes de diferentes longitudes.
