# General Skills — mus1c

## Descripción
> **Prompt oficial:** "I wrote you a song. Put it in the picoCTF{} flag format."
>
> El enlace "song" descarga un archivo `lyrics.txt` (ver copia local en esta carpeta).
>
> **Hints:**
> 1. Do you think you can master rockstar?

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny

## Solución
`lyrics.txt` no es una canción real: es código fuente en **Rockstar**, un lenguaje de programación esotérico diseñado para que el código parezca la letra de una canción de rock/power ballad (`Put`, `Knock ... down`, `Build ... up`, `shout`, literales poéticos como `Pico's a CTFFFFFFF`, etc.).

Para resolverlo hace falta un **intérprete real de Rockstar** — no tiene sentido intentar simularlo a mano, ya que las reglas de literales poéticos (el valor numérico se construye a partir de la longitud de cada palabra) y de pronombres (`It`, `This` refieren a la última variable nombrada) son fáciles de aplicar mal. Se usó el intérprete oficial online: **https://codewithrockstar.com/online** (Starship, la implementación de referencia).

Pasos:
1. Descargar `lyrics.txt`.
2. Pegar el contenido tal cual en el editor de https://codewithrockstar.com/online.
3. Ejecutar con el botón **Rock**.
4. El programa hace `shout` (imprime) de 14 valores numéricos, uno por línea — cada uno es un código ASCII.
5. Decodificar esos 14 números como caracteres ASCII y concatenarlos; ese texto es lo que va **dentro** de las llaves de `picoCTF{...}` (el propio programa no imprime el prefijo `picoCTF{`, ya que el enunciado pide explícitamente darle ese formato).

```bash
# Salida del intérprete (una por línea):
# 114 114 114 111 99 107 110 114 110 48 49 49 51 114
python3 -c "
vals = [114,114,114,111,99,107,110,114,110,48,49,49,51,114]
print(''.join(chr(v) for v in vals))
"
# -> rrrocknrn0113r
```

Flag: `picoCTF{rrrocknrn0113r}`

## Notas adicionales
- No hizo falta instancia (`Launch Instance`) para este reto — es puramente offline/estático, solo el archivo descargable.
- Intentar reimplementar un intérprete de Rockstar a mano (o instalarlo vía `npm`/`pip`) resultó más lento y propenso a errores que usar directamente el intérprete oficial online, que carga vía WebAssembly y no requiere cuenta ni instalación.
- El nombre del reto ("mus1c") y el estilo del código (variables "song", "lyric", verbos "shout", "build up", "knock down") son un guiño a que Rockstar está diseñado para parecer letras de canciones de rock — es la pista principal para identificar el lenguaje sin más contexto.

## Referencias
- Reto: https://learn.cylabacademy.org/library/15
- Archivo fuente: `lyrics.txt` (copia en esta carpeta)
- Intérprete usado: https://codewithrockstar.com/online
- Especificación de Rockstar: https://codewithrockstar.com/docs
