# Reverse Engineering — vault-door-4

## Descripción
> **Prompt oficial del reto:** "This vault uses ASCII encoding for the password.
> The source code for this vault is here: [VaultDoor4.java](https://challenge-files.cylabacademy.net/library/e8b3667853e7380d04e46c5b844bbad1cbd0855975b83213e23045054681c91d/VaultDoor4.java)"
>
> **Pistas oficiales:**
> 1. Use a search engine to find an "ASCII table"
> 2. You will also need to know the difference between octal, decimal, and hexadecimal numbers.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Mark E. Haase

## Solución
El reto proporciona el código fuente en Java `VaultDoor4.java`. Al inspeccionar la función `checkPassword`:

```java
public boolean checkPassword(String password) {
    byte[] passBytes = password.getBytes();
    byte[] myBytes = {
        106 , 85  , 53  , 116 , 95  , 52  , 95  , 98  ,
        0x55, 0x6e, 0x43, 0x68, 0x5f, 0x30, 0x66, 0x5f,
        0142, 0131, 0164, 063 , 0163, 0137, 062 , 0141,
        '8' , '4' , 'e' , 'c' , '9' , 'f' , '2' , '0' ,
    };
    for (int i=0; i<32; i++) {
        if (passBytes[i] != myBytes[i]) {
            return false;
        }
    }
    return true;
}
```

La función compara la contraseña carácter a carácter contra un arreglo de 32 bytes expresados en cuatro sistemas de representación numérica distintos:
1. **Fila 1 (Decimal):** Valores en base 10 (`106, 85, 53, ...`).
2. **Fila 2 (Hexadecimal):** Valores con prefijo `0x` en base 16 (`0x55, 0x6e, ...`).
3. **Fila 3 (Octal):** Literales en base 8 en Java, denotados por el cero inicial (`0142, 0131, ...`).
4. **Fila 4 (Caracteres ASCII literales):** Caracteres individuales entre comillas simples (`'8', '4', ...`).

### Script de decodificación en Python

Podemos convertir cada fila a caracteres ASCII y concatenarlos:

```python
bytes_decimal = [106 , 85  , 53  , 116 , 95  , 52  , 95  , 98]
bytes_hex = [0x55, 0x6e, 0x43, 0x68, 0x5f, 0x30, 0x66, 0x5f]
bytes_octal = [0o142, 0o131, 0o164, 0o63 , 0o163, 0o137, 0o62 , 0o141]
chars_literal = ['8' , '4' , 'e' , 'c' , '9' , 'f' , '2' , '0']

all_bytes = bytes_decimal + bytes_hex + bytes_octal + [ord(c) for c in chars_literal]
password = "".join(chr(b) for b in all_bytes)
print(f"Bandera: academy{{{password}}}")
```

Al ejecutar el script:

```bash
python3 solve.py
```

Se obtiene la contraseña de 32 caracteres que compone la bandera en formato `academy{...}`.

## Notas adicionales
En Java, los números enteros que inician con un dígito `0` (como `0142`) son interpretados por el compilador como literales en base octal. En Python 3, la sintaxis equivalente para literales octales requiere el prefijo `0o` (por ejemplo, `0o142`).

## Referencias
- Reto: https://learn.cylabacademy.org/library/71
- Apoyo: https://www.asciitable.com/
- Apoyo: https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html
