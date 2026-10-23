# Substitution0

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2022  
**Plataforma:** CyLab Security Academy  

## Descripción

A message has come in but it seems to be all scrambled. Luckily it seems to
have the key at the beginning. Can you crack it?

[message.txt](https://challenge-files.cylabacademy.net/library/c81cd186dacb4ad82560df3b81fe365fc1c38a1c7dca9a73a9604c5345ab4473/message.txt)

## Hints

1. Try a frequency attack. An online tool might help.

## Solución

El archivo `message.txt` comienza con la clave del cifrado en la primera línea:

```
DJHMILABFORYVGNKUXQSCPEWZT
```

Esta es la lista del alfabeto cifrado: la letra A se cifra como D, la B como J, la C como H, etc.

Para descifrar, se construye el mapeo inverso: D→A, J→B, H→C, M→D, etc.

```python
key = 'DJHMILABFORYVGNKUXQSCPEWZT'

# Construir tabla de descifrado
decrypt = {}
for i, c in enumerate(key):
    decrypt[c] = chr(ord('A') + i)
    decrypt[c.lower()] = chr(ord('a') + i)

text = open('message.txt').read()
result = ''.join(decrypt.get(c, c) for c in text)
print(result)
```

El texto descifrado revela un fragmento de "The Gold-Bug" de Edgar Allan Poe y la flag al final:

```
academy{5UB5717U710N_3V0LU710N_6A8C4822}
```

## Referencias

- [Ataque de frecuencia - Wikipedia](https://en.wikipedia.org/wiki/Frequency_analysis)
- [dcode.fr - Substitution Cipher](https://www.dcode.fr/substitution-cipher)
