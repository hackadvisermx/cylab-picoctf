# droids1 - Reverse Engineering Hard (picoCTF 2019)

## Información del Reto
- **Puntos:** 400
- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Challenge ID:** 7
- **Evento:** picoCTF 2019
- **Autor:** Jason
- **Descripción:** "Find the pass, get the flag"

## Análisis del Reto

El reto proporciona un archivo APK (aplicación Android) llamado `one.apk`. La tarea es encontrar la contraseña correcta, ingresarla en la aplicación, y obtener la flag.

## Solución

### Paso 1: Descargar y Descompilar

```bash
# Descompilar el APK con JADX
jadx-gui one.apk
```

### Paso 2: Localizar la Autenticación

En JADX, explorar la aplicación y encontrar `MainActivity.java`:
- Buscar métodos que validen entrada de usuario
- Encontrar la lógica de autenticación
- Buscar la variable de contraseña

### Paso 3: Encontrar la Contraseña

La contraseña se encuentra en los recursos de la aplicación (strings.xml) o en el código:
- Navegando a `res/values/strings.xml` en la vista de recursos decompilados
- O buscando `R.string.password` en el código

**Contraseña:** `opossum`

### Paso 4: Obtener la Flag

1. Ejecutar el APK en un emulador Android o en Android Studio
2. Ingresar la contraseña `opossum`
3. Hacer clic en el botón
4. La flag se mostrará en la pantalla

### Explicación Técnica

El código decompilado revela:
- Una actividad que solicita entrada de usuario
- Una comparación de la entrada con una contraseña almacenada en los recursos
- Un método que genera o devuelve la flag cuando la contraseña es correcta

### Conceptos Clave

- **Decompilación de Android**: Extraer código fuente de APK
- **Resource Strings**: Almacenamiento de strings en archivos de recursos XML
- **Autenticación básica**: Validación de contraseña
- **APK Execution**: Ejecutar aplicaciones en emuladores

## Flag

`picoCTF{pining.for.the.fjords}`

## Herramientas Requeridas

- **JADX** - Decompilador Java/Android
- **Android Studio** - Emulador y IDE
- **apktool** - Descompilación alternativa
- **Text Editor** - Para buscar strings

## Pasos de Ejecución

```bash
# 1. Descompilar
jadx-gui one.apk

# 2. Buscar MainActivity y la lógica de autenticación
# En JADX: Ctrl+Shift+F para búsqueda global
# Buscar: "password" o "opossum"

# 3. Ejecutar en emulador
# Abrir Android Studio > AVD Manager > Ejecutar emulador
# Instalar APK: adb install one.apk

# 4. Ejecutar aplicación y usar contraseña
```

## Notas Importantes

- La contraseña es literal en los recursos o código
- No requiere decryption o algoritmos complejos
- Es un buen ejemplo de falla de seguridad: hardcodear contraseñas en APK
- Más complejo que droids0 pero aún introductorio

## Dificultad y Aprendizaje
- **Dificultad:** Hard (requiere análisis de recursos Android)
- **Conceptos clave:** Decompilación, strings.xml, autenticación
- **Tiempo estimado:** 20-40 minutos

## Información de Resolución
- Método: Decompilación con JADX + búsqueda de recursos
- Complejidad: Media-baja
- Herramienta principal: JADX
