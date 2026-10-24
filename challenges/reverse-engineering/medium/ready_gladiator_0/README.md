# Reverse Engineering — Ready Gladiator 0

## Descripción
> **Prompt oficial del reto:** "Can you make a CoreWars warrior that always loses, no ties?"
>
> **Pistas oficiales:**
> 1. CoreWars is a well-established game with a lot of docs and strategy
> 2. Experiment with input to the CoreWars handler or create a self-defeating bot

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto requiere diseñar un guerrero para el entorno **Core Wars** que **pierda todas las 100 rondas** frente al `Imp`, sin permitir empates.

### 1. Principio de ejecución en Redcode
En el estándar Redcode, la instrucción `DAT` define datos no ejecutables. Si un hilo de ejecución intenta procesar una instrucción `DAT`, el hilo se considera inválido y el simulador lo termina de forma inmediata (*process termination*).

### 2. Guerrero autodestructivo
Para garantizar una derrota inmediata en el primer ciclo sin generar empates:

```redcode
;redcode
;name Suicide
;assert 1
dat 0, 0
end
```

Al iniciar la batalla, el guerrero ejecuta la instrucción `dat 0, 0` en el ciclo 1, lo cual provoca la muerte instantánea del proceso y otorga la victoria completa al oponente (`Imp`).

### 3. Ejecución
Enviando el código del guerrero al servicio por red:

```bash
nc <host> <puerto> < warrior.red
```

Salida del servicio:
```text
Rounds: 100
Warrior 1 wins: 0
Warrior 2 wins: 100
Ties: 0
You did it!
academy{...}
```

El servidor confirma la condición de victoria inversa y muestra la bandera en formato `academy{...}`.

## Notas adicionales
- Mientras que la mayoría de retos en competencias de Core Wars buscan maximizar la tasa de supervivencia, este reto evalúa la comprensión de los mecanismos fundamentales de terminación de procesos en el simulador MARS.

## Referencias
- Reto: https://learn.cylabacademy.org/library/368
- Core Wars FAQ: http://www.koth.org/info.html
