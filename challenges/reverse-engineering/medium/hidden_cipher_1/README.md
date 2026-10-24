# Reverse Engineering — Hidden Cipher 1

## Descripción
> **Prompt oficial del reto:** "The flag is right in front of you; just slightly encrypted. All you have to do is figure out the cipher and the key.
> You can download the program files [here](https://challenge-files.cylabacademy.net/library/cc69caef03ead47c4a0e948fc8a62790818f0be172498c427c6582acde9c00d0/hiddencipher.zip)."
>
> **Pistas oficiales:**
> 1. The binary can be unpacked using a tool that's often pre-installed on Linux
> 2. The program hides a secret. Look at how it's defined and used.
> 3. Think XOR. What happens when you XOR something twice with the same key?

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
El archivo descargable `hiddencipher.zip` contiene un ejecutable `hiddencipher` y un archivo `flag.txt` de prueba. 

### 1. Desempaquetado con UPX
Al inspeccionar `hiddencipher` con `strings` o herramientas de análisis de cabeceras, se detectan firmas de UPX (`UPX!`). Se procede a desempaquetar el binario:

```bash
upx -d -o hiddencipher_unpacked hiddencipher
```

### 2. Análisis del binario desempacado
Al examinar las funciones del binario desempacado con `objdump -d -M intel`:
1. **Función `get_secret`:**
   Construye la clave secreta caracter por caracter en memoria:
   ```assembly
   mov byte ptr [rip + ...], 0x53   ; 'S'
   mov byte ptr [rip + ...], 0x33   ; '3'
   mov byte ptr [rip + ...], 0x43   ; 'C'
   mov byte ptr [rip + ...], 0x72   ; 'r'
   mov byte ptr [rip + ...], 0x33   ; '3'
   mov byte ptr [rip + ...], 0x74   ; 't'
   ```
   La clave resultante es `S3Cr3t` (longitud 6).

2. **Función `main`:**
   Abre el archivo `flag.txt`, lee su contenido y en un bucle aplica una operación XOR entre cada byte de la bandera y la clave repetida:
   ```assembly
   movzx esi, byte ptr [rax]       ; flag[i]
   ...                             ; rdx = i % 6
   movzx eax, byte ptr [rax + rdx] ; key[i % 6]
   xor   eax, esi                  ; flag[i] ^ key[i % 6]
   call  printf                    ; imprime en formato hexadecimal "%02x"
   ```

### 3. Conexión remota y descifrado
Al conectarse a la instancia remota (`nc <host> <puerto>`), el servidor imprime la bandera cifrada en formato hexadecimal. Dado que el cifrado es XOR simétrico ($C \oplus K = P$):

```python
import socket

s = socket.create_connection(('<host>', <puerto>))
data = s.recv(4096).decode().strip()
hex_str = data.split('\n')[-1].strip()

key = b'S3Cr3t'
ciphertext = bytes.fromhex(hex_str)
flag = bytes([c ^ key[i % len(key)] for i, c in enumerate(ciphertext)])
print("Flag:", flag.decode('ascii'))
```

Salida del programa:
```text
Here your encrypted flag:
3250221656192a483b1d412b265d3313501f0c072d135f0d2002302d07463756721005112e

Flag: academy{...}
```

## Notas adicionales
- Al ser XOR un operador involutivo, el descifrado utiliza el mismo algoritmo y clave que el cifrado original.

## Referencias
- Reto: https://learn.cylabacademy.org/library/745
- UPX (Ultimate Packer for eXecutables): https://upx.github.io/
