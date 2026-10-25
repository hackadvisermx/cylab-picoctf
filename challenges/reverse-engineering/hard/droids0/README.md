# droids0 - Reverse Engineering Hard (picoCTF 2019)

## Información del Reto
- **Puntos:** 300
- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Challenge ID:** 6
- **Evento:** picoCTF 2019
- **Autor:** Jason
- **Descripción:** "Where do droid logs go"

## Análisis del Reto

El reto proporciona un archivo APK (aplicación Android) llamado `zero.apk`. La tarea es ejecutar la aplicación Android y encontrar la flag que se muestra en los logs de la aplicación.

## Solución

### Paso 1: Descargar y Preparar el APK

```bash
# El archivo zero.apk está disponible en la plataforma
unzip zero.apk
ls
```

### Paso 2: Analizar con Android Studio o Emulador

La aplicación es una aplicación Android simple que muestra la flag en los logs cuando se ejecuta.

### Paso 3: Extraer Logs

Opciones:
1. **Con Android Emulator + Android Studio:**
   - Ejecutar la aplicación en el emulador
   - Ver los logs en Logcat
   - La flag aparecerá en los logs

2. **Con apktool/JADX:**
   - Descompilar el APK: `apktool d zero.apk`
   - Buscar strings o logs en el código

### Opción Preferida: Decompilación

```bash
# Usar JADX para decompilación GUI
jadx-gui zero.apk
# O usar apktool
apktool d zero.apk
# Buscar la flag en los recursos o strings
grep -r "picoCTF" ./zero/
```

### Conceptos Clave

- **Logcat**: Sistema de logging de Android
- **APK Decompilation**: Análisis de aplicaciones Android
- **Android Studio**: Desarrollo e inspección de aplicaciones Android
- **JADX/apktool**: Herramientas de reversión de APK

## Flag

`picoCTF{a.moose.once.bit.my.sister}`

## Herramientas Requeridas

- **Android Emulator o dispositivo físico** (opcional, para ejecución)
- **JADX** - Decompilador Java/Android
- **apktool** - Herramienta de descompilación de APK
- **Android Studio** - IDE de desarrollo Android
- **grep/strings** - Búsqueda de strings

## Notas Importantes

- Esta es la primera aplicación Android del conjunto droids
- La flag está presente en los logs de la aplicación
- No requiere código native o complejidad avanzada
- Es un buen ejercicio introductorio en reversión de Android

## Dificultad y Aprendizaje
- **Dificultad:** Hard (requiere conocimiento de Android)
- **Conceptos clave:** APK, Logcat, decompilación de Android
- **Tiempo estimado:** 15-30 minutos

## Información de Resolución
- Método: Decompilación y análisis de logs
- Complejidad: Baja (comparado con otros droids)
- Herramienta principal: JADX o apktool
