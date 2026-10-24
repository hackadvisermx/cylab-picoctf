# Cryptography — XtraORdinary

## Descripción
> **Prompt oficial del reto:** "Check out my new, never-before-seen method of encryption! I totally invented it myself. I added so many for loops that I don't even know what it does. It's extraordinarily secure!"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoMini by redpwn
- **Autor:** Boolean

## Solución

Al inspeccionar el script `encrypt.py`:
1. El texto original `flag` se cifra inicialmente mediante XOR repetido con una clave secreta desconocida `key`:
   $$c_0 = \text{flag} \oplus \text{key}$$
2. Posteriormente, se ejecutan bucles anidados con rangos aleatorios (`randint`) que aplican XOR repetidamente con cadenas tomadas de una lista `random_strs`.

### Análisis de Paridad XOR
La operación XOR es involutiva, asociativa y conmutativa:
$$A \oplus B \oplus B = A$$
Cualquier cadena aplicada un número par de veces se anula por completo ($0$ veces), y si se aplica un número impar de veces, equivale a haberla aplicado exactamente $1$ vez.

Revisando `random_strs`, existen únicamente 5 cadenas distintas (las repeticiones consecutivas de `b'ever'` se agrupan en su paridad total):
- `b'my encryption method'`
- `b'is absolutely impenetrable'`
- `b'and you will never'`
- `b'ever'`
- `b'break it'`

Por lo tanto, solo existen $2^5 = 32$ posibles combinaciones efectivas de cadenas XOR aplicadas al texto cifrado.

### Ataque de Texto Claro Conocido (Known-Plaintext Attack)
Sabemos que la bandera inicia con el prefijo `picoCTF{`.
Para cada una de las 32 combinaciones:
1. Revertimos las cadenas activas en esa combinación aplicando XOR sobre el texto cifrado.
2. Extraemos los primeros 7 bytes y los operamos con XOR contra `b'picoCTF'`.
3. Al comprobar las posibles claves derivadas, una de las combinaciones revela la clave legible `b'Africa!'`.
4. Desciframos el texto completo utilizando dicha clave para obtener la bandera.

```bash
python3 - << 'EOF'
with open('output.txt') as f:
    ctxt = bytes.fromhex(f.read().strip())

def encrypt(ptxt, key):
    return bytes([ptxt[i] ^ key[i % len(key)] for i in range(len(ptxt))])

random_strs = [
    b'my encryption method',
    b'is absolutely impenetrable',
    b'and you will never',
    b'ever',
    b'break it'
]

for i in range(2):
    for j in range(2):
        for k in range(2):
            for l in range(2):
                for m in range(2):
                    temp = ctxt
                    if i: temp = encrypt(temp, random_strs[0])
                    if j: temp = encrypt(temp, random_strs[1])
                    if k: temp = encrypt(temp, random_strs[2])
                    if l: temp = encrypt(temp, random_strs[3])
                    if m: temp = encrypt(temp, random_strs[4])
                    
                    potential_key = encrypt(temp[:7], b'picoCTF')
                    if potential_key == b'Africa!':
                        print(encrypt(temp, potential_key).decode())
EOF
```

## Notas adicionales
- Este problema ilustra la falacia de "seguridad por complejidad": anidar múltiples bucles con operaciones XOR no incrementa el espacio de estados más allá de las paridades independientes de cada máscara.
- Flag en formato: `picoCTF{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/208
- Apoyo: https://en.wikipedia.org/wiki/Exclusive_or#Properties
