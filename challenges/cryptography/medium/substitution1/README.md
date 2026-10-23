# Substitution1

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2022  
**Plataforma:** CyLab Security Academy  

## Descripción

A second message has come in the mail, and it seems almost identical to the first one. Maybe the same thing will work again.

[message.txt](https://challenge-files.cylabacademy.net/library/7bfa985513e099d32240b37e499262d5fb6147c074a8ee5ecd932c14deb05ac7/message.txt)

## Hints

1. Try a frequency attack
2. Do the punctuation and the individual words help you make any substitutions?

## Solución

A diferencia de Substitution0, esta vez no hay clave al inicio. El texto cifrado es el mismo párrafo sobre CTFs pero con un alfabeto de sustitución diferente.

**Construcción del mapeo por palabras conocidas:**

El texto trata sobre competencias CTF. Al identificar palabras probables:
- `ktkuxvb{...}` = `academy{...}` → k→a, t→c, u→d, x→e, v→m, b→y
- `TAHd` = `CTFs` → T→C, A→T, H→F, d→s
- `aqx` = `the` → a→t (ya conocida), q→h
- `hzko` = `flag` → h→f, z→l, o→g

Con estas anclas se va completando el mapeo letra por letra hasta descifrar todo el texto.

```python
# Mapeo construido por análisis
known = {
    'k':'a', 't':'c', 'u':'d', 'x':'e', 'v':'m', 'b':'y',
    'a':'t', 'h':'f', 'd':'s', 'q':'h', 'z':'l', 'o':'g',
    'l':'r', 'e':'o', 'f':'p', 'c':'u', 'r':'n', 'i':'i',
    'n':'k', 'm':'q', 's':'b'
}
for k, v in list(known.items()):
    known[k.upper()] = v.upper()

text = open('message.txt').read()
result = ''.join(known.get(c, c) for c in text)
print(result)
```

La última letra del sufijo del hash (`S→B`) se determinó por prueba con `submit_flag()`.

Flag: `academy{FR3QU3NCY_4774CK5_4R3_C001_7B0043A0}`

## Referencias

- [Frequency Analysis - Wikipedia](https://en.wikipedia.org/wiki/Frequency_analysis)
- [quipqiup.com - solucionador automático de sustitución](https://quipqiup.com)
