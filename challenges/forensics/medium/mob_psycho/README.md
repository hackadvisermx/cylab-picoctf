# Forensics — Mob psycho

## Descripción
> **Prompt oficial del reto:** "Can you handle APKs?
>
> Download the android apk [here](https://challenge-files.cylabacademy.net/library/1a2a849001ba23ed7ff2d86cb2cf9422c1ca5aca5219bcb037ee4b75bbe3a868/mobpsycho.apk)."
>
> **Hints:**
> - "Did you know you can `unzip` APK files?"
> - "Now you have the whole host of shell tools for searching these files."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** NGIRIMANA Schadrack

## Solución
El reto proporciona un paquete de aplicación para Android (`mobpsycho.apk`). Los archivos `.apk` son contenedores en formato ZIP estándar que empaquetan el código fuente compilado (`classes.dex`), los manifiestos, los recursos estáticos y los certificados de la aplicación.

### Paso 1: Inspección de contenidos del archivo APK
Podemos examinar las entradas del archivo ZIP sin necesidad de decompiladores complejos (como JADX o Apktool), buscando archivos o cadenas que contengan la palabra "flag":

```bash
unzip -l mobpsycho.apk | grep -i flag
```

La búsqueda identifica un archivo de texto ubicado dentro de los recursos de la aplicación:
`res/color/flag.txt`

### Paso 2: Extracción y decodificación del contenido
Al extraer e inspeccionar el contenido de `res/color/flag.txt`, se observa una cadena en formato hexadecimal:

```bash
unzip -p mobpsycho.apk res/color/flag.txt
# 61636164656d797b...
```

Dado que `61636164656d79` corresponde en código ASCII a `academy`, convertimos la representación hexadecimal a texto plano utilizando `xxd` o Python:

```bash
# Decodificación directa con xxd
unzip -p mobpsycho.apk res/color/flag.txt | xxd -r -p

# O mediante un script rápido en Python
python3 -c "
import zipfile
with zipfile.ZipFile('mobpsycho.apk') as z:
    hex_data = z.read('res/color/flag.txt').strip().decode()
    print(bytes.fromhex(hex_data).decode())
"
```

El resultado revela la flag en formato plano: `academy{...}`.

## Notas adicionales
- En el desarrollo de aplicaciones para Android, el directorio `res/` alberga recursos estáticos organizados por tipos (animaciones, layouts, valores de color, etc.). En este caso, el autor colocó directamente el archivo del reto dentro de `res/color/` ocultando el contenido como una cadena hexadecimal.

## Referencias
- Reto: https://learn.cylabacademy.org/library/420
- Estructura de un paquete APK (Android Developers): https://developer.android.com/guide/components/fundamentals
