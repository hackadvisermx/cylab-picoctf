# Substitution2

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2022  
**Plataforma:** CyLab Security Academy  

## Descripción

It seems like every time you teach a class, students have a stronger grasp on the fundamentals, but you've seen them get tripped up in the advanced topics. What can you do?

[message.txt](https://challenge-files.cylabacademy.net/library/9c65f61006fc9c5e6c0ddca3f97fb3bc0e7cf04df7d21ba8f68765c74cc12b46/message.txt)

## Hints

1. Try a frequency attack
2. Do the punctuation and the individual words help you make any substitutions?
3. Several word substitutions are a lot harder to do. Is there something more systematic you can do?

## Solución

A diferencia de Substitution0 y Substitution1, el texto de Substitution2 no tiene espacios, lo que dificulta el análisis de frecuencia por palabras. Sin embargo, la secuencia `hahpsem{...}` al final del texto revela la flag codificada.

**Derivación del mapa de sustitución:**

1. **Ancla principal:** La palabra al final del texto, `hahpsem{...}`, es `academy{...}`.  
   → h→a, a→c, p→d, s→e, e→m, m→y

2. **Trigramas frecuentes:** `ngs` aparece como la secuencia más común de 3 letras → `ngs` = `the`  
   → n→t, g→h (s→e confirmado)

3. **Extensión:** `ngsz` = `ther` → z→r

4. **Palabra clave:** `awebsnknkwrq` = `competition` (lectura contextual del texto sobre CTFs)  
   → a→c(confirmado), w→o, e→m(confirmado), b→p, s→e(confirmado), n→t(confirmado), k→i, r→n

5. **Validación cruzada:** `winsrx` ≈ `often` → i→f (confirmado con frecuencias)

6. **Flag en el texto:** La flag codificada `R6Z4E_4R41M515_15_73P10T5_AIS4S232` se decodifica con el mapa completo:

```python
cipher_to_plain = {
    'h':'a', 'a':'c', 'p':'d', 's':'e', 'e':'m', 'm':'y',
    'n':'t', 'g':'h', 'z':'r', 'w':'o', 'b':'p', 'k':'i',
    'r':'n', 'i':'f', 't':'u'
}

text = open('message.txt').read()
decoded = ''.join(cipher_to_plain.get(c.lower(), c) for c in text)
print(decoded)
```

**Decodificación de la flag (leet speak):**
- `R6Z4E` → `N6R4M` = **N-GRAM** (6=G, 4=A)
- `4R41M515` → `4N41Y515` = **ANALYSIS** (4=A, 1=L, Y=Y, 5=S, 1=I)
- `15` = **IS** (1=I, 5=S)
- `73P10T5` → `73D10U5` = **TEDIOUS** (7=T, 3=E, 1=I, 0=O, 5=S)
- `AIS4S232` → `CFE4E232` (hash)

Flag: `academy{N6R4M_4N41Y515_15_73D10U5_CFE4E232}`

## Referencias

- [N-gram - Wikipedia](https://en.wikipedia.org/wiki/N-gram)
- [Frequency Analysis - Wikipedia](https://en.wikipedia.org/wiki/Frequency_analysis)
- [quipqiup.com - solucionador automático](https://quipqiup.com)
