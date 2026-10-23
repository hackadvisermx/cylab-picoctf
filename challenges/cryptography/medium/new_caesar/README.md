# New Caesar

| Campo       | Valor                  |
|-------------|------------------------|
| Categoría   | Cryptography           |
| Dificultad  | Medium                 |
| Origen      | picoCTF 2021           |
| Puntos      | 60                     |

## Descripción

> We found a brand new type of encryption, can you break the secret code? (Wrap around the end of the alphabet!)

El reto entrega dos archivos: `new_caesar.py` con el algoritmo de cifrado y `ciphertext` con el texto cifrado. El objetivo es revertir el cifrado y recuperar la flag.

Texto cifrado:
```
kjlijdliljhdjdhfkfkhhjkkhhkihlhnhghekfhmhjhkhfhekfkkkjkghghjhlhghmhhhfkikfkfhm
```

## Hints oficiales

1. *"Do you know what a base 16 (hexadecimal) encoding looks like?"*
2. *"Do you know what a caesar cipher is?"*

## Solución

### Análisis del algoritmo de cifrado

El script `new_caesar.py` aplica dos transformaciones en cadena:

**Paso 1 — Codificación base 16 propia (`b16_encode`)**

Se define un alfabeto reducido de 16 letras: `ALPHABET = 'abcdefghijklmnop'`.

Para cada carácter del texto plano:
1. Se obtiene su valor ASCII en binario de 8 bits (por ejemplo, `'p'` → `01110000`).
2. Se divide en dos nibbles de 4 bits: `0111` y `0000`.
3. Cada nibble se convierte a un entero (0–15) y se mapea a la letra correspondiente del alfabeto de 16.
4. El resultado son dos letras por cada carácter original → la cadena cifrada duplica su longitud.

**Paso 2 — Cifrado César con clave de un carácter (`shift`)**

Se extrae la clave `key = flag[7]`, es decir, el octavo carácter de la flag. Dado que la flag empieza con `picoCTF{`, ese carácter es el primero del contenido secreto. La clave pertenece forzosamente al alfabeto de 16 letras (`'a'`–`'p'`), porque el reto garantiza que la flag es ASCII imprimible y la codificación base 16 propia sólo produce esas letras.

El desplazamiento César es circular módulo 16:
```
enc_char = ALPHABET[(ord(plain_char) - ord('a') + ord(key) - ord('a')) % 16]
```

### Vulnerabilidad: espacio de claves trivial

La clave es un único carácter elegido de un alfabeto de **16 letras**. El espacio de búsqueda tiene exactamente **16 posibilidades**, lo que permite un ataque de fuerza bruta instantáneo. Para cada clave candidata se invierte el César y luego la codificación base 16, y se comprueba si el resultado empieza con `picoCTF{` o `academy{`.

### Pasos del descifrado

1. **Invertir el César**: para cada carácter del ciphertext, restar el desplazamiento de la clave candidata (módulo 16).
2. **Invertir la codificación base 16**: tomar los caracteres de dos en dos, convertir cada uno a su índice en el alfabeto de 16, concatenar los dos nibbles de 4 bits y convertir el byte resultante a carácter ASCII.
3. **Verificar**: comprobar si el texto descifrado empieza por `picoCTF{` o `academy{`.

## Script de descifrado

```python
import string

ALPHABET = string.ascii_lowercase[:16]  # 'abcdefghijklmnop'
ciphertext = "kjlijdliljhdjdhfkfkhhjkkhhkihlhnhghekfhmhjhkhfhekfkkkjkghghjhlhghmhhhfkikfkfhm"

def b16_decode(enc):
    """Invierte la codificación base-16 propia del reto."""
    plain = ''
    for i in range(0, len(enc), 2):
        c1 = ALPHABET.index(enc[i])
        c2 = ALPHABET.index(enc[i + 1])
        binary = bin(c1)[2:].zfill(4) + bin(c2)[2:].zfill(4)
        plain += chr(int(binary, 2))
    return plain

def unshift(c, k):
    """Invierte el desplazamiento César módulo 16."""
    t1 = ord(c) - ord('a')
    t2 = ord(k) - ord('a')
    return ALPHABET[(t1 - t2) % len(ALPHABET)]

# Fuerza bruta sobre las 16 claves posibles
for key in ALPHABET:
    unshifted = ''.join(unshift(c, key) for c in ciphertext)
    try:
        decoded = b16_decode(unshifted)
        if decoded.startswith('picoCTF') or decoded.startswith('academy'):
            print(f"Clave encontrada: '{key}'")
            print(f"Flag: {decoded}")
    except Exception:
        pass  # Algunos candidatos generan caracteres no imprimibles; se ignoran
```

Ejecutar:
```bash
python3 solve.py
```

La única clave que produce una cadena con prefijo `picoCTF{` revela la flag.

## Notas adicionales

- El nombre "New Caesar" hace referencia a que es una variante del cifrado César clásico, pero restringida a un alfabeto de 16 letras en lugar de 26.
- La codificación `b16_encode` del script no es base-16 estándar (hexadecimal); utiliza letras en lugar de dígitos `0–9a–f`, lo que puede despistar en un primer análisis.
- El hint 1 orienta a identificar que el ciphertext está compuesto exclusivamente por letras `a`–`p`, sugiriendo una representación de nibbles (4 bits).
- El hint 2 orienta al desplazamiento César aplicado a continuación.
- La clave de un solo carácter es la debilidad principal: un cifrado César con clave de un byte y alfabeto de 16 ofrece sólo 16 combinaciones posibles.

## Referencias

- Reto disponible en picoCTF Practice: https://play.picoctf.org/practice/challenge/56
- Cifrado César: https://en.wikipedia.org/wiki/Caesar_cipher
- Representación en nibbles (base 16): https://en.wikipedia.org/wiki/Nibble
