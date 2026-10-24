# Reverse Engineering — timer

## Descripción
> **Prompt oficial del reto:** "You will find the flag after analysing this apk. Download here."
>
> **Pistas oficiales:**
> 1. Decompile
> 2. mobsf or jadx

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** Loic Shema

## Solución
El reto proporciona un paquete de aplicación para Android (`timer.apk`).

### 1. Análisis del archivo APK
Un archivo `.apk` es en esencia un contenedor comprimido en formato ZIP que contiene recursos, manifiestos XML y el código compilado para la máquina virtual Dalvik/ART (`classes.dex`).

Al inspeccionar los archivos DEX contenidos dentro del APK o extraer sus cadenas de texto:

```bash
unzip -q timer.apk
strings classes*.dex | grep -E "academy|picoCTF"
```

O utilizando una herramienta de descompilación como `jadx` para decompilar el archivo DEX a código Java legible:

```bash
jadx -d out timer.apk
grep -rn "academy{" out/
```

### 2. Extracción de la bandera
En el archivo `classes3.dex`, la cadena de la bandera se encuentra directamente almacenada en texto claro dentro de los recursos estáticos de la aplicación. Al consultarla mediante un script en Python:

```python
import zipfile
import re

with zipfile.ZipFile('timer.apk') as z:
    for name in z.namelist():
        if name.endswith('.dex'):
            data = z.read(name)
            match = re.search(rb'academy\{[^}]+\}', data)
            if match:
                print("Encontrada en", name, ":", match.group(0).decode())
```

El resultado revela la bandera en formato `academy{...}`.

## Notas adicionales
- En auditorías de seguridad en Android, la búsqueda inicial de cadenas y secretos en los archivos `.dex` sin ofuscación (ProGuard/R8) es una de las primeras comprobaciones para identificar llaves o credenciales quemadas (*hardcoded secrets*).

## Referencias
- Reto: https://learn.cylabacademy.org/library/381
- JADX decompiler: https://github.com/skylot/jadx
