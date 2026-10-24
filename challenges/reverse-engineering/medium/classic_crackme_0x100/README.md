# Reverse Engineering — Classic Crackme 0x100

## Descripción
> **Prompt oficial del reto:** "A classic Crackme. Find the password, get the flag! Binary can be downloaded here. Crack the Binary file locally and recover the password. Use the same password on the server to get the flag!"
>
> **Pistas oficiales:**
> 1. Let the machine figure out the symbols!

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** Nandan Desai

## Solución
El reto entrega un binario ejecutable x86-64 (`crackme100`) y permite desplegar una instancia remota interactiva accesible por `nc`. El objetivo es encontrar la contraseña correcta que valida el binario y enviarla al servidor para recibir la bandera.

### 1. Análisis de la función `main`
Al desensamblar `crackme100` con `objdump`:

```bash
objdump -d crackme100 | grep -A 80 "<main>:"
```

Se observa la inicialización de un arreglo objetivo de 50 caracteres en la pila (`[rbp - 0x80]`), cuya cadena cifrada corresponde a:
`zpwyduihqzxrxbkdapjnnoftgyocsqrxyxqrhaqxywoespqfit`

Luego, el programa lee la contraseña mediante `scanf("%50s", input)` y ejecuta dos bucles anidados:
- **Bucle externo:** Se ejecuta exactamente 3 veces (`i` de 0 a 2).
- **Bucle interno:** Itera sobre cada posición `j` desde 0 hasta la longitud de la cadena.

Dentro del bucle interno se implementa una rutina de conteo de bits activados (*popcount*) sobre `j % 255`:
```c
uVar1 = (((j % 255) >> 1) & 0x55) + ((j % 255) & 0x55);
uVar1 = ((uVar1 >> 2) & 0x33) + (uVar1 & 0x33);
popcount = ((uVar1 >> 4) & 0x0f) + (uVar1 & 0x0f);
input[j] = ((input[j] - 'a' + popcount) % 26) + 'a';
```

Al cabo de las 3 iteraciones, cada carácter se desplaza:
$$\text{target}[j] = ((\text{input}[j] - 'a' + 3 \cdot \text{popcount}(j \pmod{255})) \pmod{26}) + 'a'$$

### 2. Inversión del algoritmo
Para recuperar la contraseña original a partir del texto cifrado, se despeja la operación aplicando el desplazamiento inverso:
$$\text{input}[j] = ((\text{target}[j] - 'a' - 3 \cdot \text{popcount}(j \pmod{255})) \pmod{26}) + 'a'$$

Script de resolución en Python:

```python
target = 'zpwyduihqzxrxbkdapjnnoftgyocsqrxyxqrhaqxywoespqfit'

def popcount(x):
    return bin(x).count('1')

password = []
for j, c in enumerate(target):
    shift = 3 * popcount(j % 255)
    orig = ((ord(c) - ord('a') - shift) % 26) + ord('a')
    password.append(chr(orig))

print('Contraseña:', ''.join(password))
```

### 3. Obtención de la bandera
Conectándose a la instancia remota y proporcionando la contraseña calculada:

```bash
nc <host> <puerto>
Enter the secret password: <password>
SUCCESS! Here is your flag: academy{...}
```

## Notas adicionales
- La rutina de conteo de bits de Hamming (`0x55`, `0x33`, `0x0f`) es la implementación clásica sin instrucciones vectoriales ni la instrucción dedicada `popcnt` de x86.

## Referencias
- Reto: https://learn.cylabacademy.org/library/409
- Hamming weight algorithms: https://en.wikipedia.org/wiki/Hamming_weight
