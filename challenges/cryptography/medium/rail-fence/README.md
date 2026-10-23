# rail-fence

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2022  
**Plataforma:** CyLab Security Academy  

## Descripción

A type of transposition cipher is the rail fence cipher, which is described [here](https://en.wikipedia.org/wiki/Rail_fence_cipher). Here is one such cipher encrypted using the rail fence with 4 rails. Can you decrypt it?  
Download the message [here](https://challenge-files.cylabacademy.net/library/d6cea3d41550d2d3e365dd3a7ea99fe9b44fe5fa437d1c921b5134a2070894a5/message.txt).

The decoded message names a phrase. Put that phrase, and nothing else, in the academy flag format: `academy{phrase}`.

## Hints

1. Once you've understood how the cipher works, it's best to draw it out yourself on paper

## Solución

El archivo `message.txt` contiene: `Ta _7N6D4Chlg:W3D_H3C31N__3E4ef sHR053F38N43DBC i33___NB`

El cifrado de valla de ferrocarril (Rail Fence) es un cifrado de transposición donde el texto plano se escribe en zigzag a lo largo de un número de "rieles" y luego se lee fila por fila.

Con **4 rieles** y un mensaje de **56 caracteres**, el periodo es 2×(4-1) = 6. La estructura zigzag asigna cada posición a un riel. Para descifrar:

1. Se determina qué posiciones pertenecen a cada riel.
2. Se cuentan cuántos caracteres hay en cada riel.
3. Se distribuye el texto cifrado en los rieles según esos conteos.
4. Se reconstruye el mensaje leyendo en orden zigzag.

```python
def rail_fence_decode(ciphertext, rails):
    n = len(ciphertext)
    period = 2 * (rails - 1)

    # Determinar a qué riel pertenece cada posición
    pattern = []
    for i in range(n):
        cycle_pos = i % period
        if cycle_pos < rails:
            pattern.append(cycle_pos)
        else:
            pattern.append(period - cycle_pos)

    # Contar chars por riel
    rail_lengths = [pattern.count(r) for r in range(rails)]

    # Dividir el ciphertext en rieles
    rail_strings = []
    idx = 0
    for r in range(rails):
        rail_strings.append(list(ciphertext[idx:idx + rail_lengths[r]]))
        idx += rail_lengths[r]

    # Reconstruir leyendo en orden zigzag
    rail_indices = [0] * rails
    result = []
    for r in pattern:
        result.append(rail_strings[r][rail_indices[r]])
        rail_indices[r] += 1

    return ''.join(result)

msg = 'Ta _7N6D4Chlg:W3D_H3C31N__3E4ef sHR053F38N43DBC i33___NB'
print(rail_fence_decode(msg, 4))
# Output: The flag is: WH3R3_D035_7H3_F3NC3_8361N_4ND_3ND_43BBCEC4
```

El mensaje descifrado es: `The flag is: WH3R3_D035_7H3_F3NC3_8361N_4ND_3ND_43BBCEC4`

La frase (phrase) a introducir en el formato de flag es `WH3R3_D035_7H3_F3NC3_8361N_4ND_3ND_43BBCEC4`.

La flag completa es: `academy{WH3R3_D035_7H3_F3NC3_8361N_4ND_3ND_43BBCEC4}`

## Referencias

- [Rail Fence Cipher - Wikipedia](https://en.wikipedia.org/wiki/Rail_fence_cipher)
- [dCode Rail Fence Cipher](https://www.dcode.fr/rail-fence-cipher)
