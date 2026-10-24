# Reverse Engineering — FactCheck

## Descripción
> **Prompt oficial del reto:** "This binary is putting together some important piece of information... Can you uncover that information? Examine this file. Do you understand its inner workings?"
>
> **Pistas oficiales:**
> (Ninguna pista proporcionada en la plataforma)

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** Junias Bonou

## Solución
El reto proporciona un binario ELF x86-64 compilado en C++ (`bin`). Al ejecutarlo directamente no produce ninguna salida en consola ni solicita datos por entrada estándar.

### 1. Análisis de cadenas y rodata
Al inspeccionar las cadenas presentes en la sección `.rodata`:

```bash
strings -a bin | grep academy
```

Se encuentra el prefijo inicial de la bandera y una serie de caracteres individuales almacenados (`2`, `5`, `4`, `3`, `a`, `c`, `e`, `d`, `b`, `1`, `6`, `9`, `8`).

### 2. Desensamblado de la función `main`
Al desensamblar `main` con `objdump`:

```bash
objdump -d bin | grep -A 100 "<main>:"
```

Se identifica la creación de múltiples objetos `std::string` a partir de estos caracteres individuales, seguidos por una serie de verificaciones condicionales que determinan cuáles caracteres se anexan al objeto de la bandera:

1. **Condición 1:** Compara el valor del carácter `'5'` (ASCII 53) con `0x41` ('A' = 65). Dado que $53 \le 65$, se cumple la condición y se añade `'1'`.
2. **Condición 2:** Compara el valor del carácter `'6'` (ASCII 54) con `0x41`. Dado que $54 \ne 65$, se cumple la condición y se añade `'9'`.
3. **Condición 3:** Evalúa la diferencia entre los caracteres `'3'` (51) y `'e'` (101). Como $51 - 101 = -50 \ne 3$, la condición no se cumple y se salta este bloque.
4. **Anexos incondicionales:** Se agregan `'4'` y `'c'`.
5. **Condición 4:** Evalúa si el carácter `'a'` es igual a `'G'`. Como no coinciden, se omite.
6. **Anexos finales:** Se anexan incondicionalmente `'a'`, `'1'`, `'2'`, `'5'`, y finalmente el carácter de cierre `}` (`0x7d`).

Reuniendo las partes en orden de concatenación de los bloques válidos se reconstruye la bandera en formato `academy{...}`.

## Notas adicionales
- Al compilar código C++ con `std::string`, los métodos `basic_string::append` y los constructores generan un flujo de control estructurado que puede reconstruirse estáticamente o analizarse de forma dinámica mediante un punto de interrupción en GDB justo antes de la destrucción de las variables locales.

## Referencias
- Reto: https://learn.cylabacademy.org/library/416
- GCC C++ std::string documentation: https://gcc.gnu.org/onlinedocs/libstdc++/manual/strings.html
