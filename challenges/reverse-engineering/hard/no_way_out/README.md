# Reverse Engineering — No way out

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Autor:** Kris
- **Evento / Origen:** picoCTF 2023
- **ID CyLab:** 361
- **Puntos:** 200

---

## Descripción del Reto

> **Prompt:** "Put this flag in standard academy format before submitting. If the flag was `h1_1m_7h3_f14g` submit `academy{h1_1m_7h3_f14g}` to the platform."
> 
> Archivos proporcionados:
> - `win.zip` (Juego Windows compilado en Unity)
> - `mac.app.zip` (Juego macOS compilado en Unity)
> 
> Contraseña de descompresión: `picoctf`

Al iniciar el juego, el jugador se encuentra confinado en un recinto cerrado por muros invisibles. A lo lejos, fuera del recinto delimitado, se observa una bandera blanca que ondea (`USMC flag.obj`). El reto consiste en franquear las barreras físicas/colisionadores del mapa y alcanzar la bandera para activar la visualización del flag.

---

## Estructura Técnica del Juego

El juego fue desarrollado sobre el motor **Unity** utilizando el backend de scripting **Mono** (en lugar de IL2CPP), lo que facilita enormemente la inspección y análisis estático:

- **Ejecutable:** `pico.exe`
- **Motor / Runtime:** `UnityPlayer.dll`, `MonoBleedingEdge/`
- **Ensamblado Principal:** `pico_Data/Managed/Assembly-CSharp.dll`
- **Recursos y Escenas:** `pico_Data/level0`, `pico_Data/globalgamemanagers.assets`, `pico_Data/sharedassets0.assets`

---

## Análisis de Ensamblado (`Assembly-CSharp.dll`)

Al inspeccionar los metadatos y código IL de `Assembly-CSharp.dll` mediante herramientas .NET (`dnfile`, `dncil` o dnSpy), se identifican las clases del juego:

1. **`EvolveGames.PlayerController`:**
   - Gestiona el movimiento en primera persona: `walkingSpeed`, `RuningSpeed`, `jumpSpeed`, `gravity`, `characterController`.
   - En el método `Update`, las restricciones de salto verifican si el jugador se encuentra sobre el suelo (`characterController.isGrounded`).

2. **`.APTX` (Disparador de la Bandera):**
   - Posee dos campos privados de tipo `GameObject`:
     - `player`
     - `Mysterious`
   - El método `OnTriggerEnter(Collider other)` evalúa:
     ```csharp
     private void OnTriggerEnter(Collider other)
     {
         if (other.gameObject == this.player)
         {
             this.Mysterious.SetActive(true);
         }
     }
     ```
   - Al colisionar el jugador con el objeto que contiene este componente, se activa el objeto oculto `Mysterious`.

---

## Análisis Estático de la Escena (`level0`)

Mediante el análisis de assets con `UnityPy` sobre `pico_Data/level0`:

1. **Objetos de Escena Relevantes:**
   - `PlayerController` (Path ID 78): Controlador del jugador (activo por defecto).
   - `USMC flag.obj` (Path ID 85): Bandera ubicada en coordenadas globales `(-24.0, 0.0, -22.2)`.
   - `Text (TMP)` (Path ID 39): Elemento UI con estado `m_IsActive: false`.

2. **Componentes de `USMC flag.obj`:**
   - `Transform` (Path ID 176)
   - `BoxCollider` (Path ID 389)
   - `MonoBehaviour` (Path ID 459): Instancia del script `APTX` (MonoScript ID 1086 en `globalgamemanagers.assets`). Sus referencias son:
     - `player` $\rightarrow$ Path ID 78 (`PlayerController`)
     - `Mysterious` $\rightarrow$ Path ID 39 (`Text (TMP)`)

3. **Contenido de `Text (TMP)`:**
   - Componente `TextMeshProUGUI` (Path ID 446).
   - Al inspeccionar los datos serializados del componente de texto, se encuentra el string estático configurado en el editor de Unity:
     ```text
     WELCOME_TO_UNITY!!
     ```

---

## Métodos de Resolución

### Método 1: Análisis Estático de Assets (Directo, sin emulación de Windows)
Dado que Unity serializa las cadenas de texto de los componentes UI en texto plano dentro de los archivos de nivel:
1. Inspeccionar `pico_Data/level0` extrayendo las cadenas de los componentes `TextMeshProUGUI`.
2. O bien, rastrear las referencias de `APTX` en `USMC flag.obj` hasta el GameObject `Text (TMP)` y extraer el buffer de texto `WELCOME_TO_UNITY!!`.

### Método 2: Patching de `Assembly-CSharp.dll` (dnSpy)
1. Abrir `pico_Data/Managed/Assembly-CSharp.dll` en dnSpy.
2. Navegar a `EvolveGames.PlayerController::Update`.
3. Modificar la condición de salto:
   - Incrementar `jumpSpeed` a un valor elevado (e.g. 50.0f) o eliminar la comprobación `isGrounded` para permitir salto continuo / vuelo sobre los muros invisibles.
4. Guardar el ensamblado compilado, ejecutar el juego y desplazarse hacia `USMC flag.obj` en `(-24.0, 0, -22.2)`.
5. Al tocar la bandera, `APTX::OnTriggerEnter` activa el componente `Text (TMP)` mostrando la flag en pantalla.

### Método 3: Modificación de Memoria (Cheat Engine)
1. Adjuntar Cheat Engine al proceso `pico.exe`.
2. Localizar las coordenadas de posición del jugador (`Transform.position` en tipo `float`).
3. Modificar la coordenada Y (altura) o teleportar directamente a las coordenadas de la bandera `X = -24.0, Y = 1.0, Z = -22.2`.
4. El colisionador se activa inmediatamente, desplegando el texto en pantalla.

---

## Validación

Se envió la bandera a la API de CyLab mediante `submit_flag(361, flag)`:

```python
submit_flag(361, "academy{WELCOME_TO_UNITY!!}")
```

Respuesta del servidor:
```json
{"user": 486, "challenge": 361, "flag": "academy{WELCOME_TO_UNITY!!}", "correct": true, "historical": false}
```

---

## Flag

```
academy{WELCOME_TO_UNITY!!}
```
*(Flag original en picoCTF: `picoCTF{WELCOME_TO_UNITY!!}`)*
