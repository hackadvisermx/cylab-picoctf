# Reverse Engineering — vault-door-6

## Descripción
> **Prompt oficial del reto:** "This vault uses an XOR encryption scheme.
> The source code for this vault is here: [VaultDoor6.java](https://challenge-files.cylabacademy.net/library/680b9af3f234379a0a23e4715a45e59daff456725331969e493e085fb6df3687/VaultDoor6.java)"
>
> **Pistas oficiales:**
> 1. If X ^ Y = Z, then Z ^ Y = X. Write a program that decrypts the flag based on this fact.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Mark E. Haase

## Solución
El reto proporciona el código fuente en Java `VaultDoor6.java`. En el método `checkPassword`:

```java
public boolean checkPassword(String password) {
    if (password.length() != 32) {
        return false;
    }
    byte[] passBytes = password.getBytes();
    byte[] myBytes = {
        0x3b, 0x65, 0x21, 0xa , 0x38, 0x0 , 0x36, 0x1d,
        0xa , 0x3d, 0x61, 0x27, 0x11, 0x66, 0x27, 0xa ,
        0x21, 0x1d, 0x61, 0x3b, 0xa , 0x2d, 0x65, 0x27,
        0xa , 0x36, 0x33, 0x30, 0x30, 0x63, 0x63, 0x61,
    };
    for (int i=0; i<32; i++) {
        if (((passBytes[i] ^ 0x55) - myBytes[i]) != 0) {
            return false;
        }
    }
    return true;
}
```

La condición de validación requiere que:
$$(\text{passBytes}[i] \oplus 0\text{x}55) - \text{myBytes}[i] = 0$$
$$\implies \text{passBytes}[i] \oplus 0\text{x}55 = \text{myBytes}[i]$$

### Propiedad involutiva del XOR

Dado que la operación XOR es su propio inverso:
$$\text{Si } A \oplus K = B \implies B \oplus K = A$$

Por lo tanto, podemos recuperar cada byte de la contraseña aplicando XOR a cada elemento de `myBytes` con la misma clave `0x55`:
$$\text{passBytes}[i] = \text{myBytes}[i] \oplus 0\text{x}55$$

### Script de descifrado en Python

```python
my_bytes = [
    0x3b, 0x65, 0x21, 0xa , 0x38, 0x0 , 0x36, 0x1d,
    0xa , 0x3d, 0x61, 0x27, 0x11, 0x66, 0x27, 0xa ,
    0x21, 0x1d, 0x61, 0x3b, 0xa , 0x2d, 0x65, 0x27,
    0xa , 0x36, 0x33, 0x30, 0x30, 0x63, 0x63, 0x61,
]

key = 0x55
password = "".join(chr(b ^ key) for b in my_bytes)
print(f"academy{{{password}}}")
```

Al ejecutar el script:

```bash
python3 solve.py
```

Se obtienen los caracteres de la contraseña, formando la bandera en formato `academy{...}`.

## Notas adicionales
El cifrado XOR de un solo byte es un algoritmo simétrico elemental muy común en malware básico y empaquetadores para ofuscar cadenas de texto y firmas. Al ser una operación bit a bit sin acarreo, cada byte cifrado depende exclusivamente del byte correspondiente y de la clave.

## Referencias
- Reto: https://learn.cylabacademy.org/library/45
- Apoyo: https://en.wikipedia.org/wiki/Exclusive_or#Computer_science
