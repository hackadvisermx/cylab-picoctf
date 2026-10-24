# Reverse Engineering — M1n10n'5_53cr37

## Descripción
> **Prompt oficial del reto:** "Get ready for a mischievous adventure with your favorite Minions! 🕵️‍♂️💥 They’ve been up to their old tricks, and this time, they've hidden the flag in a devious way within the Android source code. Your task is to channel your inner Minion and dive into the disassembled or decompiled code. Watch out, because these little troublemakers have hidden the flag in multiple sneaky spots or maybe even pulled a fast one and concealed it in the same location!
>
> Put on your overalls, grab your magnifying glass, and get cracking. The Minions have left clues, and it's up to you to follow their trail and uncover the flag. Can you outwit these playful pranksters and find their secret? Let the Minion mischief begin!
> Find the android apk here [Minions Mobile Application](https://challenge-files.cylabacademy.net/library/d10acd738363d35dcd0e677988ff9677f78f102bd27b2b72d985f53718b8ddd5/minions.apk) and try to get the flag."
>
> **Pistas oficiales:**
> 1. Do you know how to disassemble an apk file?
> 2. Any interesting source files?

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoMini by CMU-Africa
- **Autor:** Prince Niyonshuti N.

## Solución
El reto proporciona un archivo APK de Android llamado `minions.apk`. Dado que un APK es un archivo ZIP comprimido, se descomprime para inspeccionar sus recursos y código compilado:

```bash
unzip minions.apk -d apk_extracted/
```

### 1. Inspección de recursos y layouts
Examinando los archivos de diseño en `res/layout/activity_main.xml` o las cadenas compiladas en `resources.arsc`:
- Se encuentra un atributo de texto que indica una pista explícita:
  `"Look into me my Banana Value is interesting"`
- El atributo `Banana` en los recursos de la aplicación contiene una cadena codificada en Base32:
  `OBUWG32DKRDHWMLUL53TI43OG5PWQNDSMRPXK3TSGR3DG3BRNY4V65DIGNPW2MDCGFWDGX3DGBSDG7I=`

### 2. Decodificación en Base32
Al decodificar la cadena Base32:

```bash
echo "OBUWG32DKRDHWMLUL53TI43OG5PWQNDSMRPXK3TSGR3DG3BRNY4V65DIGNPW2MDCGFWDGX3DGBSDG7I=" | base32 -d
```

O en Python:
```python
import base64

b32_str = "OBUWG32DKRDHWMLUL53TI43OG5PWQNDSMRPXK3TSGR3DG3BRNY4V65DIGNPW2MDCGFWDGX3DGBSDG7I="
flag = base64.b32decode(b32_str).decode('utf-8')
print(flag)
```

Salida:
```text
picoCTF{...}
```
En la plataforma CyLab Academy, la bandera se envía bajo el prefijo `academy{...}`:
```text
academy{...}
```

## Notas adicionales
- Al analizar aplicaciones Android, los archivos de recursos binarios (`resources.arsc` y archivos XML compilados) frecuentemente contienen cadenas estáticas o secretos ofuscados que no requieren descompilar el bytecode Dalvik (`classes.dex`).

## Referencias
- Reto: https://learn.cylabacademy.org/library/528
- Android Application Package (APK): https://developer.android.com/guide/components/fundamentals
- RFC 4648 Base32 Encoding: https://datatracker.ietf.org/doc/html/rfc4648#section-6
