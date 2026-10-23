# rotation

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2023  
**Plataforma:** CyLab Security Academy  

## Descripción

You will find the flag after decrypting this file.  
Download the encrypted flag [here](https://challenge-files.cylabacademy.net/library/0ef23aae5f4b057bc3ecd26dea457bdc0eb3657ede271ab91f6b026f4305b52b/encrypted.txt).

## Hints

1. Sometimes rotation is right

## Solución

El archivo `encrypted.txt` contiene: `ikilmug{z0bib1wv_l3kzgxb3l_i4008m11}`

El prefijo `ikilmug` corresponde al formato de flag `academy`, lo que permite determinar el desplazamiento de rotación. Comparando letra a letra:

- `a` → `i`: desplazamiento de 8
- `c` → `k`: desplazamiento de 8
- `a` → `i`: desplazamiento de 8
- ...

El cifrado de rotación (una generalización del ROT13) desplaza las letras del alfabeto 8 posiciones hacia adelante. Para descifrar se resta 8 posiciones (equivalente a sumar 18 módulo 26).

```python
def rot_decrypt(text, shift):
    result = []
    for c in text:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result.append(chr((ord(c) - base - shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

cipher = 'ikilmug{z0bib1wv_l3kzgxb3l_i4008m11}'
# Buscar el desplazamiento que convierta el prefijo en 'academy'
for shift in range(26):
    prefix_dec = rot_decrypt('ikilmug', shift)
    if prefix_dec == 'academy':
        print(f'Shift: {shift}')
        inner = rot_decrypt('z0bib1wv_l3kzgxb3l_i4008m11', shift)
        print(f'Flag: academy{{{inner}}}')
```

Con desplazamiento **8** el texto interior `z0bib1wv_l3kzgxb3l_i4008m11` se convierte en `r0tat1on_d3crypt3d_a4008e11`.

Los caracteres no alfabéticos (dígitos y guiones bajos) no se modifican.

La flag completa es: `academy{r0tat1on_d3crypt3d_a4008e11}`

## Referencias

- [ROT cipher - Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
- [CyberChef ROT13 Brute Force](https://gchq.github.io/CyberChef/)
