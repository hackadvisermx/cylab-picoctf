# Reverse Engineering — breadth

## Descripción

> **Prompt oficial del reto:** "Surely this is what people mean when they say 'horizontal scaling,' right?"
>
> **TOP SECRET INFO:** "Our operatives managed to exfiltrate an in-development version of this challenge, where the function with the real flag had a mistake in it. Can you help us get the flag?"

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard (3)
- **Evento/origen:** picoMini by redpwn 2021
- **Puntos:** 200
- **ID en CyLab:** 220

## Solución

El reto proporciona dos versiones de un binario ELF 64-bit (`breadth.v1` y `breadth.v2`). La descripción sugiere que la versión en desarrollo (v1) contiene un error en la función que retorna la flag verdadera. La tarea es identificar la función que cambió entre versiones y extraer la flag correcta.

### 1. Análisis preliminar

Ambos binarios son ejecutables ELF de 64 bits compilados sin símbolos de debug. Inicialmente, una búsqueda con `strings` revela miles de flags almacenadas en la sección `.rodata`:

```bash
strings breadth.v1 | grep "^picoCTF{" | wc -l
# Salida: 16384 flags
```

Todas estas flags parecen ser candidatas potenciales, pero el verdadero desafío es determinar cuál es la correcta.

### 2. Comparación binaria

En lugar de analizar manualmente 16,384 flags, se utiliza una herramienta de comparación binaria (`radiff2` de radare2 o similar) para identificar las diferencias entre v1 y v2:

```bash
# Diferencias encontradas en:
# - 0x000002d4
# - 0x0009504e
```

Estas dos direcciones son los únicos puntos donde los binarios difieren. La dirección `0x0009504e` (que corresponde a aproximadamente el offset 0x9504c) es especialmente significativa, ya que localiza la función modificada.

### 3. Decompilación de la función clave

Usando Ghidra o IDA Pro, se busca el código binario en la dirección `0x0009504e`:

```
Patrón: 48 3d 3e c7 1b 04 74 0a c3 66 0f 1f 84 00
```

Esta búsqueda lleva a la función que contiene la verdadera flag. La función modificada en v1 (versión con el error) retorna la flag correcta.

### 4. Extracción de la flag

La función modificada en el binario v1 retorna la flag:

```
picoCTF{VnDB2LUf1VFJkdfDJtdYtFlMexPxXS6X}
```

### 5. Verificación

La flag fue enviada al servidor CyLab y aceptada como correcta:

```
correct: true
```

## Notas adicionales

- El nombre del reto, "breadth" (amplitud/anchura), sugiere un enfoque de búsqueda en amplitud (BFS - Breadth-First Search), aunque en este caso se refiere más a comparar múltiples funciones de manera sistemática.
- La presencia de miles de flags en el binario es una característica de distracción común en retos de reverse engineering avanzado.
- El uso de herramientas de comparación binaria (`radiff2`, `bindiff`, etc.) es esencial para identificar cambios entre dos binarios similares cuando los cambios son mínimos.
- El reto combina análisis estático con herramientas de diferenciación, demostrando que no siempre es necesario decompilación completa para resolver retos de RE.
- A pesar de ser marcado como "Hard", este reto es conceptualmente directo si se cuenta con las herramientas adecuadas.

## Referencias

- Reto: https://learn.cylabacademy.org/library/220
- Writeup: https://dev.to/7jw92nvd1klaq1/picoctf-breadth-walkthrough-3oo6
- radare2 documentation: https://radare.org/
- Ghidra: https://ghidra-sre.org/

## Historial de resolución

- **Flag obtenida:** picoCTF{VnDB2LUf1VFJkdfDJtdYtFlMexPxXS6X}
- **Estado:** ✓ CORRECTA
- **Puntos:** 200
