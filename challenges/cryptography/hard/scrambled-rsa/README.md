# Cryptography — Scrambled: RSA

## Descripción
> **Prompt oficial del reto:** "Hmmm I wonder if you have learned your lesson... Let's see if you understand RSA and how the encryption works."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** Sara

## Solución

Al interactuar con el servicio remoto, se observa que:
1. El servidor entrega el texto cifrado de la bandera (un entero decimal extenso de más de 8000 dígitos), el módulo RSA $n$ de 1024 bits y el exponente público $e = 65537$.
2. El servicio ofrece un oráculo interactivo que cifra cualquier cadena provista por el usuario.
3. Al cifrar cadenas de texto, la longitud del texto cifrado crece de forma estrictamente proporcional a la cantidad de caracteres de entrada (aproximadamente 308 dígitos por carácter, que corresponde a un bloque de 1024 bits).
4. El servicio cifra cada carácter de forma independiente (dependiendo de su posición/prefijo) y concatena los bloques resultantes en orden permutado/desordenado (scrambled).

### Vulnerabilidad y Estrategia de Ataque (Oráculo de Texto Claro Escogido)
Dado que el cifrado de un prefijo $P = c_0 c_1 \dots c_{k-1}$ genera exactamente los bloques $\{S_0, S_1, \dots, S_{k-1}\}$, al solicitar el cifrado de $P + c$ se generan los mismos bloques del prefijo más un bloque nuevo $S_k$ correspondiente al carácter $c$ en la posición $k$.

Podemos aislar el bloque $S_k$ removiendo una a una las representaciones de los bloques ya conocidos del prefijo:
$$S_k = \text{encrypt}(P + c) \setminus \{S_0, S_1, \dots, S_{k-1}\}$$

Si el bloque aislado $S_k$ (de $\approx 308$ dígitos) está contenido en el texto cifrado de la bandera `flag_ct`, entonces $c$ es el carácter correcto en dicha posición. Al confirmarse el carácter:
- Se añade $c$ a la bandera recuperada.
- Se añade $S_k$ a la lista de bloques del prefijo.
- Se remueve $S_k$ del texto cifrado de la bandera (`flag_ct = flag_ct.replace(S_k, '', 1)`) para evitar solapamientos y falsos positivos.

Iniciando desde el prefijo conocido `academy{` y probando iterativamente el conjunto de caracteres imprimibles hasta encontrar la llave de cierre `}`, se reconstruye la bandera completa.

```bash
python3 - << 'EOF'
import socket, re, string

host = "chatelaine.cylabacademy.net"
port = 10837

s = socket.create_connection((host, port), timeout=25)

def recvuntil(s, delim):
    buf = b''
    while delim not in buf:
        c = s.recv(1)
        if not c: break
        buf += c
    return buf

banner = recvuntil(s, b'I will encrypt whatever you give me: ').decode()
flag_ct = ''
for l in banner.split('\n'):
    if l.startswith('flag:'):
        flag_ct = l.split('flag:')[1].strip()

def encrypt(txt):
    s.sendall(txt.encode() + b'\n')
    ans = recvuntil(s, b'\n').decode().strip().replace('Here you go: ', '')
    recvuntil(s, b'I will encrypt whatever you give me: ')
    return ans

prefix_segments = []
flag = ''
known = 'academy{'

for c in known:
    res = encrypt(flag + c)
    temp = res
    for seg in prefix_segments:
        temp = temp.replace(seg, '', 1)
    flag += c
    prefix_segments.append(temp)
    flag_ct = flag_ct.replace(temp, '', 1)

charset = string.digits + string.ascii_lowercase + '_}'

while not flag.endswith('}'):
    for c in charset:
        res = encrypt(flag + c)
        temp = res
        for seg in prefix_segments:
            temp = temp.replace(seg, '', 1)
        if len(temp) in (307, 308, 309) and (temp in flag_ct):
            flag += c
            prefix_segments.append(temp)
            flag_ct = flag_ct.replace(temp, '', 1)
            break

print(flag)
s.close()
EOF
```

## Notas adicionales
- Este vector de ataque aprovecha la ausencia de esquemas de autenticación y difusión probabilística como RSA-OAEP, donde una modificación mínima en cualquier byte del mensaje altera completamente el bloque cifrado entero.
- Flag en formato: `academy{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/107
- Apoyo: https://en.wikipedia.org/wiki/Chosen-plaintext_attack
