# Forensics — Trivial Flag Transfer Protocol

## Descripción
> **Prompt oficial del reto:** "Figure out how they moved the flag.
> [tftp.pcapng](https://challenge-files.cylabacademy.net/library/c867f9c01ef11f33b38ca48b413b5b9b3067891682c49225c0cc97c32bcb4082/tftp.pcapng)"
>
> **Hints:**
> - "What are some other ways to hide data?"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Danny

## Solución
El reto proporciona una captura de tráfico de red en formato `.pcapng` (`tftp.pcapng`). El nombre del reto hace alusión al protocolo **TFTP** (*Trivial File Transfer Protocol*, UDP/69), un protocolo ligero de transferencia de archivos sin autenticación ni cifrado en tránsito.

### Paso 1: Extracción de objetos TFTP
Podemos inspeccionar los archivos transferidos utilizando la funcionalidad *Export Objects $\rightarrow$ TFTP* de Wireshark, o mediante `tshark`:

```bash
tshark -r tftp.pcapng --export-objects "tftp,extracted_files"
```

El proceso recupera 6 archivos transferidos:
1. `instructions.txt`
2. `plan`
3. `program.deb`
4. `picture1.bmp`
5. `picture2.bmp`
6. `picture3.bmp`

### Paso 2: Análisis de los mensajes cifrados
Inspeccionamos el contenido de `instructions.txt`:
```text
GSGCQBRFAGRAPELCGBHEROTAppropriate...
```
Aplicando un descifrado César (ROT13), el mensaje se lee:
> *"TFTPDOESNTENCRYPTOURTRAFFICSOWEMUSTFLAGDUTYCHECKOURFLAG"*

Inspeccionamos el archivo `plan`:
```text
VHFRQOQERHAGRAPELC...
```
Tras descifrarlo con ROT13 / César, el plan revela la técnica y la contraseña utilizada:
> *"IUSEDTHEPROGRAMANDHIDITWITH-DUEDILIGENCE.CHECKOUTTHEPHOTOS"*

La clave indicada es `DUEDILIGENCE`.

### Paso 3: Identificación del software y extracción esteganográfica
Examinamos el paquete Debian transferido `program.deb`:
```bash
dpkg-deb -I program.deb
# Package: steghide
```
El archivo transferido corresponde a la herramienta de esteganografía **`steghide`**. Esto confirma que los datos fueron incrustados dentro de alguna de las imágenes BMP mediante `steghide` usando la contraseña `DUEDILIGENCE`.

Probamos extraer información oculta en cada imagen BMP:
```bash
steghide extract -sf picture1.bmp -p DUEDILIGENCE
steghide extract -sf picture2.bmp -p DUEDILIGENCE
steghide extract -sf picture3.bmp -p DUEDILIGENCE
```

En `picture3.bmp`, `steghide` extrae exitosamente el archivo incrustado `flag.txt`:
```text
wrote extracted data to "flag.txt".
```

Al leer `flag.txt` se obtiene la flag del reto.

## Notas adicionales
- TFTP opera sobre UDP mediante bloques numerados de datos (*DATA/ACK*). Al no cifrar el canal, todo el contenido de los archivos y nombres transferidos es completamente visible para cualquier analista con visibilidad del tráfico.
- La combinación de tráfico no autenticado con técnicas de esteganografía LSB en formatos gráficos estándar (como BMP) es un patrón clásico de evasión de DLP (*Data Loss Prevention*).

## Referencias
- RFC 1350: The TFTP Protocol (Revision 2)
- Steghide Documentation: http://steghide.sourceforge.net/
