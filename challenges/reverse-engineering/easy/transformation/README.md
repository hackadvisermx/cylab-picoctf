# Reverse Engineering — Transformation

## Descripción
> **Prompt oficial del reto:** "I wonder what this really is... [enc](https://challenge-files.cylabacademy.net/library/dc17749d8d457a4caa6caa09c664f5143959611291adc36e2fac64193d1472f9/enc)
> 
> ```python
> ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
> ```"
>
> **Pistas oficiales:**
> 1. You may find some decoders online

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2021
- **Autor:** madStacks

## Solución
El reto proporciona un archivo codificado llamado `enc` y la comprensión de lista de Python utilizada para generarlo a partir de la bandera original:

```python
''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
```

### Análisis del algoritmo de cifrado / empaquetado

1. El generador toma pares de caracteres adyacentes de la cadena de entrada (`flag[i]` y `flag[i + 1]`).
2. Desplaza el código numérico del primer carácter 8 bits a la izquierda:
   $$\text{ord}(\text{flag}[i]) \ll 8$$
   Esto sitúa su valor de 8 bits en el byte más significativo (*high byte*) de un entero de 16 bits.
3. Suma el código numérico del segundo carácter en los 8 bits menos significativos (*low byte*):
   $$\text{code} = (\text{ord}(\text{flag}[i]) \ll 8) + \text{ord}(\text{flag}[i + 1])$$
4. Convierte el número resultante de 16 bits en un único carácter Unicode con `chr(...)`.

Cada carácter del texto resultante empaqueta dos caracteres ASCII de la flag original en formato *big-endian*.

### Proceso de inversión

Para revertir cada carácter codificado $C$ con código ordinal $N = \text{ord}(C)$:
- Primer carácter: desplazar 8 bits a la derecha para aislar el byte superior:
  $$\text{char}_1 = \text{chr}(N \gg 8)$$
- Segundo carácter: aplicar una máscara con `0xFF` para aislar el byte inferior:
  $$\text{char}_2 = \text{chr}(N \ \& \ \text{0xFF})$$

### Script de resolución

```python
# solve.py
with open("enc", "r", encoding="utf-8") as f:
    ciphertext = f.read().strip()

flag = ""
for char in ciphertext:
    code = ord(char)
    char1 = chr(code >> 8)
    char2 = chr(code & 0xFF)
    flag += char1 + char2

print("Flag recuperada:", flag)
```

Ejecución en una sola línea desde la terminal:

```bash
python3 -c "
with open('enc', 'r', encoding='utf-8') as f:
    s = f.read().strip()
print(''.join(chr(ord(c) >> 8) + chr(ord(c) & 0xff) for c in s))
"
```

La flag final tiene la estructura `academy{...}`.

## Notas adicionales
- Este esquema es idéntico a interpretar un flujo de bytes UTF-8 o ASCII como caracteres codificados en UTF-16 Big Endian. También se puede resolver directamente en Python mediante decodificación de bytes: `ciphertext.encode('utf-16-be').decode('utf-8')`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/104
- Python chr() and ord() Built-in Functions: https://docs.python.org/3/library/functions.html
