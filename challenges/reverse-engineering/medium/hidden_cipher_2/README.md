# Reverse Engineering — Hidden Cipher 2

## Descripción
> **Prompt oficial del reto:** "The flag is right in front of you... kind of. You just need to solve a basic math problem to see it. But to get the real flag, you’ll have to understand how that math answer is used.
> You can download the program files [here](https://challenge-files.cylabacademy.net/library/25615a6b0204fa43517181f2a03a400cf1fc1f6106d9ff7f27ddc248bc7448dc/hiddencipher2.zip)."
>
> **Pistas oficiales:**
> 1. Focus on what the program does with your correct answer. Is it reused later?
> 2. Disassembling or decompiling tools (Ghidra, IDA) can help reveal the exact transformation on the flag.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
El archivo adjunto `hiddencipher2.zip` contiene un binario ELF x86-64 `hiddencipher2` y un archivo `flag.txt` con contenido de prueba (`academy{fake_flag}`). El servicio interactivo real se ejecuta en red tras iniciar la instancia on-demand (`nc <host> <puerto>`).

### 1. Análisis del binario
Al desensamblar `hiddencipher2` con `objdump -d -M intel`, se observan las funciones:
- `generate_math_question`: Genera dos números aleatorios $A$ y $B$, e imprime `What is A + B? `.
- `read_flag_file`: Carga el contenido de `flag.txt` en memoria.
- `encode_flag`: Aplica una transformación sobre la flag usando la respuesta correcta de la suma:

```assembly
1520: add  rax, rdx
1523: movzx eax, byte ptr [rax]    ; byte de la flag: flag[i]
1526: movsx eax, al
1529: imul eax, dword ptr [rbp - 0x1c] ; imul por la respuesta matemática
152d: mov  esi, eax
1536: mov  rdi, rax                ; "%d"
153e: call printf
```

El algoritmo de codificación multiplica el código ASCII de cada carácter de la flag por el resultado de la suma ($ans = A + B$) y emite la lista de enteros separados por comas:
$$C_i = \text{flag}[i] \times ans$$

### 2. Recuperación de la flag
Para revertir el cifrado, basta con resolver la suma, recibir los enteros devueltos por el servidor y dividir cada valor entre $ans$:
$$\text{flag}[i] = \frac{C_i}{ans}$$

### 3. Automatización en Python

```python
import socket, re

s = socket.create_connection(('<host>', <puerto>))
data = s.recv(1024).decode()

m = re.search(r'What is (\d+)\s*\+\s*(\d+)\?', data)
if m:
    a, b = int(m.group(1)), int(m.group(2))
    ans = a + b
    s.sendall(f'{ans}\n'.encode())
    
    resp = s.recv(4096).decode()
    nums = [int(x) for x in re.findall(r'\d+', resp)]
    flag = bytes([x // ans for x in nums if x % ans == 0])
    print("Flag:", flag.decode('ascii'))
```

Salida del programa:
```text
Prompt: What is 7 + 1? 
Encoded flag values:
776, 792, 776, 800, 808, 872, 968, 984, 872, 416, 928, 832, 760, 784, 408, 832, 392, 880, 800, 760, 792, 392, 896, 832, 408, 912, 760, 800, 448, 400, 392, 448, 448, 432, 816, 1000

Flag: academy{...}
```

## Notas adicionales
- Dado que la operación aritmética es una multiplicación entera con un escalar positivo y sin módulo, la inversión es exacta e inequívoca mediante división entera.

## Referencias
- Reto: https://learn.cylabacademy.org/library/751
