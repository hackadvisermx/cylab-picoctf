# Transposition Trial

| Campo       | Valor                  |
|-------------|------------------------|
| Categoría   | Cryptography           |
| Dificultad  | Medium                 |
| Origen      | picoCTF 2022           |
| CyLab ID    | 312                    |

## Descripción

> Our data got corrupted on the way here. Luckily, nothing got replaced, but every block of 3 got scrambled around! The first word seems to be three letters long, maybe you can use that to recover the rest of the message.

El reto entrega un archivo `message.txt` con texto cifrado mediante un **cifrado de transposición por bloques de 3**. Los caracteres no se reemplazan (a diferencia de los cifrados de sustitución), sino que se reordenan dentro de cada bloque con una permutación fija. La pista es que la primera palabra tiene 3 letras.

Texto cifrado:
```
heTfl g as icaaemd{7y4NRP051N5_16_35P3X51N3_V7F2D46C}5
```

## Hints oficiales

1. *"Split the message up into blocks of 3 and see how the first block is scrambled"*

## Solución

### Análisis del cifrado

El mensaje se divide en bloques de exactamente 3 caracteres. En cada bloque, los caracteres se reordenan con la **misma permutación** desconocida. Existen únicamente 3! = 6 permutaciones posibles de 3 elementos: (0,1,2), (0,2,1), (1,0,2), (1,2,0), (2,0,1), (2,1,0).

El primer bloque del ciphertext es `"heT"`. El reto indica que la primera palabra tiene 3 letras; la palabra inglesa más probable de 3 letras al inicio de un mensaje es `"The"`. Por lo tanto:

```
cifrado[0] = 'h' = plain[1]   →  la posición 0 del bloque cifrado fue la posición 1 del original
cifrado[1] = 'e' = plain[2]   →  la posición 1 del bloque cifrado fue la posición 2 del original
cifrado[2] = 'T' = plain[0]   →  la posición 2 del bloque cifrado fue la posición 0 del original
```

Para **descifrar** (invertir la transposición) se aplica la permutación **(2, 0, 1)** a cada bloque:
```
plain[0] = cifrado[2]
plain[1] = cifrado[0]
plain[2] = cifrado[1]
```

Verificación: `"heT"` → `'T'+'h'+'e'` = `"The"` ✓

### Pasos de la solución

1. Leer el archivo `message.txt`.
2. Dividir el texto en bloques de 3 caracteres.
3. Aplicar fuerza bruta sobre las 6 permutaciones posibles (o deducir directamente la permutación a partir del primer bloque).
4. La permutación **(2, 0, 1)** produce el único resultado legible.
5. Extraer la flag del texto descifrado.

### Script de descifrado

```python
from itertools import permutations

# Texto cifrado del reto
message = "heTfl g as icaaemd{7y4NRP051N5_16_35P3X51N3_V7F2D46C}5"

# Dividir en bloques de 3 caracteres
blocks = [message[i:i+3] for i in range(0, len(message), 3)]
print(f"Bloques: {blocks}")

# Probar las 6 permutaciones posibles
for perm in permutations([0, 1, 2]):
    result = []
    for block in blocks:
        if len(block) == 3:
            new_block = block[perm[0]] + block[perm[1]] + block[perm[2]]
            result.append(new_block)
        else:
            result.append(block)
    decoded = ''.join(result)
    print(f"Permutación {perm}: {decoded}")
```

Resultado al ejecutar:
```
Bloques: ['heT', 'fl ', 'g a', 's i', 'caa', 'emd', '{7y', '4NR', 'P05', '1N5', '_16', '_35', 'P3X', '51N', '3_V', '7F2', 'D46', 'C}5']

Permutación (0, 1, 2): heTfl g as icaaemd{7y4NRP051N5_16_35P3X51N3_V7F2D46C}5
Permutación (0, 2, 1): hTef lga si caaedm{y74RNP5015N_61_53PX35N13V_72FD64C5}
Permutación (1, 0, 2): ehTlf  ga siacamed7{yN4R0P5N151_63_53PX15N_3VF724D6}C5
Permutación (1, 2, 0): eThl f ag isaacmde7y{NR405PN5116_35_3XP1N5_V3F2746D}5C
Permutación (2, 0, 1): The flag is academy{7R4N5P051N6_15_3XP3N51V3_27F6D45C}
Permutación (2, 1, 0): Teh lfa gi saacdmey7{RN450P5N161_53_X3PN15V_32F764D5}C
```

La única permutación que produce texto legible en inglés con una flag válida es **(2, 0, 1)**.

## Notas adicionales

- El cifrado de transposición es una técnica clásica donde el **orden** de los caracteres cambia pero ningún carácter se reemplaza; todos los caracteres del cifrado aparecen en el texto plano, solo en posiciones diferentes.
- Con bloques de 3 elementos, el espacio de claves es trivial: solo 6 permutaciones posibles (3! = 6). Un ataque de fuerza bruta basta.
- La pista de "la primera palabra tiene 3 letras" es clave: reduce inmediatamente la búsqueda a comparar `"heT"` con `"The"`, revelando la permutación sin necesidad de probar las 6 opciones.
- El contenido de la flag (`7R4N5P051N6_15_3XP3N51V3_27F6D45C`) en leetspeak se lee aproximadamente como `TRANSPOSING IS EXPENSIVE`, lo cual es una referencia al nombre del reto.
- La longitud del mensaje (54 caracteres) es múltiplo exacto de 3, lo que confirma que todos los bloques están completos.

## Referencias

- Reto en CyLab Academy: https://learn.cylabacademy.org/library/312
- Cifrado de transposición: https://en.wikipedia.org/wiki/Transposition_cipher
- Permutaciones: https://en.wikipedia.org/wiki/Permutation
