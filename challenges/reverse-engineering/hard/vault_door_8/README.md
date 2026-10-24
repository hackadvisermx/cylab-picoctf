# Reverse Engineering — vault-door-8

## Descripción
> **Prompt oficial del reto:** "Apparently Dr. Evil's minions knew that our agency was making copies of their source code, because they intentionally sabotaged this source code in order to make it harder for our agents to analyze and crack into! The result is a quite mess, but I trust that my best special agent will find a way to solve it."
>
> **Pistas oficiales:**
> 1. Clean up the code first so you can read it.
> 2. How can you reverse the bit transposition?

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Mark E. Haase

## Solución
El reto proporciona el código fuente en Java de un mecanismo de validación de contraseña (`VaultDoor8.java`). A diferencia de los retos anteriores de la serie `vault-door`, el código ha sido ofuscado y aplica una permutación a nivel de bits sobre cada carácter de la contraseña ingresada antes de compararla con un arreglo de bytes esperado.

### 1. Análisis del código fuente
Al formatear e inspeccionar `VaultDoor8.java`:

```java
public char[] scramble(String password) {
    char[] a = password.toCharArray();
    for (int b = 0; b < a.length; b++) {
        char c = a[b];
        c = switchBits(c, 1, 2);
        c = switchBits(c, 0, 3);
        c = switchBits(c, 5, 6);
        c = switchBits(c, 4, 7);
        c = switchBits(c, 0, 1);
        c = switchBits(c, 3, 4);
        c = switchBits(c, 2, 5);
        c = switchBits(c, 6, 7);
        a[b] = c;
    }
    return a;
}

public char switchBits(char c, int p1, int p2) {
    char mask1 = (char)(1 << p1);
    char mask2 = (char)(1 << p2);
    char bit1 = (char)(c & mask1);
    char bit2 = (char)(c & mask2);
    char rest = (char)(c & ~(mask1 | mask2));
    char shift = (char)(p2 - p1);
    char result = (char)((bit1 << shift) | (bit2 >> shift) | rest);
    return result;
}
```

La función `switchBits(c, p1, p2)` intercambia las posiciones de los bits `p1` y `p2` dentro del byte `c`. Un intercambio de bits es una operación idempotente / involutiva ($f(f(x)) = x$): al aplicar el mismo intercambio dos veces se recupera el valor original.

Para invertir la función `scramble`, únicamente se debe aplicar la secuencia de intercambios en orden exactamente inverso:
1. `(6, 7)`
2. `(2, 5)`
3. `(3, 4)`
4. `(0, 1)`
5. `(4, 7)`
6. `(5, 6)`
7. `(0, 3)`
8. `(1, 2)`

### 2. Script de resolución en Python

```python
def switch_bits(c, p1, p2):
    mask1 = 1 << p1
    mask2 = 1 << p2
    bit1 = c & mask1
    bit2 = c & mask2
    rest = c & ~(mask1 | mask2)
    shift = p2 - p1
    return ((bit1 << shift) | (bit2 >> shift) | rest) & 0xFF


def unscramble_char(c):
    c = switch_bits(c, 6, 7)
    c = switch_bits(c, 2, 5)
    c = switch_bits(c, 3, 4)
    c = switch_bits(c, 0, 1)
    c = switch_bits(c, 4, 7)
    c = switch_bits(c, 5, 6)
    c = switch_bits(c, 0, 3)
    c = switch_bits(c, 1, 2)
    return c


expected = [
    0xF4, 0xC0, 0x97, 0xF0, 0x77, 0x97, 0xC0, 0xE4,
    0xF0, 0x77, 0xA4, 0xD0, 0xC5, 0x77, 0xF4, 0x86,
    0xD0, 0xA5, 0x45, 0x96, 0x27, 0xB5, 0x77, 0xB4,
    0xD0, 0xA5, 0xC2, 0xE1, 0xE0, 0xC0, 0xF0, 0xB4,
]

inner = bytes([unscramble_char(b) for b in expected]).decode("latin1")
# Flag: academy{...}
```

## Notas adicionales
- El programa extrae el contenido de la contraseña descartando los primeros 8 caracteres y el último (`c.substring(8, c.length()-1)`), correspondiente a la envoltura `academy{...}` o `picoCTF{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/10
- Permutaciones a nivel de bits (Bit twiddling): https://graphics.stanford.edu/~seander/bithacks.html
