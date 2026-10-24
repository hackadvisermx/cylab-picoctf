# Forensics — Weird File

## Descripción
> **Prompt oficial del reto:** "What could go wrong if we let Word documents run programs? (aka \"in-the-clear\").
> [weird.docm](https://challenge-files.cylabacademy.net/library/b99ccd7c322df5b671439cb3a077a65446b967013fe4a3036610b53e0d311bca/weird.docm)"
>
> **Hints:**
> - "https://www.youtube.com/watch?v=Y7IJjnLGqTQ"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** thelshell

## Solución
El reto proporciona un archivo con extensión `.docm` (`weird.docm`), correspondiente a un documento de Microsoft Word habilitado para macros (*Office Open XML Macro-Enabled Document*). Los archivos `.docm` son contenedores ZIP que almacenan las macros VBA compiladas en el archivo binario `word/vbaProject.bin`.

### Paso 1: Análisis estático de macros con olevba
Utilizamos la herramienta especializada `olevba` (de la suite `oletools`) para extraer e inspeccionar el código de Visual Basic for Applications (VBA) incrustado en el documento:

```bash
olevba weird.docm
```

Alternativamente, podemos descomprimir la estructura ZIP y examinar las cadenas del proyecto VBA:

```bash
unzip weird.docm -d weird_extracted
strings weird_extracted/word/vbaProject.bin | grep -i "academy{"
```

### Paso 2: Desofuscación del código VBA
Al inspeccionar el módulo de código extraído (función `AutoOpen()` o similar), encontramos rutinas de ejecución automática que construyen cadenas mediante concatenación de caracteres o llamadas a funciones del sistema (`Shell`, `WScript.Shell`):

```vba
Sub AutoOpen()
    ' Rutina de ejecución con la carga útil
    Dim cmd As String
    ...
End Sub
```

La rutina reconstruye y expone la cadena de texto plano con la flag del reto (`academy{...}`).

## Notas adicionales
- Los documentos de Office con macros maliciosas son uno de los vectores iniciales más prevalentes en ataques de phishing (*Initial Access* según MITRE ATT&CK T1566.001 / T1204.002).
- Para realizar análisis forense seguro de documentos Office sin ejecutar el entorno de Microsoft Word ni habilitar macros activas, el estándar de la industria es utilizar analizadores estáticos basados en Python como `oletools` (`olevba`, `mraptor`, `olebrowse`).

## Referencias
- Oletools Documentation: https://github.com/decalage2/oletools
- MITRE ATT&CK T1059.005: Visual Basic for Applications
