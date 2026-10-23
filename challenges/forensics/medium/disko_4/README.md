# Forensics — DISKO 4

## Descripción
> **Prompt oficial del reto:** "Can you find the flag in this disk image?
> This time I deleted the file! Let see you get it now!
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/4642fdd92be0f083b557c67cba47484a62c74bfdf3a99153137b356902f5b13c/disko-4.dd.gz)."
>
> **Hints:**
> 1. How would you look for deleted files?

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Darkraicg492

## Solución
El reto proporciona un volcado de disco `disko-4.dd.gz` correspondiente a un sistema de archivos `FAT32`. El enunciado advierte que el archivo portador de la flag fue eliminado del sistema de archivos.

1. **Identificación del sistema de archivos:**
   - Se descomprime `disko-4.dd.gz`.
   - El comando `file disko4.dd` confirma una estructura `FAT (32 bit)`.

2. **Enumeración de archivos eliminados con The Sleuth Kit:**
   - La herramienta `fls` de The Sleuth Kit permite inspeccionar tanto archivos activos como entradas de directorio marcadas como eliminadas (indicadas con un asterisco `*`).
   - Al ejecutar `fls -r disko4.dd`, se localiza una entrada eliminada destacada en el directorio de logs:
     `+ r/r * 532021: dont-delete.gz`
   - El inodo / cluster asignado es `532021`.

3. **Recuperación del archivo eliminado:**
   - Utilizando la herramienta `icat` sobre el inodo `532021`, se extrae el flujo binario del archivo comprimido eliminado a `dont-delete.gz`.
   - Al descomprimir `dont-delete.gz` mediante `gzip -d` o Python, se obtiene directamente el texto plano que contiene la flag.

```bash
# 1. Descomprimir el volcado de disco
gzip -d disko-4.dd.gz

# 2. Listar archivos incluyendo eliminados (*)
fls -r disko-4.dd | grep "\*"
# + r/r * 522629:	messages
# + r/r * 532021:	dont-delete.gz

# 3. Extraer el archivo eliminado correspondiente al inodo 532021
icat disko-4.dd 532021 > dont-delete.gz

# 4. Descomprimir y leer la flag
gzip -dc dont-delete.gz
# Here is your flag
# academy{...}
```

## Notas adicionales
- Cuando un archivo es eliminado en sistemas de archivos FAT o ext, los datos del archivo raramente se sobrescriben de forma inmediata; el sistema simplemente marca la entrada en la tabla de asignación como disponible y desvincula el puntero de directorio. Mientras los clusters no sean reutilizados por nuevas escrituras, la recuperación forense de los datos (*file carving* o recuperación vía metadatos) es trivial.

## Referencias
- Reto: https://learn.cylabacademy.org/library/704
- Sleuthkit fls Documentation: https://wiki.sleuthkit.org/index.php?title=Fls
- FAT32 File System Specification: https://en.wikipedia.org/wiki/File_Allocation_Table#FAT32
