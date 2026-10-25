# droids3 - Reverse Engineering Hard (picoCTF 2019)

## Información del Reto
- **Puntos:** 600
- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Challenge ID:** 9
- **Evento:** picoCTF 2019
- **Autor:** Jason
- **Descripción:** "Find the pass, get the flag"
- **Hint:** "make this app your own"

## Análisis del Reto

El reto proporciona un archivo APK (aplicación Android) llamado `three.apk`. Este es más complejo que los anteriores: requiere no solo encontrar la contraseña sino también modificar/parchar la aplicación para obtener la flag.

## Solución

### Paso 1: Descompilar el APK

```bash
# Descompilar con apktool (mejor para edición)
apktool d three.apk -o three_decompiled
cd three_decompiled
```

### Paso 2: Analizar la Lógica

Buscar en el código de la aplicación:
- Método `getFlag()` o similar
- Métodos `yep()` y `nope()`
- Lógica de validación

La aplicación probablemente tiene:
- Una función `nope()` que devuelve algo incorrecto
- Una función `yep()` que devuelve la flag correcta
- Lógica de validación que llama a `nope()` cuando falla

### Paso 3: Parchar el APK (Smali Modification)

El hint "make this app your own" sugiere que necesitamos modificar el APK:

```bash
# Editar el archivo smali en three_decompiled/smali
# Encontrar la llamada a nope() en el método de validación
# Cambiarla para que llame a yep() en su lugar

# Los archivos smali están en: three_decompiled/smali/
# Ejemplo de ruta: three_decompiled/smali/com/picoctf/MainActivity.smali

# En el archivo smali, encontrar:
# invoke-virtual {p0}, Lcom/picoctf/MainActivity;->nope()V
# y cambiarla a:
# invoke-virtual {p0}, Lcom/picoctf/MainActivity;->yep()V
```

### Paso 4: Recompilar el APK

```bash
# Recompilar el APK modificado
apktool b three_decompiled -o three_modified.apk

# Firmar el APK
# Crear un keystore si no existe
keytool -genkey -v -keystore my-release-key.keystore -keyalg RSA \
  -keysize 2048 -validity 10000 -alias my-key-alias

# Firmar el APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore my-release-key.keystore three_modified.apk my-key-alias
```

### Paso 5: Ejecutar el APK Modificado

```bash
# Instalar y ejecutar en emulador
adb install three_modified.apk
```

### Conceptos Clave

- **Smali Code**: Bytecode de Dalvik (lenguaje de bajo nivel de Android)
- **APK Modification**: Edición de aplicaciones compiladas
- **Code Patching**: Cambio de instrucciones en bytecode
- **APK Signing**: Firma digital de APK
- **Decompilation/Recompilation**: Ciclo de modificación de APK

## Flag

`picoCTF{tis.but.a.scratch}`

## Herramientas Requeridas

- **apktool** - Descompilación/recompilación de APK (mejor que JADX para esto)
- **keytool** - Creación de keystores
- **jarsigner** - Firma de APK
- **Android Studio** - Emulación
- **Text Editor** - Edición de archivos smali

## Pasos de Ejecución Completo

```bash
# 1. Descompilar
apktool d three.apk

# 2. Editar archivos smali
# Buscar MainActivity.smali
nano three/smali/com/picoctf/MainActivity.smali

# 3. Cambiar la lógica (nope → yep)

# 4. Recompilar
apktool b three -o three_modified.apk

# 5. Firmar
keytool -genkey -v -keystore my.keystore -keyalg RSA -keysize 2048 -validity 10000
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore my.keystore three_modified.apk my-key-alias

# 6. Instalar y ejecutar
adb install three_modified.apk
```

## Notas Importantes

- Este reto requiere modificación de bytecode Smali
- El hint "make this app your own" es clave: debes modificar/parchar el APK
- La firma digital es necesaria para instalar un APK modificado
- Más complejo que droids0-2

## Dificultad y Aprendizaje
- **Dificultad:** Hard (requiere conocimiento de smali y APK patching)
- **Conceptos clave:** Smali, patching, signing, Android internals
- **Tiempo estimado:** 45-90 minutos

## Información de Resolución
- Método: Decompilación + modificación smali + recompilación + firma
- Complejidad: Media-Alta
- Herramienta principal: apktool
