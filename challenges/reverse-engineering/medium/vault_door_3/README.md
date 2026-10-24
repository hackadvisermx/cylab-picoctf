# Reverse Engineering — vault-door-3

## Descripción
> **Prompt oficial del reto:** "This vault uses for-loops and byte arrays.
> The source code for this vault is here: [VaultDoor3.java](https://challenge-files.cylabacademy.net/library/64ed47ea66574a28e2f23bbe36be348987a9ff131641bf451b1c04bb7b3e2d9f/VaultDoor3.java)"
>
> **Pistas oficiales:**
> 1. Make a table that contains each value of the loop variables and the corresponding buffer index that it writes to.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Mark E. Haase

## Solución
El reto proporciona el archivo de código fuente Java `VaultDoor3.java`. En el método `checkPassword`:

```java
public boolean checkPassword(String password) {
    if (password.length() != 32) {
        return false;
    }
    char[] buffer = new char[32];
    int i;
    for (i=0; i<8; i++) {
        buffer[i] = password.charAt(i);
    }
    for (; i<16; i++) {
        buffer[i] = password.charAt(23-i);
    }
    for (; i<32; i+=2) {
        buffer[i] = password.charAt(46-i);
    }
    for (i=31; i>=17; i-=2) {
        buffer[i] = password.charAt(i);
    }
    String s = new String(buffer);
    return s.equals("jU5t_a_sna_3lpm16gd4e_u_4_m7re42");
}
```

La función permuta las posiciones de los 32 caracteres de `password` en el arreglo `buffer` mediante cuatro bucles:
1. Para $i \in [0, 7]$: `buffer[i] = password[i]` (posiciones 0 a 7 directas).
2. Para $i \in [8, 15]$: `buffer[i] = password[23 - i]` (posiciones 15 a 8 invertidas).
3. Para $i \in [16, 30]$ con paso 2: `buffer[i] = password[46 - i]` (índices pares de 16 a 30).
4. Para $i \in [31, 17]$ descendiendo de 2 en 2: `buffer[i] = password[i]` (índices impares de 17 a 31 directos).

El resultado final en `buffer` debe ser idéntico a `"jU5t_a_sna_3lpm16gd4e_u_4_m7re42"`.

### Reversión de la permutación

Podemos modelar la permutación registrando para cada índice `i` del búfer de destino cuál índice de `password` originó ese carácter, y luego invertir el mapeo para reconstruir `password`:

```python
target = "jU5t_a_sna_3lpm16gd4e_u_4_m7re42"

mapping = {}

# Bucle 1
for i in range(8):
    mapping[i] = i

# Bucle 2
for i in range(8, 16):
    mapping[i] = 23 - i

# Bucle 3
for i in range(16, 32, 2):
    mapping[i] = 46 - i

# Bucle 4
for i in range(31, 16, -2):
    mapping[i] = i

# Invertir mapeo: password[mapping[i]] = target[i]
password = ["?"] * 32
for buf_idx, pass_idx in mapping.items():
    password[pass_idx] = target[buf_idx]

result = "".join(password)
print(f"academy{{{result}}}")
```

Al ejecutar el script de inversión:

```bash
python3 solve.py
```

Se obtiene la cadena original de la contraseña, completando la bandera en formato `academy{...}`.

## Notas adicionales
Este tipo de transformación es una permutación determinista sin pérdida (biyección de índices). Dado que cada posición del búfer se escribe exactamente una vez y depende de una posición única de la entrada, la permutación inversa se calcula sin ambigüedades.

## Referencias
- Reto: https://learn.cylabacademy.org/library/60
- Apoyo: https://en.wikipedia.org/wiki/Permutation
