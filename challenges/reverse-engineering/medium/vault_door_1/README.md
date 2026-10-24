# Reverse Engineering — vault-door-1

## Descripción
> **Prompt oficial del reto:** "This vault uses some complicated arrays! I hope you can make sense of it, special agent. The source code for this vault is here: [VaultDoor1.java](https://challenge-files.cylabacademy.net/library/60e8fbcf22f4bfa0e9856c1ebbd5506050d5f0ab9fb013f9e3e175021205869b/VaultDoor1.java)"
>
> **Pistas oficiales:**
> 1. Look up the charAt() method online.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Mark E. Haase

## Solución
El reto provee el archivo de código fuente en Java `VaultDoor1.java`. Al inspeccionar el método de validación `checkPassword`:

```java
public boolean checkPassword(String password) {
    return password.length() == 32 &&
           password.charAt(0)  == 'd' &&
           password.charAt(29) == 'b' &&
           password.charAt(4)  == 'r' &&
           password.charAt(2)  == '5' &&
           password.charAt(23) == 'r' &&
           password.charAt(3)  == 'c' &&
           password.charAt(17) == '4' &&
           password.charAt(1)  == '3' &&
           password.charAt(7)  == 'b' &&
           password.charAt(10) == '_' &&
           password.charAt(5)  == '4' &&
           password.charAt(9)  == '3' &&
           password.charAt(11) == 't' &&
           password.charAt(15) == 'c' &&
           password.charAt(8)  == 'l' &&
           password.charAt(12) == 'H' &&
           password.charAt(20) == 'c' &&
           password.charAt(14) == '_' &&
           password.charAt(6)  == 'm' &&
           password.charAt(24) == '5' &&
           password.charAt(18) == 'r' &&
           password.charAt(13) == '3' &&
           password.charAt(19) == '4' &&
           password.charAt(21) == 'T' &&
           password.charAt(16) == 'H' &&
           password.charAt(27) == '5' &&
           password.charAt(30) == 'c' &&
           password.charAt(25) == '_' &&
           password.charAt(22) == '3' &&
           password.charAt(28) == 'e' &&
           password.charAt(26) == '4' &&
           password.charAt(31) == '3';
}
```

La función comprueba que la longitud sea de 32 caracteres y evalúa cada posición mediante `charAt(i) == '<c>'`. Las condiciones están escritas en un orden no secuencial para desorientar una lectura directa rápida.

### Script de extracción y ordenamiento en Python

Podemos usar expresiones regulares para extraer cada pareja `(índice, carácter)` y ordenarlas numéricamente por su posición:

```python
import re

with open("VaultDoor1.java") as f:
    content = f.read()

# Extraer comparaciones charAt(pos) == 'char'
matches = re.findall(r"password\.charAt\((\d+)\)\s*==\s*'([^']*)'", content)

# Armar la cadena en orden de índice
flag_chars = ["?"] * 32
for idx, char in matches:
    flag_chars[int(idx)] = char

password = "".join(flag_chars)
print(f"academy{{{password}}}")
```

Al ordenar los caracteres de 0 a 31:

```bash
python3 solve.py
```

Se obtiene la contraseña completa en texto plano que forma la bandera en formato `academy{...}`.

## Notas adicionales
El método `charAt(int index)` de la clase `String` en Java devuelve el valor del carácter en el índice especificado, comenzando en 0 hasta `length() - 1`. Dado que el orden de evaluación booleana en Java no altera el significado declarativo de las igualdades conjuntivas (`&&`), reordenar por índice reconstruye la cadena original instantáneamente.

## Referencias
- Reto: https://learn.cylabacademy.org/library/12
- Apoyo: https://docs.oracle.com/javase/8/docs/api/java/lang/String.html#charAt-int-
