# Cryptography — Play Nice

## Descripción
> **Prompt oficial del reto:** "Not all ancient ciphers were so bad... The flag is not in standard format."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** madStacks

## Solución
El reto implementa una variante del cifrado clásico **Playfair** sobre una cuadrícula de tamaño $6 \times 6$ (36 caracteres alfanuméricos), proporcionando el script `playfair.py`. Al conectarse al servicio, este entrega un alfabeto permutado de 36 caracteres y un mensaje cifrado, solicitando el mensaje en texto plano dentro de un límite de tiempo de 18 segundos.

### Reglas de cifrado y descifrado en Playfair ($6 \times 6$)
La cuadrícula $M$ de $6 \times 6$ se genera secuencialmente a partir del alfabeto entregado. El texto se procesa por pares de caracteres (dígrafos) $(c_1, c_2)$ con posiciones $(r_1, c_1)$ y $(r_2, c_2)$:

1. **Misma fila ($r_1 = r_2$):**
   - En cifrado: se desplazan una posición a la derecha: $(col + 1) \pmod 6$.
   - En descifrado: se desplazan una posición a la izquierda: $(col - 1) \pmod 6$.
2. **Misma columna ($c_1 = c_2$):**
   - En cifrado: se desplazan una posición hacia abajo: $(row + 1) \pmod 6$.
   - En descifrado: se desplazan una posición hacia arriba: $(row - 1) \pmod 6$.
3. **Distinta fila y columna (rectángulo):**
   - Se intercambian las columnas manteniendo las filas:
     $$p_1 = M[r_1][c_2], \quad p_2 = M[r_2][c_1]$$
   - Esta operación es simétrica y es idéntica en cifrado y descifrado.

### Script de resolución automatizada
```bash
python3 - << 'EOF'
import socket
import re

SQUARE_SIZE = 6

def generate_square(alphabet):
    matrix = []
    for i, letter in enumerate(alphabet):
        if i % SQUARE_SIZE == 0: matrix.append([])
        matrix[-1].append(letter)
    return matrix

def get_index(letter, matrix):
    for r in range(SQUARE_SIZE):
        for c in range(SQUARE_SIZE):
            if matrix[r][c] == letter:
                return (r, c)
    raise ValueError(f"letter {letter} not found")

def decrypt_pair(pair, matrix):
    p1 = get_index(pair[0], matrix)
    p2 = get_index(pair[1], matrix)
    if p1[0] == p2[0]:
        return matrix[p1[0]][(p1[1] - 1) % SQUARE_SIZE] + matrix[p2[0]][(p2[1] - 1) % SQUARE_SIZE]
    elif p1[1] == p2[1]:
        return matrix[(p1[0] - 1) % SQUARE_SIZE][p1[1]] + matrix[(p2[0] - 1) % SQUARE_SIZE][p2[1]]
    else:
        return matrix[p1[0]][p2[1]] + matrix[p2[0]][p1[1]]

def decrypt_string(s, matrix):
    res = ""
    for i in range(0, len(s), 2):
        res += decrypt_pair(s[i:i+2], matrix)
    return res

# Conexión al servicio interactivo
s = socket.create_connection(("chatelaine.cylabacademy.net", 17353))
data = s.recv(4096).decode()

alpha_m = re.search(r"Here is the alphabet: ([^\n\r]+)", data)
enc_m = re.search(r"Here is the encrypted message: ([^\n\r]+)", data)

alphabet = alpha_m.group(1).strip()
enc_msg = enc_m.group(1).strip()
matrix = generate_square(alphabet)
plain = decrypt_string(enc_msg, matrix)

s.sendall(f"{plain}\n".encode())
resp = s.recv(4096).decode()
s.close()

print(resp)
EOF
```

Al enviar la cadena descifrada, el servidor responde con la bandera (en formato no estándar, cadena hexadecimal de 32 caracteres): `00000000000000000000000000000000`.

## Notas adicionales
- El cifrado Playfair original usaba una matriz de $5 \times 5$ (25 letras, combinando 'I' y 'J'). La variante de $6 \times 6$ permite acomodar las 26 letras del abecedario inglés junto a los 10 dígitos decimales ('0'-'9'), evitando sustituciones de letras.

## Referencias
- Reto: https://learn.cylabacademy.org/library/114
- Apoyo: Wikipedia: Playfair cipher
