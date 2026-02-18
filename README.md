# Ejercicio_Stream_Cipher
Silvia Illescas #22376


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
