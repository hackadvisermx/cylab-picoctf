# Reverse Engineering — Secure Password Database

## Descripción
> **Prompt oficial del reto:** "I made a new password authentication program that even shows you the password you entered saved in the database! Isn't that cool?
> system.out"
>
> **Pistas oficiales:**
> 1. How does the hashing algorithm work?

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Philip Thayer

## Solución
El binario proporcionado (`system.out`) es un ejecutable ELF x86-64 no *stripped*. Al examinar su flujo con `objdump` o desensambladores, se identifican las funciones principales `main`, `make_secret` y `hash`.

### 1. Análisis de `hash` y `make_secret`

La función `hash` implementa el algoritmo clásico **djb2**:
- Inicializa el acumulador con `0x1505` (5381).
- Para cada byte $c$ de la cadena, calcula: `hash = ((hash << 5) + hash) + c` (es decir, `hash * 33 + c`), operando en 64 bits.

La función `make_secret`:
- Lee un arreglo global ofuscado de bytes ubicado en la sección `.rodata` en la dirección `0x2008` (`obf_bytes`):
  `c3 ff c8 c2 92 9b 8b c0 80 c2 c4 8b 00`
- Realiza una operación XOR byte a byte con `0xaa` (`xor eax, -0x56`):
  ```python
  raw = bytes.fromhex("c3ffc8c2929b8bc080c2c48b")
  secret = bytes([b ^ 0xaa for b in raw])
  # Resultado: b'iUbh81!j*hn!'
  ```
- Finaliza la cadena con un byte nulo en el índice 12 y calcula `hash(secret)`.

### 2. Cálculo del hash esperado

Al computar el hash djb2 de la cadena secreta desofuscada `iUbh81!j*hn!`:

```python
h = 5381
for b in b"iUbh81!j*hn!":
    h = (((h << 5) + h) + b) & 0xFFFFFFFFFFFFFFFF

# Representación como entero con signo de 64 bits (usado por strtoll en el binario)
signed_hash = h if h < (1 << 63) else h - (1 << 64)
print(signed_hash)  # -3209081493549540382
```

### 3. Explotación remota

En la función `main`, el programa pide:
1. Una contraseña arbitraria.
2. La longitud en bytes a inspeccionar (vulnerabilidad tipo *heartbleed* donde si se solicitan más bytes de los ingresados se filtra memoria interna del proceso).
3. "Enter your hash to access your account!", leyendo la entrada con `strtol`/`strtoll`. Si el número coincide exactamente con el valor devuelto por `make_secret`, se abre `flag.txt` y se imprime la flag.

```bash
printf "test\n10\n-3209081493549540382\n" | nc <host> <puerto>
```

Salida del programa:
```text
Please set a password for your account:
How many bytes in length is your password?
You entered: 10
Your successfully stored password:
116 101 115 116 10 0 0 0 0 0 0 
Enter your hash to access your account!
academy{...}
```

## Notas adicionales
- El binario compara el valor numérico devuelto por `strtol(..., 10)` contra el hash de 64 bits. Dado que el resultado de djb2 excede `LONG_MAX` (`0x7fffffffffffffff`), ingresarlo como un entero positivo sin signo hace que `strtol` devuelva saturación `LONG_MAX` por desbordamiento (`ERANGE`). Ingresarlo como su representación con signo en complemento a dos (`-3209081493549540382`) pasa la validación directamente.

## Referencias
- Reto: https://learn.cylabacademy.org/library/767
- djb2 Hash Function: http://www.cse.yorku.ca/~oz/hash.html
