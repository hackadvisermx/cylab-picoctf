# Forensics — B1g_Mac

## Descripción
> **Prompt oficial del reto:** "Here's a [zip file](https://challenge-files.cylabacademy.net/library/77695762a74381ca12a69932aab6c7a22e4dc95de92d0056f13a315ac133833b/b1g_mac.zip)."

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Santiago C

## Solución
El reto proporciona un archivo ZIP que contiene un binario de Windows (`main.exe`) y un directorio `test` con imágenes BMP copiadas y originales (`Item01.bmp`, `Item01 - Copy.bmp`, etc.).

1. **Análisis del nombre y del binario:**
   - El título "B1g_Mac" es un juego de palabras que hace referencia directa a los tiempos **MAC** (*Modification, Access, Creation*) del sistema de archivos NTFS en Windows.
   - En Windows, la estructura `FILETIME` almacena marcas de tiempo como enteros de 64 bits que cuentan intervalos de 100 nanosegundos transcurridos desde el 1 de enero de 1601.
   - Al desensamblar `main.exe` con Ghidra o IDA Pro, se observan dos funciones clave: una para ocultar información (`_hideInFile` / `_listdir`) y otra función que decodifica (`_decode`).
   - El binario oculta los bytes de la flag en los campos de menor peso de las marcas de tiempo de los archivos de imagen mediante llamadas a la API de Windows `SetFileTime`.

2. **Extracción Forense:**
   - La función `_decode` existente en el ejecutable puede ejecutarse desviando el puntero de instrucción (`EIP`) en un depurador (como `x32dbg`).
   - Alternativamente, se extraen las marcas de tiempo de modificación de alta precisión de cada archivo `.bmp` en el orden correspondiente. Los dos últimos bytes de los enteros `FILETIME` de cada archivo corresponden secuencialmente a los caracteres de la flag.

```bash
# 1. Descomprimir el archivo conservando marcas de tiempo exactas (e.g. con 7z)
7z x b1g_mac.zip

# 2. En un entorno de depuración (x32dbg), cargar main.exe
# Colocar un breakpoint en la llamada de codificación y cambiar EIP a la dirección de _decode
# Ejecutar para que la función de decodificación imprima la bandera en consola
```

## Notas adicionales
- Al descomprimir archivos en retos basados en metadatos temporales de sistemas de archivos, es crucial utilizar herramientas como `7z` o preservar las marcas de tiempo sin modificarlas al acceder a ellas.

## Referencias
- Reto: https://learn.cylabacademy.org/library/56
- Microsoft Docs - FILETIME structure: https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-filetime
