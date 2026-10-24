# Reverse Engineering — Ready Gladiator 1

## Descripción
> **Prompt oficial del reto:** "Can you make a CoreWars warrior that wins? Your opponent is the Imp. To get the flag, you must beat the Imp at least once out of the many rounds."
>
> **Pistas oficiales:**
> 1. You may be able to find a viable warrior in beginner docs

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto sitúa a un guerrero de **Core Wars** frente al clásico `Imp`. El objetivo es lograr al menos una victoria sobre 100 rondas de simulación.

### 1. Estrategia del bombardero (*Bomber*)
Para neutralizar al `Imp` (cuya única acción es copiar la instrucción `mov 0, 1` hacia adelante), se diseña un bombardero que esparza instrucciones destructivas `DAT` a lo largo de la memoria circular:

```redcode
;redcode
;name Bomber
;assert 1
add #4, 3
mov 2, @2
jmp -2
dat #0, #0
end
```

- `add #4, 3`: Incrementa el puntero de destino en pasos de 4 celdas.
- `mov 2, @2`: Copia la instrucción bomba (`dat #0, #0`) en la celda apuntada.
- `jmp -2`: Salta al inicio para repetir el ciclo indefinidamente.

Cuando el hilo del `Imp` alcanza una celda sobreescrita con la instrucción `DAT`, el proceso finaliza inmediatamente.

### 2. Ejecución
Enviando el guerrero al puerto del servidor:

```bash
nc <host> <puerto> < warrior.red
```

Salida del servicio:
```text
Rounds: 100
Warrior 1 wins: 20
Warrior 2 wins: 0
Ties: 80
You did it!
academy{...}
```

Al superar el umbral de victorias requerido, el servidor imprime la bandera en formato `academy{...}`.

## Notas adicionales
- Los empates ocurren comúnmente en Core Wars cuando ambos guerreros sobreviven el límite máximo de ciclos de la simulación sin que ninguno muera. Lograr que el oponente ejecute una instrucción `DAT` es la forma estándar de asegurar una victoria.

## Referencias
- Reto: https://learn.cylabacademy.org/library/369
- The Beginners' Guide to Corewar: http://www.koth.org/info/akguide/
