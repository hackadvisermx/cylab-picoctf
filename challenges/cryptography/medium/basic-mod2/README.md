# basic-mod2

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2022  
**Plataforma:** CyLab Security Academy  

## Descripción

A new modular challenge!
Download the message [here](https://challenge-files.cylabacademy.net/library/79ab2df83c3efdaa68f8d1d7b4ce3e478bd49e8193ca7002a30ea460743c412c/message.txt).

Take each number mod 41 and find the modular inverse for the result. Then map
to the following character set: 1-26 are the alphabet, 27-36 are the decimal
digits, and 37 is an underscore.

Wrap your decrypted message in the academy flag format
(i.e. `academy{decrypted_message}`)

## Hints

1. Do you know what the modular inverse is?
2. The inverse modulo *z* of *x* is the number, *y* that when multiplied by *x* is 1 modulo *z*
3. It's recommended to use a tool to find the modular inverse

## Solución

Este reto extiende basic-mod1 añadiendo un paso de **inverso modular**. El proceso es:

1. **Descargar `message.txt`** con la secuencia de números.

2. **Aplicar módulo 41** a cada número: `n % 41`.

3. **Calcular el inverso modular** del resultado respecto a 41.  
   El inverso modular de `x` módulo `m` es el valor `y` tal que `x * y ≡ 1 (mod m)`.  
   En Python 3.8+ se puede calcular como `pow(x, -1, m)`.

4. **Mapear al conjunto de caracteres**:
   - 1–26 → letras mayúsculas A–Z
   - 27–36 → dígitos 0–9
   - 37 → guión bajo `_`

5. **Concatenar y envolver** en `academy{...}`.

```python
with open('message.txt') as f:
    numbers = list(map(int, f.read().split()))

def get_char(val):
    if 1 <= val <= 26:
        return chr(ord('A') + val - 1)
    elif 27 <= val <= 36:
        return str(val - 27)
    elif val == 37:
        return '_'
    return '?'

result = ''
for n in numbers:
    rem = n % 41
    inv = pow(rem, -1, 41)   # inverso modular
    result += get_char(inv)

print(f'academy{{{result}}}')
```

**Mensaje original:** `309 44 274 149 57 378 313 311 64 420 405 86 98 195 256 48 238 277 448 411 240 436 214`

**Resultado:** `1NV3R53LY_H4RD_FED0A735`

La frase juega con "inversely hard" — aludiendo al inverso modular que hay que aplicar para descifrar.

## Referencias

- [Inverso modular — Wikipedia](https://es.wikipedia.org/wiki/Inverso_multiplicativo_modular)
- [pow() con exponente negativo en Python 3.8+](https://docs.python.org/3/library/functions.html#pow)
- [picoCTF 2022](https://picoctf.org)
