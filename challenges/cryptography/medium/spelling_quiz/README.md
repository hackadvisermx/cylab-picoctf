# spelling-quiz

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Plataforma:** CyLab Academy (picoMini by redpwn, ID 210)  
**Puntos:** N/A (estático)

## Descripción

> I found the flag, but my brother wrote a program to encrypt all his text files. He has a spelling quiz study guide too, but I don't know if that helps.

## Archivos

- `encrypt.py` — script Python que cifra todos los `.txt` del directorio
- `study-guide.txt` — guía de estudio de ortografía cifrada (~3 MB, ~272 000 palabras)
- `flag.txt` — flag cifrada

## Análisis

### El cifrado

`encrypt.py` implementa una **sustitución monoalfabética** (cifrado por sustitución simple):

```python
alphabet = list('abcdefghijklmnopqrstuvwxyz')
random.shuffle(shuffled := alphabet[:])
dictionary = dict(zip(alphabet, shuffled))
```

Se genera un mapeo aleatorio de cada letra minúscula a otra letra del alfabeto. Caracteres que no son letras minúsculas (mayúsculas, dígitos, guiones bajos) no se modifican. El mismo mapeo se aplica a **todos** los archivos `.txt` del directorio, por lo que tanto `study-guide.txt` como `flag.txt` fueron cifrados con la misma clave.

### Flag cifrada

```
brcfxba_vfr_mid_hosbrm_iprc_exa_hoav_vwcrm
```

Los guiones bajos no cambian, lo que sugiere una estructura de palabras separadas: 7 palabras de longitudes 7, 3, 3, 6, 4, 3, 4, 5.

## Solución

### Ataque de texto conocido por patrones de palabras

La guía de estudio contiene ~272 000 palabras inglesas cifradas. La idea es:

1. Para cada palabra cifrada, calcular su **patrón estructural** (qué posiciones comparten la misma letra). Ej.: `"add"` → patrón `(0,1,1)`.
2. Buscar en un diccionario del sistema (`/usr/share/dict/words`) palabras inglesas con el mismo patrón.
3. Si solo existe **una** palabra en inglés con ese patrón y longitud, el emparejamiento es unívoco y revela letras del mapeo.
4. Iterar hasta cubrir todas las letras del alfabeto.

```python
from collections import defaultdict, Counter

def get_pattern(word):
    mapping = {}
    counter = 0
    pattern = []
    for c in word:
        if c not in mapping:
            mapping[c] = counter
            counter += 1
        pattern.append(mapping[c])
    return tuple(pattern)

# Construir índice de patrones del diccionario
with open('/usr/share/dict/words') as f:
    dict_words = set(l.strip().lower() for l in f if l.strip().isalpha())

pattern_to_words = defaultdict(list)
for w in dict_words:
    pattern_to_words[get_pattern(w)].append(w)

# Buscar coincidencias únicas en la guía
cipher_map = {}
inv_cipher_map = {}

for enc_word in enc_words[:10000]:
    pat = get_pattern(enc_word)
    matches = pattern_to_words.get(pat, [])
    if len(matches) == 1:
        # Mapeo unívoco: enc_word <-> matches[0]
        for ec, pc in zip(enc_word, matches[0]):
            cipher_map[ec] = pc
            inv_cipher_map[pc] = ec
```

Con las primeras 10 000 palabras de la guía se obtienen ~2 133 coincidencias únicas, suficientes para decodificar las 26 letras del alfabeto.

### Tabla de descifrado obtenida

| Cifrado | Plano | | Cifrado | Plano |
|---------|-------|-|---------|-------|
| a | s | | n | c |
| b | p | | o | u |
| c | r | | p | v |
| d | g | | q | y |
| e | w | | r | e |
| f | h | | s | m |
| g | k | | t | n |
| h | j | | u | b |
| i | o | | v | t |
| j | q | | w | i |
| k | z | | x | a |
| l | l | | y | f |
| m | d | | z | x |

### Descifrado de la flag

```
brcfxba_vfr_mid_hosbrm_iprc_exa_hoav_vwcrm
perhaps_the_dog_jumped_over_was_just_tired
```

Parte a parte:
- `brcfxba` → `perhaps`
- `vfr` → `the`
- `mid` → `dog`
- `hosbrm` → `jumped`
- `iprc` → `over`
- `exa` → `was`
- `hoav` → `just`
- `vwcrm` → `tired`

## Script de solución

`solve_spelling2.py` (en `tmp/`):

```python
enc_flag = 'brcfxba_vfr_mid_hosbrm_iprc_exa_hoav_vwcrm'
cipher_map = {
    'a':'s','b':'p','c':'r','d':'g','e':'w','f':'h','g':'k','h':'j',
    'i':'o','j':'q','k':'z','l':'l','m':'d','n':'c','o':'u','p':'v',
    'q':'y','r':'e','s':'m','t':'n','u':'b','v':'t','w':'i','x':'a',
    'y':'f','z':'x'
}
decrypted = ''.join(cipher_map.get(c, c) for c in enc_flag)
# perhaps_the_dog_jumped_over_was_just_tired
```

## Lecciones aprendidas

- Una sustitución monoalfabética **nunca debe reutilizar la misma clave** en múltiples archivos: con texto conocido (o predecible como una guía de ortografía) se recupera el mapeo completo.
- Con ~3 MB de texto cifrado, el **análisis de frecuencias** también funciona, aunque el análisis por patrones de palabras es más preciso.
- La estructura del flag (guiones bajos preservados) facilita verificar el resultado: las palabras descifradas forman una frase con sentido en inglés.
