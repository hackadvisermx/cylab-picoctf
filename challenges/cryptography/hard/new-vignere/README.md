# Cryptography — New Vignere

## Descripción
> **Prompt oficial del reto:** "Another slight twist on a classic, see if you can recover the flag. (Wrap with academy{}) new_vignere.py emfakcakmklfajnnlpekfpkndlmildnmnnljenfckbalpglfnknaonebfcnodkpe"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** madStacks

## Solución

Al analizar el script `new_vignere.py`:
1. El texto original `flag` está compuesto únicamente por caracteres hexadecimales en minúsculas: `0123456789abcdef`.
2. La función `b16_encode` transforma cada byte en dos caracteres del alfabeto restringido `ALPHABET = "abcdefghijklmnop"` (los primeros 16 caracteres ASCII):
   - Primer nibble (bits más significativos): `ALPHABET[int(binary[:4], 2)]`.
   - Segundo nibble (bits menos significativos): `ALPHABET[int(binary[4:], 2)]`.
3. Cada carácter par $2k$ proviene del nibble superior del código ASCII de un dígito hexadecimal:
   - Para dígitos ASCII `'0'` a `'9'` (`0x30` a `0x39` $\rightarrow$ binario `0011 xxxx`): el primer nibble es `3` $\rightarrow$ `'d'`.
   - Para letras ASCII `'a'` a `'f'` (`0x61` a `0x66` $\rightarrow$ binario `0110 xxxx`): el primer nibble es `6` $\rightarrow$ `'g'`.
   - Por tanto, **el carácter en toda posición par de `b16` es obligatoriamente `'d'` o `'g'`**.
4. La clave secreta `key` tiene una longitud menor a 15 caracteres (`len(key) < 15`) y solo usa letras de `ALPHABET`.
5. El cifrado aplica un desplazamiento tipo Vigenère módulo 16:
   $$c_i = (b16_i + \text{key}_{i \bmod L}) \bmod 16$$

### Criptoanálisis por Fuerza Bruta de Clave Restringida
Dado que la longitud de clave $L \in [1, 14]$ y cada posición de la clave debe producir únicamente los caracteres `'d'` o `'g'` al descifrar las posiciones pares correspondientes:
1. Para cada longitud posible $L \in \{1, \dots, 14\}$ y para cada posición $0 \le j < L$, filtramos los candidatos de `key[j]` probando los 16 caracteres de `ALPHABET`.
2. Las restricciones reducen el espacio de búsqueda a una única clave válida de longitud 9: `bickhknij`.
3. Con dicha clave, se invierte el desplazamiento Vigenère y se decodifica Base16 para recuperar la cadena hexadecimal de la bandera.
4. Se envuelve el resultado en el formato `academy{...}`.

```bash
python3 - << 'EOF'
import string

enc = "emfakcakmklfajnnlpekfpkndlmildnmnnljenfckbalpglfnknaonebfcnodkpe"
LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

valid_pairs = {}
for c in "abcdef0123456789":
    b = "{0:08b}".format(ord(c))
    p1 = ALPHABET[int(b[:4], 2)]
    p2 = ALPHABET[int(b[4:], 2)]
    valid_pairs[(p1, p2)] = c

def unshift(c, k):
    t1 = ord(c) - LOWERCASE_OFFSET
    t2 = ord(k) - LOWERCASE_OFFSET
    return ALPHABET[(t1 - t2) % len(ALPHABET)]

for key_len in range(1, 15):
    cand_sets = []
    for ki in range(key_len):
        possible_k = []
        for k in ALPHABET:
            ok = True
            for j in range(ki, len(enc), key_len):
                if j % 2 == 0 and unshift(enc[j], k) not in ('d', 'g'):
                    ok = False
                    break
            if ok:
                possible_k.append(k)
        cand_sets.append(possible_k)
    
    total = 1
    for s in cand_sets: total *= len(s)
    if 0 < total < 10000:
        import itertools
        for key_tuple in itertools.product(*cand_sets):
            key = ''.join(key_tuple)
            b16 = [unshift(enc[j], key[j % key_len]) for j in range(len(enc))]
            flag_chars = []
            valid = True
            for idx in range(0, len(b16), 2):
                pair = (b16[idx], b16[idx+1])
                if pair not in valid_pairs:
                    valid = False
                    break
                flag_chars.append(valid_pairs[pair])
            if valid:
                print(f"academy{{{''.join(flag_chars)}}}")
                break
EOF
```

## Notas adicionales
- La drástica reducción del espacio de búsqueda se debe a la baja entropía del conjunto de caracteres de entrada (alfabeto hexadecimal) y la linealidad de la transformación Base16.
- Flag en formato: `academy{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/148
- Apoyo: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher#Cryptanalysis
