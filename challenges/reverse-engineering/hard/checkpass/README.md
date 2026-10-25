# Checkpass - Reverse Engineering Hard (picoCTF 2021)

## Información del Reto
- **Puntos:** 320
- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento:** picoCTF 2021
- **Descripción:** "What is the password?"

## Análisis del Reto

El reto proporciona un binario compilado en Rust que valida una contraseña específica. La tarea es recuperar la contraseña correcta realizando ingeniería inversa del proceso de validación.

## Solución

### Estructura del Binario

El binario valida una contraseña de exactamente 41 caracteres con formato:
```
picoCTF{<contenido_secreto_de_33_caracteres>}
```

### Proceso de Validación

La validación ocurre en múltiples rondas de transformación:

1. **Formato inicial**: La contraseña debe tener exactamente 41 caracteres
2. **Extracción del núcleo**: Se extrae el contenido entre `{` y `}` (33 caracteres)
3. **Rondas de encriptación**: El núcleo se pasa a través de 4 rondas (0-3) de transformación
4. **Cada ronda aplica**:
   - Sustitución S-box (4 diferentes S-boxes disponibles)
   - Permutación/intercambio de posiciones de bytes
5. **Verificación final**: El resultado transformado se compara con valores esperados

### Técnica de Solución

El enfoque es invertir el proceso de encriptación:

1. **Extraer S-boxes**: Localizar en el binario las cuatro tablas de sustitución S-box
2. **Extraer permutaciones**: Identificar los arrays de permutación/intercambio
3. **Invertir transformaciones**: Trabajar hacia atrás desde los valores esperados
4. **Reconstruir la contraseña**: Aplicar las transformaciones inversas para recuperar el original

### Herramientas Necesarias

- **Ghidra** - Análisis estático del binario
- **radare2/r2** - Análisis dinámico y dumping de memoria
- **Python** - Script para invertir la lógica de encriptación

### Conceptos Clave

Este reto demuestra:
- **Encriptación iterativa**: Aplicación de múltiples rondas de transformación
- **S-boxes (Substitution boxes)**: Tablas de sustitución criptográfica
- **Permutaciones**: Reordenamiento de bytes
- **Ingeniería inversa de crypto**: Análisis de algoritmos criptográficos en binarios compilados
- **Timing side-channels**: El nombre "Checkpass" y la lógica sugieren potencial para análisis de tiempo de ejecución

## Flag

`picoCTF{t1mingS1deChann3l_gVQSfJxl3VPFGQ}`

## Notas Importantes

- El binario está compilado en Rust, lo que puede hacer que el análisis de decompiladores sea más desafiante
- Las S-boxes pueden estar inlineadas o en secciones específicas del binario
- Los valores de permutación están hardcodeados en el binario
- La solución requiere comprensión de criptografía básica y análisis binario

## Referencias
- [CTFtime.org - Checkpass Writeup](https://ctftime.org/writeup/27056)
- [Rust in Ghidra](https://ghidra-sre.org/)

## Archivos Importantes
- Binario: `checkpass` (ejecutable Rust)
- Flag núcleo: `t1mingS1deChann3l_gVQSfJxl3VPFGQ`

## Dificultad y Aprendizaje
- **Dificultad:** Hard (requiere conocimiento de criptografía y análisis binario)
- **Conceptos clave:** S-boxes, permutaciones, criptografía reversible, análisis de Rust
- **Tiempo estimado:** 60-90 minutos para usuarios experimentados
