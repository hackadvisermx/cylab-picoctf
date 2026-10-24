# Reverse Engineering — Ready Gladiator 2

## Descripción
> **Prompt oficial del reto:** "Can you make a CoreWars warrior that wins every single round?"
>
> **Pistas oficiales:**
> 1. If your warrior is close, try again, it may work on subsequent tries... why is that?

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto implementa una simulación del juego de programación competitiva **Core Wars** ejecutada a través de un servicio en red. A diferencia de las versiones 0 y 1, en este reto el guerrero debe **ganar el 100% de las rondas** (100 de 100) contra el guerrero oponente (`Imp`).

### 1. El oponente (`Imp`)
El programa `Imp` es un clásico guerrero de una sola instrucción que se replica sucesivamente en la siguiente posición de memoria:
```redcode
mov 0, 1
```

Si el oponente se ejecuta sin interrupción, puede generar réplicas infinitas o empates.

### 2. Estrategia de victoria total: Trampa de decremento
Para garantizar una tasa de victoria del 100%, se requiere un programa que altere inmediatamente el espacio de memoria previo a la ejecución del oponente o que cree un bucle infinito que capture y destruya las instrucciones entrantes:

```redcode
;redcode
;name Dominator
;assert 1
jmp 0, <-2
end
```

- `jmp 0`: Genera un bucle infinito en su propia instrucción, manteniéndose en ejecución segura.
- `<-2`: Aplica un direccionamiento indirecto con pre-decremento (`<`) sobre el campo B dos posiciones atrás. En cada ciclo de cómputo, decrementa la celda de memoria referenciada, corrompiendo la instrucción del `Imp` cuando intenta avanzar, forzando la muerte del proceso adversario.

### 3. Ejecución
Enviando el código del guerrero al servidor mediante Netcat:

```bash
nc <host> <puerto> < warrior.red
```

Salida del servicio:
```text
Rounds: 100
Warrior 1 wins: 100
Warrior 2 wins: 0
Ties: 0
You did it!
academy{...}
```

## Notas adicionales
- El direccionamiento con pre-decremento (`<`) es una de las técnicas más eficientes en Redcode para sembrar bombas o corromper punteros de ejecución de procesos concurrentes.

## Referencias
- Reto: https://learn.cylabacademy.org/library/370
- Core Wars / Redcode ICWS'94 Standard: http://www.koth.org/info/standards/icws94.html
