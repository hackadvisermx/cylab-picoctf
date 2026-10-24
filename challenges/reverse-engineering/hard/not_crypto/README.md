# not crypto - Reverse Engineering Hard (picoMini by redpwn)

## Información del Reto
- **Puntos:** 150
- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Challenge ID:** 222
- **Evento:** picoMini by redpwn 2021
- **Autor:** asphyxia
- **Usuarios resueltos:** 2307
- **Hint:** "there's crypto in here but the challenge is not crypto"

## Descripción
El nombre del reto es engañoso: aunque sugiere que involucra criptografía, en realidad es un desafío de ingeniería inversa que explota las optimizaciones agresivas del compilador. El binario compilado carece de un `main` method visible, lo que complica el análisis estático con Ghidra.

## Solución

### Análisis Inicial

El archivo binario es un ejecutable ELF compilado con optimizaciones agresivas. Cuando se intenta analizarlo con Ghidra, resulta ser muy difícil localizando la función `main` debido a las optimizaciones del compilador que eliminan símbolos y reordenan el código.

### Enfoque: Análisis Dinámico con GDB

En lugar de intentar entender toda la lógica del programa a través del análisis estático, la solución aprovecha el análisis dinámico:

1. **Descarga del binario**
   - El binario `not_crypto` está disponible en la instancia de picoCTF
   - Se puede descargar mediante la interfaz web o acceso directo

2. **Análisis con Ghidra**
   - Importar el binario en Ghidra
   - Notar la ausencia de `main` method visible
   - Reconocer que probablemente hay una comparación de strings usando `memcmp()`

3. **Debugging con GDB**
   - Abrir el binario en GDB: `gdb ./not_crypto`
   - Crear un breakpoint en `memcmp`: `break memcmp`
   - Ejecutar el programa: `run`
   - Proporcionar entrada arbitraria (cualquier string de prueba)
   - Cuando el programa se detiene en `memcmp`, inspeccionar los registros

4. **Extracción de la Flag**
   - Examinar el registro **RDI**, que típicamente contiene el primer argumento a `memcmp()`
   - El registro RDI contendrá la flag comparada por el programa
   - Imprimir el contenido: `x/s $rdi`

### Concepto Clave

Las optimizaciones agresivas del compilador (como `-O3`) pueden eliminar símbolos de debug, inline funciones, y restructurar el código de manera que dificulta el análisis estático tradicional. Sin embargo, en tiempo de ejecución, la flag aún debe estar presente en memoria para ser comparada.

El breakpoint en `memcmp()` nos permite capturar ese momento exacto donde la flag sin ofuscar está disponible en los registros del procesador antes de ser comparada.

## Técnicas Utilizadas
- Análisis estático de binarios ELF con Ghidra
- Debugging dinámico con GDB
- Inspección de registros x86-64
- Uso de breakpoints condicionales
- Comprensión de optimizaciones de compilador
- Reversión de binarios altamente optimizados

## Herramientas Requeridas
- **Ghidra** - Análisis estático de binarios
- **GDB** - Debugger GNU para análisis dinámico
- **file** - Identificar tipo de binario
- **objdump** - Análisis de estructura del binario

## Pasos de Ejecución

```bash
# 1. Descargar el binario desde picoCTF
wget <url_del_binario>

# 2. Hacer ejecutable
chmod +x not_crypto

# 3. Examinar con file
file not_crypto

# 4. Abrir en GDB
gdb ./not_crypto

# 5. Dentro de GDB
(gdb) break memcmp
(gdb) run
[Proporcionar entrada arbitraria]
[El programa se detiene en memcmp]
(gdb) x/s $rdi
[La flag se mostrará aquí]
```

## Flag
`picoCTF{...}` (ver creds.txt para la flag real)

## Referencias
- [Diana Lin - not-crypto Writeup](https://www.dianalin.me/blog/writeups/picomini-2021/not-crypto/)
- [Ghidra Documentation](https://ghidra-sre.org/)
- [GDB Manual](https://sourceware.org/gdb/documentation/)
- [Compiler Optimizations](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)

## Notas Importantes

### Por qué Ghidra Solo No Es Suficiente
Las optimizaciones del compilador transforman el binario de manera que:
- Eliminan símbolos de debug
- Reordenan instrucciones
- Inline funciones automáticamente
- Eliminan código "innecesario" (aunque sea crítico para el análisis)

### Por qué GDB Funciona
En tiempo de ejecución, el programa debe cumplir su función original, comparando la entrada del usuario con la flag. GDB nos permite:
- Pausar la ejecución en puntos específicos
- Inspeccionar el estado de la memoria y registros
- Acceder a datos que nunca fueron "guardados" en el binario de forma análoga

Este reto demuestra un principio importante: los compiladores modernos priorizan la velocidad y la eficiencia sobre la facilidad de reversión, lo que hace que el debugging dinámico sea crucial en algunos casos.

## Archivos Importantes
- `not_crypto` - Binario a analizar
- Registro RDI en el breakpoint de `memcmp()` - Contiene la flag

## Dificultad y Aprendizaje
- **Dificultad:** Hard (requiere conocimiento de reversión binaria avanzada)
- **Conceptos clave:** Optimizaciones de compilador, análisis dinámico, arquitectura x86-64
- **Tiempo estimado:** 30-45 minutos para usuarios experimentados
