# droids4 - Reverse Engineering Hard (picoCTF 2019)

## Información del Reto
- **Puntos:** 700
- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Challenge ID:** 10
- **Evento:** picoCTF 2019
- **Autor:** Jason
- **Descripción:** "reverse the pass, patch the file, get the flag"

## Análisis del Reto

El reto proporciona un archivo APK (aplicación Android) llamado `four.apk`. Este es el más desafiante de la serie: requiere reversión de un algoritmo obfuscado para encontrar la contraseña, seguido de parching del APK.

## Solución

### Paso 1: Descompilar el APK

```bash
# Descompilar con JADX primero para análisis
jadx-gui four.apk

# También descompilar con apktool para edición smali
apktool d four.apk -o four_decompiled
```

### Paso 2: Analizar la Lógica de Contraseña

En JADX, buscar métodos que construyan o validen la contraseña:

El código obfuscado probablemente:
- Usa StringBuilder para construir la contraseña dinámicamente
- Aplica manipulaciones de caracteres (shifts, swaps, etc.)
- Contiene múltiples capas de ofuscación

Ejemplo de lógica típica:
```java
StringBuilder password = new StringBuilder();
password.append((char) ('a' + 14)); // 'o'
password.append((char) ('l' - 2));  // 'j'
// ... más manipulaciones
```

### Paso 3: Reconstruir la Contraseña

Analizando el código obfuscado, extraer cada carácter manipulado:
- Seguir cada operación de carácter
- Reconstruir la cadena resultante
- Verificar con los patrones de ofuscación

**Contraseña descubierta:** `alphabetsoup`

### Paso 4: Parchar el APK (Parte Crítica)

El reto requiere parching similar a droids3, pero más complejo:

```bash
# Editar los archivos smali
cd four_decompiled/smali

# Buscar la llamada al método native cardamom
# Encontrar algo como:
# invoke-static {p0}, Lcom/picoctf/FourActivity;->cardamom()Ljava/lang/String;

# Este método cardamom es probablemente native (JNI)
# Necesitamos hacer que sea llamado en lugar del return anterior
```

### Paso 5: Modificación Smali Específica

El reto menciona "patch the file":
- Necesitamos cambiar la lógica para que llame a un método diferente
- O modificar el flujo de control para que use `cardamom()` en lugar de otra función
- La función `cardamom` probablemente es un método native que devuelve información adicional

```bash
# Recompilar
apktool b four_decompiled -o four_modified.apk

# Firmar
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore my.keystore four_modified.apk my-key-alias

# Ejecutar
adb install four_modified.apk
```

### Conceptos Clave

- **Ofuscación de código**: Técnicas para hacer código difícil de entender
- **StringBuilder**: Construcción dinámica de strings
- **Manipulación de caracteres**: Operaciones matemáticas en valores ASCII
- **Métodos nativos (JNI)**: Llamadas a código compilado (C/C++)
- **Reverse engineering avanzado**: Análisis de algoritmos compilados y ofuscados

### Técnica de Análisis

1. **Identificar ofuscación**: Reconocer patrones de ofuscación típicos
2. **Desofuscar manualmente**: Evaluar manualmente las operaciones
3. **Escribir script**: Crear un script Python para automatizar la reversión
4. **Verificar resultado**: Confirmar que la contraseña es válida

## Flag

`picoCTF{not.particularly.silly}`

## Contraseña

`alphabetsoup`

## Herramientas Requeridas

- **JADX** - Análisis de código obfuscado
- **apktool** - Modificación de APK
- **keytool/jarsigner** - Firma de APK
- **Python** - Script para análisis de obfuscación
- **Android Studio** - Emulación

## Ejemplo de Script de Reversión (Python)

```python
# Script para ayudar a desofuscar la contraseña
# Basado en patrones típicos

def reverse_password():
    chars = []
    # Seguir cada operación del código
    chars.append(chr(ord('a') + 14))  # 'o'
    chars.append(chr(ord('l') - 2))   # 'j'
    # ... más caracteres según el patrón
    return ''.join(chars)

password = reverse_password()
print(f"Contraseña: {password}")
```

## Notas Importantes

- Droids4 es el más desafiante del conjunto
- Requiere reversión de algoritmos obfuscados
- La contraseña NO es obvia y requiere análisis cuidadoso
- El parching es similar a droids3 pero el análisis es más complejo
- Puede ser necesario escribir scripts para automatizar el análisis

## Dificultad y Aprendizaje
- **Dificultad:** Hard+ (requiere conocimiento avanzado)
- **Conceptos clave:** Ofuscación, ingeniería inversa avanzada, JNI, smali
- **Tiempo estimado:** 90-180 minutos

## Información de Resolución
- Método: Decompilación + análisis de ofuscación + parching + firma
- Complejidad: Alta
- Herramientas principales: JADX, apktool, Python
