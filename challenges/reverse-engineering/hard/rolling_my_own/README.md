# Reverse Engineering — Rolling My Own

## Descripción

> **Prompt oficial del reto:** "I don't trust password checkers made by other people, so I wrote my own. It doesn't even need to store the password! If you can crack it I'll give you a flag."
>
> **Pistas oficiales:**
> 1. It's based on [this paper](https://link.springer.com/article/10.1007%2Fs11416-006-0011-3)
> 2. Here's the start of the password: `D1v1`

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Challenge ID (CyLab):** 151

---

## Análisis Técnico

### 1. Mecanismo de Anti-Disassembly con Funciones Hash
El binario suministrado (`remote`) implementa una técnica de protección de software descrita en literatura académica sobre generación dinámica de código a través de funciones hash criptográficas (*"Software Authentication on Commodity Hardware via Dynamic Self-Modifying Code"*).

En lugar de almacenar una contraseña en texto plano, comparar hashes estáticos o incluir código de verificación directo, el programa:
1. Recibe una contraseña de 16 caracteres del usuario.
2. Divide la contraseña en 4 fragmentos de 4 caracteres cada uno ($p_0, p_1, p_2, p_3$).
3. Divide una cadena de salt constante (`GpLaMjEWpVOjnnmkRGiledp6Mvcezxls`) en 4 bloques de 8 caracteres ($s_0, s_1, s_2, s_3$).
4. Concatena cada fragmento de la contraseña con su bloque de salt correspondiente ($p_i + s_i$) y calcula su hash MD5.
5. Extrae 4 bytes específicos de cada hash generado para construir un búfer contiguo de 16 bytes.
6. Asigna una página de memoria ejecutable vía `mmap(..., PROT_READ | PROT_WRITE | PROT_EXEC, ...)`, copia los 16 bytes generados y los ejecuta como una función, pasando en `rdi` la dirección de la rutina de validación / impresión de la flag.

Si la contraseña es incorrecta, los bytes resultantes no forman instrucciones x86-64 válidas o no preservan el flujo de control, provocando que el programa termine con un fallo `Illegal instruction (core dumped)` o `Segmentation fault`.

### 2. Ensamblado del Shellcode Esperado
La pista inicial revela que los primeros 4 caracteres de la contraseña son `D1v1`.

Al calcular el hash MD5 del primer bloque:
$$\text{MD5}(\texttt{"D1v1GpLaMjEW"}) = \texttt{23f144e08b603e724889fe489f78fa53}$$

Los bytes extraídos correspondientes a este bloque forman los primeros 4 bytes del shellcode:
- `\x48\x89\xfe\x48` $\rightarrow$ `mov rsi, rdi` y prefijo `REX.W`.

Esto expone la convención del shellcode esperado de 16 bytes:
```asm
mov    rsi, rdi                     ; Salva el puntero de la función en rsi
movabs rdi, 0x000000037bdc26f1      ; Carga el argumento secreto en rdi
call   rsi                          ; Invoca la función interna de verificación
ret                                 ; Retorna
```

Al desensamblar la estructura completa, los 4 bloques de 4 bytes se ensamblan como:
- **Bloque 0 (`D1v1` + `GpLaMjEW`):** `48 89 fe 48`
- **Bloque 1 ($p_1$ + `pVOjnnmk`):** `bf f1 26 dc`
- **Bloque 2 ($p_2$ + `RGiledp6`):** `b3 07 00 00`
- **Bloque 3 ($p_3$ + `Mvcezxls`):** `00 ff d6 c3`

### 3. Recuperación de la Contraseña (Búsqueda por Segmentos)
Dado que cada fragmento de 4 caracteres es independiente y se verifica de manera aislada contra su rebanada de 4 bytes en el hash MD5, el espacio de búsqueda se reduce de $62^{16}$ combinaciones imposibles a 3 búsquedas independientes de $62^4 \approx 1.47 \times 10^7$ permutaciones, resolviéndose cada una en menos de 1 segundo:

1. **Segmento 1 ($p_1$):**
   - Salt: `pVOjnnmk`
   - Rebanada esperada: `bff126dc`
   - Resultado: `d3An`
2. **Segmento 2 ($p_2$):**
   - Salt: `RGiledp6`
   - Rebanada esperada: `b3070000`
   - Resultado: `dC0n`
3. **Segmento 3 ($p_3$):**
   - Salt: `Mvcezxls`
   - Rebanada esperada: `00ffd6c3`
   - Resultado: `qu3r`

Uniendo los 4 segmentos:
$$\texttt{"D1v1"} + \texttt{"d3An"} + \texttt{"dC0n"} + \texttt{"qu3r"} = \texttt{"D1v1d3AndC0nqu3r"}$$
(Frase mnemónica: *"Divide and Conquer"* en l33tspeak).

---

## Script de Solución

```python
#!/usr/bin/env python3
import hashlib
import itertools
import string
import socket
import re

# Definición de segmentos conocidos y valores objetivo
salt_segments = [
    ("pVOjnnmk", slice(4, 12), "bff126dc"),
    ("RGiledp6", slice(14, 22), "b3070000"),
    ("Mvcezxls", slice(2, 10), "00ffd6c3"),
]

password = "D1v1"
alphabet = string.ascii_letters + string.digits

print("[*] Derivando contraseña por segmentos...")
for idx, (salt, hash_slice, expected) in enumerate(salt_segments):
    for perm in itertools.permutations(alphabet, 4):
        cand = "".join(perm)
        h = hashlib.md5((cand + salt).encode()).hexdigest()
        if h[hash_slice] == expected:
            password += cand
            print(f"[+] Segmento #{idx+1} encontrado: {cand}")
            break

print(f"[+] Contraseña completa: {password}")
```

Al enviar `D1v1d3AndC0nqu3r` al servicio remoto:
```bash
$ nc <host> <port>
Password: D1v1d3AndC0nqu3r
academy{...}
```

---

## Flag

```text
academy{...}
```

## Referencias
- *Software Authentication on Commodity Hardware via Dynamic Self-Modifying Code*: https://link.springer.com/article/10.1007%2Fs11416-006-0011-3
- CyLab Challenge 151: https://learn.cylabacademy.org/library/151
