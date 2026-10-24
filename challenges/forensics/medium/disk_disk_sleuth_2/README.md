# Forensics — Disk, disk, sleuth! II

## Descripción
> **Prompt oficial del reto:** "All we know is the file with the flag is named `down-at-the-bottom.txt`...
> [dds2-alpine.flag.img.gz](https://challenge-files.cylabacademy.net/library/ade553d24cb44d6821915085413245390e7e9c9e24a9e8154b1a7f1bc02a8410/dds2-alpine.flag.img.gz)"
>
> **Hints:**
> - "The sleuthkit has some great tools for this challenge as well."
> - "Sleuthkit docs here are so helpful: [TSK Tool Overview](http://wiki.sleuthkit.org/index.php?title=TSK_Tool_Overview)"
> - "This disk can also be booted with qemu!"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
El reto proporciona una imagen de disco comprimida de una distribución Alpine Linux (`dds2-alpine.flag.img.gz`) e indica que la flag reside dentro de un archivo con el nombre `down-at-the-bottom.txt`.

### Paso 1: Descompresión de la imagen
Descomprimimos el archivo `.gz` para obtener la imagen de disco en bruto:

```bash
gzip -d dds2-alpine.flag.img.gz
```

### Paso 2: Análisis con The Sleuth Kit (TSK) o 7-Zip
Para examinar el sistema de archivos Linux (ext4/ext3) dentro del contenedor MBR:

**Método A: The Sleuth Kit**
1. Identificamos el offset del sector de inicio de la partición Linux con `mmls`:
   ```bash
   mmls dds2-alpine.flag.img
   # Linux (0x83) inicia en el sector 2048 (offset = 2048 * 512 = 1048576)
   ```
2. Listamos recursivamente los archivos para ubicar el inodo correspondiente:
   ```bash
   fls -r -p -o 2048 dds2-alpine.flag.img | grep down-at-the-bottom.txt
   # r/r 18291: root/down-at-the-bottom.txt
   ```
3. Extraemos el contenido del inodo con `icat`:
   ```bash
   icat -o 2048 dds2-alpine.flag.img 18291
   ```

**Método B: Extracción directa con 7zz**
7-Zip es capaz de analizar la tabla de particiones MBR y el sistema de archivos ext en una sola operación:

```bash
7zz e dds2-alpine.flag.img "root/down-at-the-bottom.txt" -r
cat down-at-the-bottom.txt
```

El archivo contiene una representación en arte ASCII de los caracteres de la flag distribuidos en círculos alfanuméricos:
```text
   _     _     _     _     _  
  / \   / \   / \   / \   / \ 
 ( a ) ( c ) ( a ) ( d ) ( e ) ...
  \_/   \_/   \_/   \_/   \_/ 
```
Concatenando los caracteres se obtiene la flag del reto: `academy{...}`.

## Notas adicionales
- `mmls`, `fls` e `icat` forman el núcleo de herramientas forenses de *The Sleuth Kit* para análisis de discos sin necesidad de montar imágenes como dispositivos de bloque (`loop devices`), preservando la integridad forense del archivo de evidencia.

## Referencias
- Reto: https://learn.cylabacademy.org/library/137
- The Sleuth Kit Tool Overview: http://wiki.sleuthkit.org/index.php?title=TSK_Tool_Overview
