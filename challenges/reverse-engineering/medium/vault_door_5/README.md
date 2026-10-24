# Reverse Engineering — vault-door-5

## Descripción
> **Prompt oficial del reto:** "In the last challenge, you mastered octal (base 8), decimal (base 10), and hexadecimal (base 16) numbers, but this vault door uses a different change of base as well as URL encoding!
> The source code for this vault is here: [VaultDoor5.java](https://challenge-files.cylabacademy.net/library/e0c427718db4f670d4a09df9a1ce5c4d2ff6dec848cbbda005a892acccaa4097/VaultDoor5.java)"
>
> **Pistas oficiales:**
> 1. You may find an encoder/decoder tool helpful, such as https://encoding.tools/
> 2. Read the wikipedia articles on URL encoding and base 64 encoding to understand how they work and what the results look like.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Mark E. Haase

## Solución
El reto nos provee el archivo de código fuente en Java `VaultDoor5.java`. Al revisar el método de validación `checkPassword`:

```java
public boolean checkPassword(String password) {
    String urlEncoded = urlEncode(password.getBytes());
    String base64Encoded = base64Encode(urlEncoded.getBytes());
    String expected = "JTYzJTMwJTZlJTc2JTMzJTcyJTc0JTMxJTZlJTY3JTVm"
                    + "JTY2JTcyJTMwJTZkJTVmJTYyJTYxJTM1JTY1JTVmJTM2"
                    + "JTM0JTVmJTY1JTMzJTM0JTMwJTYzJTMzJTY1JTY0";
    return base64Encoded.equals(expected);
}
```

El algoritmo de comprobación aplica dos transformaciones consecutivas sobre la contraseña introducida:
1. **URL encoding:** Convierte cada byte en su representación hexadecimal precedida por `%` (por ejemplo, `%63%30...`).
2. **Base64 encoding:** Codifica el texto resultante del URL encoding a Base64 estándar.

### Reversión de las transformaciones

Para recuperar la contraseña original, invertimos el proceso en orden inverso:
1. Decodificar la cadena Base64 esperada para recuperar el texto URL encoded.
2. Aplicar decodificación URL (*URL decode / percent-unquote*) sobre dicho texto.

### Script de resolución en Python

```python
import base64
import urllib.parse

expected = (
    "JTYzJTMwJTZlJTc2JTMzJTcyJTc0JTMxJTZlJTY3JTVm"
    "JTY2JTcyJTMwJTZkJTVmJTYyJTYxJTM1JTY1JTVmJTM2"
    "JTM0JTVmJTY1JTMzJTM0JTMwJTYzJTMzJTY1JTY0"
)

# Paso 1: Decodificar Base64
url_encoded_bytes = base64.b64decode(expected)
url_encoded_str = url_encoded_bytes.decode("utf-8")
print("Texto codificado en URL:", url_encoded_str)

# Paso 2: Decodificar URL encoding
password = urllib.parse.unquote(url_encoded_str)
print("Contraseña recuperada:", password)
print(f"Bandera completa: academy{{{password}}}")
```

Al ejecutar el script:

```bash
python3 solve.py
```

Se obtiene la contraseña que, al ser encapsulada en `academy{...}`, conforma la bandera válida.

## Notas adicionales
Tanto Base64 como URL encoding son mecanismos de codificación de datos (*encoding*) diseñados para transportar bytes binarios a través de canales de texto plano o protocolos web, y no mecanismos criptográficos de confidencialidad, por lo que son completamente reversibles sin necesidad de claves secretas.

## Referencias
- Reto: https://learn.cylabacademy.org/library/77
- Apoyo: https://en.wikipedia.org/wiki/Percent-encoding
- Apoyo: https://en.wikipedia.org/wiki/Base64
