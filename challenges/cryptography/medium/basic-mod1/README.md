# basic-mod1

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2022  
**Plataforma:** CyLab Security Academy  

## Descripción

We found this weird message being passed around on the servers, we think we
have a working decryption scheme.
Download the message [here](https://challenge-files.cylabacademy.net/library/153c6663b971f4d124ad181fdbf1c21ad47dc241b7a578ab47253d6461f2f145/message.txt).

Take each number mod 37 and map it to the following character set: 0-25 is the
alphabet (uppercase), 26-35 are the decimal digits, and 36 is an underscore.

Wrap your decrypted message in the academy flag format
(i.e. `academy{decrypted_message}`)

## Hints

1. Do you know what `mod 37` means?
2. `mod 37` means modulo 37. It gives the remainder of a number after being divided by 37.

## Solución

El mensaje cifrado es una lista de números enteros. El esquema de descifrado es aritmética modular simple:

1. **Descargar el archivo** `message.txt` que contiene una secuencia de números enteros separados por espacios.

2. **Aplicar módulo 37** a cada número: `n % 37` produce un valor entre 0 y 36.

3. **Mapear al conjunto de caracteres**:
   - 0–25 → letras mayúsculas A–Z
   - 26–35 → dígitos 0–9
   - 36 → guión bajo `_`

4. **Concatenar los caracteres** resultantes y envolver en `academy{...}`.

```python
with open('message.txt') as f:
    numbers = list(map(int, f.read().split()))

charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
result = ''.join(charset[n % 37] for n in numbers)
print(f'academy{{{result}}}')
```

**Mensaje original:** `239 396 131 87 188 147 309 295 165 248 353 383 299 258 137 291 145 180 262 178 252 148`

**Resultado:** `R0UND_N_R0UND_0686D44A`

La frase hace referencia a la expresión "round and round" — probablemente aludiendo al movimiento circular de la aritmética modular.

## Referencias

- [Aritmética modular — Wikipedia](https://es.wikipedia.org/wiki/Aritm%C3%A9tica_modular)
- [picoCTF 2022](https://picoctf.org)
