# Reverse Engineering — Bbbbloat

## Descripción
> **Prompt oficial del reto:** "Can you get the flag?
> Reverse engineer this [binary](https://challenge-files.cylabacademy.net/library/797bac900bf1cc3c89e751bd6e171896ab95b4527c97f9a7879276bba5661f80/bbbbloat)."
>
> **Pistas oficiales:** Ninguna

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El binario provisto (`bbbbloat`) es un ejecutable ELF de 64 bits para Linux, despojado de símbolos (`stripped`). Al ejecutarlo, muestra:

```text
What's my favorite number?
```

Si ingresamos un número incorrecto, muestra `"Sorry, that's not it!"` y finaliza.

### Desensamblado y Análisis Estático

Utilizando `objdump -d -M intel bbbbloat`:

1. **Código inflado (*bloatware*):** La función principal contiene múltiples bloques de instrucciones aritméticas redundantes (`add`, `sub`, `shl`, `imul 0x55555556`) diseñadas para ofuscar el flujo y dificultar la lectura manual o el análisis simbólico superficial.
2. **Comparación clave:** Tras leer la entrada con `scanf` o `fgets`, el programa compara el valor numérico ingresado en `[rbp - 0x40]` contra una constante hexadecimal en la dirección `0x14cb`:
   ```assembly
   mov eax, dword ptr [rbp - 0x40]
   cmp eax, 0x86187
   jne 0x1581
   ```
   El valor `0x86187` equivale a `549255` en base decimal.
3. **Rutina de descifrado:** Si la comparación es exitosa, se cargan 32 bytes estáticos almacenados en la pila (cargados en `[rbp - 0x30]` mediante instrucciones `movabs` de 64 bits) y se invoca la función en `0x1249`.
4. **Algoritmo ROT47:** Al analizar la función en `0x1249`:
   - Itera por cada carácter del búfer.
   - Si el carácter está en el rango ASCII imprimible (`0x21` a `0x7e`), le suma `0x2f` (47).
   - Si sobrepasa `0x7e`, le resta `0x5e` (94).
   - Esta operación corresponde exactamente a la codificación/decodificación de **ROT47**.

### Script de resolución

Podemos emular la reconstrucción de los bytes y la decodificación ROT47 en Python:

```python
import struct

# Constantes cargadas en la pila en 0x1329 - 0x135d
b1 = struct.pack('<Q', 0x4c4a3e3635323432)
b2 = struct.pack('<Q', 0x3062396630664634)
b3 = struct.pack('<Q', 0x65353066635f3d33)
b4 = struct.pack('<Q', 0x4e666532653766)

raw = (b1 + b2 + b3 + b4).split(b'\x00')[0].decode('latin1')

def rot47(s):
    res = []
    for c in s:
        code = ord(c)
        if 33 <= code <= 126:
            res.append(chr(33 + ((code + 14) % 94)))
        else:
            res.append(c)
    return ''.join(res)

flag = rot47(raw)
print("Flag:", flag)
```

Al ejecutar el script de resolución:

```bash
python3 solve.py
```

Se obtiene la bandera en formato `academy{...}`. Alternativamente, ejecutar `./bbbbloat` e ingresar `549255` imprime la misma bandera directamente.

## Notas adicionales
El nombre del reto ("Bbbbloat") alude a las secuencias de código muerto (*dead code insertion*) utilizadas habitualmente en empaquetadores y técnicas antiforense para distraer analistas e inflar el grafo de flujo de control (CFG).

## Referencias
- Reto: https://learn.cylabacademy.org/library/255
- Apoyo: https://en.wikipedia.org/wiki/ROT47
