# Reverse Engineering — Keygenme

## Descripción
> **Prompt oficial del reto:** "Can you get the flag? Reverse engineer this binary."
>
> **Pistas oficiales:**
> 1. (Sin pistas adicionales proporcionadas)

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto suministra un binario ELF de 64 bits para x86-64 denominado `keygenme`. El programa solicita una clave de licencia de 36 caracteres y valida cada posición de la entrada contra un búfer generado dinámicamente mediante funciones de hash criptográfico MD5.

### 1. Análisis del flujo de validación
Al desensamblar la función de verificación (dirección `0x1209`):

1. **Longitud requerida:**
   - Se invoca `strlen` sobre la entrada del usuario y se verifica que coincida exactamente con `0x24` (36 caracteres en decimal):
     ```assembly
     call strlen
     cmp  rax, 0x24
     jne  fail
     ```
2. **Fragmentos estáticos iniciales:**
   - La primera parte de la clave (27 caracteres) se construye en la pila:
     `academy{br1ng_y0ur_0wn_k3y_`
   - El último carácter (posición 35) se define como la llave de cierre `}`.
3. **Cálculo de hashes MD5:**
   - Se calcula el hash MD5 de la cadena inicial:
     $$H_1 = \text{MD5}(\text{"academy\{br1ng\_y0ur\_0wn\_k3y\_"})$$
   - Se calcula el hash MD5 del carácter de cierre:
     $$H_2 = \text{MD5}(\text{"\}"})$$
   - Ambos hashes de 16 bytes se formatean a cadenas hexadecimales de 32 caracteres en minúsculas.
4. **Construcción del sufijo dinámico:**
   - Los 8 caracteres intermedios (posiciones 27 a 34) se seleccionan de índices específicos de $H_1$ y $H_2$:
     - Carácter 27: $H_1[22]$
     - Carácter 28: $H_1[21]$
     - Carácter 29: $H_1[22]$
     - Carácter 30: $H_1[3]$
     - Carácter 31: $H_2[13]$
     - Carácter 32: $H_1[8]$
     - Carácter 33: $H_1[13]$
     - Carácter 34: $H_1[9]$
5. **Comparación final:**
   - Se compara la entrada del usuario carácter por carácter con el búfer compuesto (`academy{br1ng_y0ur_0wn_k3y_` + 8 caracteres dinámicos + `}`).

### 2. Script de resolución en Python

```python
import hashlib

prefix = b"academy{br1ng_y0ur_0wn_k3y_"
suffix = b"}"

h1 = hashlib.md5(prefix).hexdigest()
h2 = hashlib.md5(suffix).hexdigest()

dynamic_part = (
    h1[22]
    + h1[21]
    + h1[22]
    + h1[3]
    + h2[13]
    + h1[8]
    + h1[13]
    + h1[9]
)

full_flag = prefix.decode() + dynamic_part + "}"
print("Flag:", "academy{...}")
```

## Notas adicionales
- En la versión original de picoCTF 2022, el prefijo utilizado era `picoCTF{br1ng_y0ur_0wn_k3y_`. La plataforma CyLab adaptó el binario al prefijo canónico `academy{br1ng_y0ur_0wn_k3y_`, lo que altera los hashes MD5 intermedios pero mantiene intacta la lógica de indexación y verificación.

## Referencias
- Reto: https://learn.cylabacademy.org/library/276
- Documentación hashlib (Python): https://docs.python.org/3/library/hashlib.html
