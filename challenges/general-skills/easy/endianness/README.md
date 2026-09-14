# General Skills — endianness

## Descripción
> **Prompt oficial:** "Know of little and big endian?" (código fuente C descargable, `nc <host> <puerto>`)

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Nana Ama Atombo-Sackey

## Solución
El servicio (código fuente `flag.c` adjunto) genera una palabra aleatoria de 5 letras y pide, uno tras otro, su representación en **little endian** y **big endian** en hexadecimal (cada carácter como byte, mayúsculas):

- **Big endian**: los bytes en el mismo orden que el texto.
- **Little endian**: los bytes en orden inverso.

```python
word = "amkpk"   # ejemplo recibido del servidor
big    = ''.join(f"{ord(c):02X}" for c in word)              # 616D6B706B
little = ''.join(f"{ord(c):02X}" for c in reversed(word))    # 6B706B6D61
```

Automatizado con un socket Python: se lee la palabra del banner ("Word: xxxxx"), se calculan ambas representaciones y se envían en el orden que pide el programa (primero little endian, luego big endian).

Flag: `picoCTF{3ndi4n_sw4p_su33ess_25c5f083}`

## Notas adicionales
- El propio código fuente deja ver el orden exacto en que hay que responder (`find_little_endian` se pide primero, `find_big_endian` después) y que la comparación se hace en mayúsculas (`toupper`).
- Reto puramente de comprensión de "endianness" a nivel de bytes de texto ASCII, sin manipulación de binarios ni ingeniería inversa real.

## Referencias
- Reto: https://learn.cylabacademy.org/library/414
- Fuente: `flag.c` (copia en esta carpeta)
