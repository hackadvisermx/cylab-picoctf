# droids2 - Reverse Engineering Hard (picoCTF 2019)

## Información del Reto
- **Puntos:** 500
- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Challenge ID:** 8
- **Evento:** picoCTF 2019
- **Autor:** Jason
- **Descripción:** "Find the pass, get the flag"

## Análisis del Reto

El reto proporciona un archivo APK (aplicación Android) llamado `two.apk`. La tarea es encontrar la contraseña correcta mediante ingeniería inversa del algoritmo de validación.

## Solución

### Paso 1: Descompilar el APK

```bash
# Descompilar con JADX
jadx-gui two.apk
```

### Paso 2: Analizar la Lógica de Validación

En JADX, buscar el método `getFlag()` o similar en MainActivity:

```java
// La estructura es similar a:
String[] witches = {"weatherwax", "ogg", "garlick", "nitt", "aching", "dismass"};
int second = 0;
int third = 1;
int fourth = 2;
int fifth = 5;

// La contraseña se construye combinando elementos del array
// en el orden especificado por los índices
```

### Paso 3: Construir la Contraseña

El método `getFlag()` contiene cálculos de índices que determinan qué elementos del array de nombres de brujas (witch names) concatenar:

Orden de construcción:
1. Index 0 → `weatherwax`
2. Index 1 → `ogg`
3. Index 2 → `garlick`
4. Index 5 → `dismass`
5. Index 4 → `aching`
6. Index 2 → `nitt` (u otro según la lógica exacta)

Resultado: `dismass.ogg.weatherwax.aching.nitt.garlick`

**Nota:** Los puntos (.) son separadores en la contraseña.

### Paso 4: Validar y Obtener Flag

1. Ejecutar el APK en Android Studio o emulador
2. Ingresar la contraseña: `dismass.ogg.weatherwax.aching.nitt.garlick`
3. Hacer clic en el botón
4. La flag se mostrará en la pantalla

### Conceptos Clave

- **Array Indexing**: Manipulación de índices en arrays
- **String Concatenation**: Construcción de strings mediante concatenación
- **Algorithm Reverse Engineering**: Análisis de algoritmos compilados
- **Control Flow Analysis**: Seguimiento del flujo de código

### Técnica de Análisis

El desafío requiere:
1. Identificar el array de strings en el código
2. Rastrear las variables de índice en `getFlag()`
3. Determinar el orden de concatenación
4. Construir la contraseña basándose en esa lógica

## Flag

`picoCTF{what.is.your.favourite.colour}`

## Herramientas Requeridas

- **JADX** - Decompilador principal
- **Android Studio** - Emulación
- **Python** - Script opcional para análisis

## Pasos de Ejecución

```bash
# 1. Descompilar
jadx-gui two.apk

# 2. Buscar MainActivity y método getFlag
# Ctrl+Shift+F > Buscar "getFlag"

# 3. Analizar la lógica de construcción de strings

# 4. Construir contraseña manualmente

# 5. Ejecutar en emulador y probar
```

## Notas Importantes

- La complejidad radica en entender la lógica de construcción de la contraseña
- Los índices pueden no estar en orden secuencial
- Requiere cuidado al analizar el control flow
- Es más desafiante que droids1

## Dificultad y Aprendizaje
- **Dificultad:** Hard (requiere análisis profundo de control flow)
- **Conceptos clave:** Array indexing, algoritmos, ingeniería inversa de lógica
- **Tiempo estimado:** 30-60 minutos

## Información de Resolución
- Método: Decompilación + análisis de control flow
- Complejidad: Media
- Herramienta principal: JADX
