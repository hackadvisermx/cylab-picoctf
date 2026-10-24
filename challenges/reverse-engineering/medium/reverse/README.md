# Reverse Engineering — Reverse

## Descripción
> **Prompt oficial del reto:** "Try reversing this file? Can ya? I forgot the password to this file. Please find it for me?"
>
> **Pistas oficiales:**
> (Ninguna pista proporcionada en la plataforma)

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** Mubarak Mikail

## Solución
El reto suministra un ejecutable ELF x86-64 llamado `ret`.

### 1. Análisis preliminar
Se verifica el tipo de archivo y las propiedades del binario:

```bash
file ret
```
Salida: `ret: ELF 64-bit LSB pie executable, x86-64, not stripped`.

El binario incluye símbolos y no ha sido despojado de nombres (*not stripped*).

### 2. Búsqueda de cadenas en el binario
Al buscar patrones de cadenas de texto dentro del ejecutable:

```bash
strings -a ret | grep -E "academy|picoCTF"
```

O en Python:
```python
with open('ret', 'rb') as f:
    data = f.read()

import re
for m in re.finditer(rb'academy\{[^}]+\}', data):
    print(m.group(0).decode())
```

El binario contiene la contraseña almacenada directamente como literal de cadena en la sección de datos de sólo lectura (`.rodata`), correspondiente a `academy{...}`.

## Notas adicionales
- Al no existir protecciones contra ingeniería inversa ni ofuscación de cadenas, la extracción estática directa permite resolver el reto de forma inmediata.

## Referencias
- Reto: https://learn.cylabacademy.org/library/372
- ELF File Format Specification: https://refspecs.linuxfoundation.org/elf/elf.pdf
