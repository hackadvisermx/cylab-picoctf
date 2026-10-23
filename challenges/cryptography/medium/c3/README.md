# C3 — Custom Cyclical Cipher

**Plataforma:** picoCTF 2024 — CyLab Academy  
**Categoría:** Cryptography  
**Dificultad:** Medium  
**ID:** 407  
**Referencia:** https://learn.cylabacademy.org/library/407

---

## Descripción

> "This is the Custom Cyclical Cipher! Enclose the flag in our wrapper for submission. If the flag was 'example' you would submit 'academy{example}'."

Se entregan dos archivos:
- `ciphertext` — el texto cifrado
- `convert.py` — el script de codificación

---

## Hints oficiales

- *"Modern crypto schemes don't depend on the encoder to be secret, but this one does."*

La pista alude a que la seguridad de este cifrado depende de mantener el algoritmo en secreto (seguridad por oscuridad), a diferencia de los esquemas modernos donde el algoritmo puede ser público y la seguridad radica solo en la clave.

---

## Análisis del algoritmo

El archivo `convert.py` define un cifrado ciclico personalizado de dos fases:

```python
lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"  # 40 chars
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"   # 40 chars

# Codificación:
# Para cada carácter en el texto plano:
#   cur  = lookup1.index(char)       # índice en tabla de entrada
#   out  = (cur - prev) % 40        # diferencia respecto al anterior
#   ciphertext += lookup2[out]       # carácter cifrado
#   prev = cur                       # actualizar estado
```

La operación es **diferencial y ciclica**: cada carácter cifrado representa la diferencia módulo 40 entre el índice del carácter actual y el del anterior en `lookup1`. El estado inicial `prev = 0`.

---

## Solución

### Fase 1 — Descifrado del ciphertext

Para invertir la operación se acumula el índice anterior y se suma al índice cifrado:

```python
lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

with open('ciphertext') as f:
    ciphertext = f.read().strip()

plaintext = ""
prev = 0
for c in ciphertext:
    cur_idx  = lookup2.index(c)
    orig_idx = (cur_idx + prev) % 40
    plaintext += lookup1[orig_idx]
    prev = orig_idx

print(plaintext)
```

El resultado es un **script Python 2** con comentarios descriptivos:

```python
#asciiorder
#fortychars
#selfinput
#pythontwo

chars = ""
from fileinput import input
for line in input():
    chars += line
b = 1 / 1

for i in range(len(chars)):
    if i == b * b * b:
        print chars[i] #prints
        b += 1 / 1
```

### Fase 2 — Ejecución del script sobre sí mismo

Los comentarios del script revelan el mecanismo:
- `#selfinput` → el script se lee a sí mismo como entrada
- `#pythontwo` → debe ejecutarse con Python 2 (donde `1/1 = 1` es entero)
- El script extrae los caracteres en las posiciones que son **cubos perfectos**: `1, 8, 27, 64, 125, 216, ...`

```bash
python2 stage2.py < stage2.py
```

Para replicarlo en Python 3:

```python
with open('stage2.py') as f:
    chars = f.read()

b = 1
result = []
for i in range(len(chars)):
    if i == b * b * b:
        result.append(chars[i])
        b += 1

print(''.join(result))
```

Los 6 cubos perfectos dentro del rango del archivo (237 caracteres) son:
`1, 8, 27, 64, 125, 216` → extraen los caracteres que forman la flag interna.

---

## Notas adicionales

- El cifrado es **ciclico diferencial**: cifra diferencias de índices en lugar de los índices directos, lo que lo hace ligeramente más complejo que un sustitución simple, pero igualmente rompible si se conoce el algoritmo.
- La seguridad por oscuridad (security through obscurity) es un antipatrón reconocido: una vez que el algoritmo es conocido, no existe ninguna clave que proteja el mensaje.
- La Fase 2 es un ejemplo de **quine parcial**: el script extrae información de su propio código fuente.
- El uso de `1 / 1` en lugar de `1` es una forma de forzar que el script requiera Python 2 (donde la división entera no produce float).

---

## Referencias

- https://learn.cylabacademy.org/library/407
- [picoCTF 2024 — C3](https://picoctf.org)
