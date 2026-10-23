# Cryptography — Easy1

## Descripción

> **Prompt oficial del reto:** "The one time pad can be cryptographically secure, but not when you know the key. Can you solve this?
> We've given you the encrypted flag, key, and a table to help `UFJKXQZQUNB` with the key of `SOLVECRYPTO`. Can you use this table to solve it?."

> **Hints:**
> 1. Submit your answer in our flag format. For example, if your answer was 'hello', you would submit 'academy{HELLO}' as the flag.
> 2. Please use all caps for the message.

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Alex Fulton/Danny

## Solución

El reto presenta un archivo `table.txt` que corresponde a una *Tabula Recta* o tabla de Vigenère. Se proporcionan:
- Texto cifrado: `UFJKXQZQUNB`
- Clave: `SOLVECRYPTO`

Dado que la longitud de la clave coincide exactamente con la longitud del texto cifrado, opera como una libreta de un solo uso (*One-Time Pad*) con el alfabeto inglés.

### Descifrado

Para cada par de caracteres $(c_i, k_i)$:
$$p_i = (c_i - k_i) \bmod 26$$

| $c_i$ | $k_i$ | $c_i - k_i \pmod{26}$ | Letra descifrada |
|---|---|---|---|
| U (20) | S (18) | 2 | **C** |
| F (5) | O (14) | -9 ≡ 17 | **R** |
| J (9) | L (11) | -2 ≡ 24 | **Y** |
| K (10) | V (21) | -11 ≡ 15 | **P** |
| X (23) | E (4) | 19 | **T** |
| Q (16) | C (2) | 14 | **O** |
| Z (25) | R (17) | 8 | **I** |
| Q (16) | Y (24) | -8 ≡ 18 | **S** |
| U (20) | P (15) | 5 | **F** |
| N (13) | T (19) | -6 ≡ 20 | **U** |
| B (1) | O (14) | -13 ≡ 13 | **N** |

El texto descifrado es `CRYPTOISFUN`.

### Script de resolución

```python
c = "UFJKXQZQUNB"
k = "SOLVECRYPTO"

plain = "".join(chr(ord("A") + (ord(ci) - ord(ki)) % 26) for ci, ki in zip(c, k))
print(f"academy{{{plain}}}")
```

## Referencias

- [Vigenère Cipher — Wikipedia](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
- [Tabula Recta — Wikipedia](https://en.wikipedia.org/wiki/Tabula_recta)
