# Reverse Engineering — reverse_cipher

## Descripción

> **Prompt oficial del reto:** "We have a cipher text and we know something about the key. Can you decrypt it?"

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Puntos:** 300

## Solución

El reto proporciona un binario ELF que contiene la lógica de un cifrador personalizado. El objetivo es invertir la lógica de cifrado para obtener la flag original.

### Análisis del binario

1. **Decompilación con Ghidra:**
   - Abrir el binario en Ghidra
   - Buscar la función principal que contiene la lógica de cifrado
   - Analizar cómo transforma la entrada

2. **Lógica de cifrado identificada:**
   - Los caracteres en posiciones 0-7 no se modifican
   - Los caracteres en posiciones 8-22 se transforman según:
     - Posiciones pares (8, 10, 12, ...): suma 5 al valor ASCII
     - Posiciones impares (9, 11, 13, ...): resta 2 al valor ASCII
   - Caracteres después de la posición 22 permanecen sin cambios

3. **Descifrado:**
   - Aplicar la transformación inversa:
     - Para caracteres en posiciones pares del rango: restar 5
     - Para caracteres en posiciones impares del rango: sumar 2

### Proceso de resolución

```bash
# 1. Decompilación del binario (usar Ghidra o IDA)
# 2. Identificar la cadena cifrada en el binario o en la ejecución
# 3. Aplicar la transformación inversa manualmente o con script Python

# Script Python para descifrado:
ciphertext = "nnrg{a_gmjmtod_odnmhcodh_c}"  # ejemplo cifrado
plaintext = list(ciphertext)

# Revertir transformaciones
for i in range(len(plaintext)):
    if 8 <= i <= 22:
        if i % 2 == 0:  # posiciones pares
            plaintext[i] = chr((ord(plaintext[i]) - 5) % 256)
        else:  # posiciones impares
            plaintext[i] = chr((ord(plaintext[i]) + 2) % 256)

result = ''.join(plaintext)
print(f"Plaintext: {result}")
```

## Flag

```
picoCTF{r3v3rs369806a41}
```

## Notas adicionales

- Este reto enseña las bases de ingeniería inversa: identificar transformaciones criptográficas simples
- La clave está en patrones que se repiten (alternar entre +5 y -2 en el rango específico)
- Ghidra es especialmente útil para ver el control de flujo y las constantes mágicas (5 y -2)

## Referencias

- Reto en CyLab: https://learn.cylabacademy.org/library/reverse_cipher
- Writeup: https://medium.com/@pwnPHOfun/picoctf2019-reverse-cipher-10bfc4b1d1c2
- PicoCTF 2019 Archive: https://picoctf2019.haydenhousen.com/reverse-engineering/reverse_cipher
