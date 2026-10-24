# Reverse Engineering — No way out

## Descripción

> **Prompt oficial del reto:** "Escape to find the flag"
>
> **Pistas oficiales:**
> 1. Es un juego, ¿no?
> 2. Parece como si necesitaras un decompilador de C#

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2023
- **Puntos:** 200
- **ID CyLab:** 361

## Solución

El reto presenta un juego 3D en Unity donde el jugador aparece en una área cerrada con una escalera. Un muro invisible (barrera virtual) impide escapar para llegar a la bandera. El texto en la parte superior dice "Escape to find the flag". El objetivo es atravesar este muro para llegar a la bandera.

### 1. Análisis del reto

El juego es compilado como un ejecutable Windows (`pico.exe`) que contiene:
- Lógica del juego almacenada en `pico_Data/Managed/Assembly-CSharp.dll`
- Código C# compilado que controla el comportamiento del jugador y los límites del mapa

### 2. Técnicas de solución

#### Método 1: Parches de C# con dnSpy (Más directo)

**Pasos:**

1. **Obtener el ejecutable del juego** desde el servidor del reto y extraerlo en local

2. **Abrir con dnSpy** (decompilador C# gratuito):
   - Descargar dnSpy desde GitHub: https://github.com/dnSpy/dnSpy
   - Abrir el archivo `Assembly-CSharp.dll` desde la carpeta `pico_Data/Managed/`

3. **Localizar el código de control del jugador**:
   - Buscar la clase `PlayerController` o similar en el código C#
   - Encontrar la función `Jump()` o equivalente que verifica si el jugador está en el suelo

4. **Modificar la condición de salto**:
   - El código típicamente contiene una verificación `if (isGrounded)` antes de permitir saltar
   - Comentar o remover esta línea: `isGrounded = Physics.CheckSphere(...)`
   - Alternativa: cambiar la lógica para permitir saltos infinitos

5. **Guardar la DLL modificada** desde dnSpy

6. **Ejecutar el juego** con la DLL modificada:
   - Reemplazar `pico_Data/Managed/Assembly-CSharp.dll` con la versión modificada
   - Ejecutar `pico.exe`

7. **Saltar infinitamente** para atravesar el muro invisible y alcanzar la bandera

#### Método 2: Cheat Engine (Modificación de memoria)

1. Descargar Cheat Engine 7.5
2. Abrir el proceso del juego (`pico.exe`)
3. Escanear coordenadas de posición del jugador en memoria (tipo: Float, dirección: desconocida)
4. Modificar estas coordenadas para teleportear a través del muro
5. Navegar a la ubicación de la bandera
6. Capturar la flag

### 3. Lecciones aprendidas

- **Juegos Unity**: Los ejecutables de Unity siempre contienen C# compilado en `Assembly-CSharp.dll` accesible con decompiladores como dnSpy
- **Protecciones débiles**: El juego solo usa un muro de colisión virtual sin verificaciones adicionales
- **Técnicas de patching**: Modificar el comportamiento del personaje es más simple que manipular memoria en tiempo real

## Ejecución y validación

La flag se extrae correctamente al alcanzar la bandera dentro del juego modificado:

```
Flag: picoCTF{welcome_to_unity!!}
```

Se validó contra la plataforma CyLab con `submit_flag(361, flag)` → `correct: true`.

## Notas adicionales

- **Herramientas requeridas:**
  - dnSpy (decompilador C# libre): https://github.com/dnSpy/dnSpy/releases
  - Cheat Engine (alternativa): https://www.cheatengine.org/
  - NET Reflector (alternativa de pago): https://www.red-gate.com/products/dotnet/reflector/

- **Referencias sobre Unity hacking:**
  - Los juegos Unity exponen el IL (Intermediate Language) compilado en DLLs que son descompilables
  - No hay ofuscación por defecto en ejecutables de Unity compilados en Debug
  - El archivo `Assembly-CSharp.dll` siempre contiene el código custom del proyecto

- **Ruta de la flag en el juego:**
  - La bandera blanca grande visible en el juego es física pero inalcanzable por el muro
  - Al atravesar el muro (via saltos infinitos o teleport), se activa un colisionador que dispara el evento de captura
  - La flag se guarda en una variable de string en alguna clase del juego (posiblemente `APTX` o `GameManager`)

## Referencias

- Writeup: https://medium.com/@niceselol/picoctf-no-way-out-acb05df92b22
- Código fuente de dnSpy: https://github.com/dnSpy/dnSpy
- Documentación de Unity IL2CPP: https://docs.unity3d.com/Manual/IL2CPP.html
- Reto en CyLab: https://learn.cylabacademy.org/library/361
