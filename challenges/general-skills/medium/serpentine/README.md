# General Skills — Serpentine

## Descripción
> **Prompt oficial del reto:** "Find the flag in the Python script!" — se entrega un script `serpentine.py` para descargar, sin instancia remota.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
El script simula un "encourager" interactivo con opciones `a) Print encouragement`, `b) Print flag`, `c) Quit` — pero la opción `b` está deshabilitada a propósito:

```python
elif choice == 'b':
    print('\nOops! I must have misplaced the print_flag function! Check my source code!\n\n')
```

No hace falta ejecutar el programa: la función `print_flag()` sigue estando definida en el código, solo que nunca se llama desde el menú. Usa una variable `flag_enc` (la flag cifrada byte a byte con `chr(0x..)`) y una función `str_xor(secret, key)` que aplica XOR repitiendo la clave `'enkidu'` cíclicamente hasta cubrir la longitud del secreto — es decir, un **XOR de clave repetida (cifrado Vigenère-como)**.

Basta con reproducir esa misma operación localmente en vez de ejecutar el script real:

```python
exec(open('serpentine.py').read().split('def main()')[0])  # carga str_xor y flag_enc
print(str_xor(flag_enc, 'enkidu'))
# picoCTF{7h3_r04d_l355_7r4v3l3d_8e47d128}
```

## Notas adicionales
- Reto puramente de "leer el código fuente" (no de ejecución/explotación): la lógica de descifrado y la clave ya están completas en el archivo entregado, solo hay que invocarlas manualmente ya que el propio programa nunca llama a `print_flag()`.
- El XOR con clave repetida es simétrico: la misma función `str_xor` que "cifra" (aplicada sobre texto plano y clave) también "descifra" (aplicada sobre el cifrado y la misma clave), porque XOR es su propia inversa.

## Referencias
- Reto: https://learn.cylabacademy.org/library/251
