# Reverse Engineering — Wizardlike

## Descripción

> **Prompt oficial del reto:** "Exploit a game engine to reveal the flag."

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2022
- **Puntos:** 500

## Solución

El reto presenta un binario interactivo tipo "dungeon crawl" donde se puede mover con WASD y salir con Q. La flag está oculta en ASCII art dentro del binario o en memoria durante la ejecución. El objetivo es explotar las limitaciones de colisión del juego o analizar el binario para revelar la flag.

### Técnica 1: Análisis de strings (más simple)

```bash
# 1. Ejecutar strings sobre el binario
strings wizardlike | grep -i "picoctf"

# 2. Si no aparece directamente, buscar ASCII art
strings wizardlike | head -200

# 3. Redimensionar terminal a 100 columnas para ver ASCII art correctamente
# (El ASCII art puede estar oculto en strings con formato específico)
```

### Técnica 2: Parching binario (más efectivo)

1. **Decompilación con Ghidra:**
   - Abrir el binario en Ghidra
   - Buscar la función de control de colisiones/límites del mapa
   - Identificar dónde se validan las coordenadas del jugador

2. **Modificación:**
   - Localizar las instrucciones que comprueban si el jugador está dentro del área de juego válida
   - Comentar o modificar las instrucciones de verificación de límites
   - Guardar el binario modificado

3. **Ejecución:**
   ```bash
   # Ejecutar el binario parchado
   ./wizardlike_patched
   
   # Navegar fuera de los límites normales del mapa
   # (WASD para movimiento) para encontrar la flag
   ```

### Técnica 3: Debugging dinámico con radare2

```bash
# 1. Iniciar radare2 en modo debug
r2 -d wizardlike

# 2. Encontrar la función principal
aaa  # analizar todo
s main

# 3. Buscar referencias a coordenadas
/r rax  # buscar referencias

# 4. Poner breakpoints en funciones de verificación
db 0x[dirección]

# 5. Continuar ejecución
dc

# 6. Modificar registros para teleportarse
dr rax=9999  # cambiar coordenadas

# 7. Inspeccionar memoria en esa ubicación
px 100 @ 0x[dirección]
```

## Flag

```
picoCTF{ur_4_w1z4rd_4B0DA5A9}
```

## Notas adicionales

- Este es uno de los retos más difíciles de RE 2022 (500 puntos)
- El juego implementa un sistema simple de colisiones que puede ser eludido
- La flag se revela cuando el jugador accede a un área "especial" del mapa
- Técnica 1 (strings) a menudo revela la flag si está en ASCII art sin comprimir
- El binario puede estar protegido contra debugging, en cuyo caso la modificación binaria es más efectiva

## Referencias

- Reto en picoCTF: https://play.picoctf.org/practice/challenge/286
- Writeup GitHub (HHousen): https://github.com/HHousen/PicoCTF-2022/blob/master/Reverse%20Engineering/Wizardlike/README.md
- Writeup personal: https://cy7.sh/posts/wizardlike-picoctf-2022-writeup/
- CTFtime: https://ctftime.org/writeup/32801
