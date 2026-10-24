# Forensics — MacroHard WeakEdge

## Descripción
> **Prompt oficial del reto:** "I've hidden a flag in this file. Can you find it?
> [Forensics_is_fun.pptm](https://challenge-files.cylabacademy.net/library/ef35dfe613527d28fe872d94179b53bc1a0497ddecf57e51d160c910be3a8e8a/Forensics_is_fun.pptm)"
>
> **Hints:** Ninguna

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** madStacks

## Solución
El reto proporciona un archivo con extensión `.pptm` (*Microsoft PowerPoint Macro-Enabled Presentation*). Los formatos modernos de Microsoft Office (OOXML) son en realidad archivos comprimidos en formato ZIP con una jerarquía predefinida de directorios XML y recursos binarios.

### Paso 1: Inspección del paquete ZIP
Podemos descomprimir el archivo o examinar su listado de ficheros utilizando herramientas estándar como `unzip` o Python:

```bash
unzip -l Forensics_is_fun.pptm
```

Entre la estructura interna de diapositivas y macros (`ppt/vbaProject.bin`), destaca un archivo con nombre inusual:
`ppt/slideMasters/hidden`

### Paso 2: Análisis del archivo oculto
Al leer el contenido de `ppt/slideMasters/hidden`:

```bash
unzip -p Forensics_is_fun.pptm ppt/slideMasters/hidden
# Z m x h Z z o g Y W N h Z G V t e X t E M W R f d V 9 r b j B 3 X 3 B w d H N f c l 9 6 M X A 1 f Q
```

Se observa una cadena en Base64 cuyos caracteres se encuentran intercalados con espacios en blanco.

### Paso 3: Decodificación
Eliminamos los espacios en blanco y decodificamos la cadena Base64 resultante:

```bash
unzip -p Forensics_is_fun.pptm ppt/slideMasters/hidden | tr -d ' ' | base64 -d
# flag: academy{...}
```

La cadena decodificada revela directamente la flag del reto.

## Notas adicionales
- El título del reto es un juego de palabras fonético (*MacroHard WeakEdge* $\rightarrow$ *Microsoft PowerPoint*).
- Los archivos OOXML permiten incluir archivos y recursos arbitrarios dentro de su árbol de carpetas que PowerPoint simplemente ignora si no están declarados en los archivos `.rels`, lo que facilita ocultar información sin alterar el funcionamiento del documento.

## Referencias
- Reto: https://learn.cylabacademy.org/library/130
- Office Open XML File Formats: https://en.wikipedia.org/wiki/Office_Open_XML
