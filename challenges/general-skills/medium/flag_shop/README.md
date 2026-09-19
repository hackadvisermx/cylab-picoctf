# General Skills — flag_shop

## Descripción
> **Prompt oficial:** "There's a flag shop selling stuff, can you buy a flag?"
>
> **Hints:**
> 1. Two's compliment can do some weird things when numbers get really big!

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny

## Solución
Al conectar con `nc` aparece un menú de una "tienda de flags" (servicio en C, probablemente) con tres opciones: ver saldo, comprar flags, salir. El saldo inicial es **1100**. En la tienda hay dos artículos:

1. "Defintely not the flag Flag" — cuesta 900 cada una, y **permite elegir cantidad libremente** (entero con signo).
2. "1337 Flag" (la flag real) — cuesta 100000, solo hay 1 en stock, y solo permite confirmar la compra de 1 unidad (no admite cantidad arbitraria).

Con un saldo de 1100 no alcanza para pagar 100000. El bug está en el artículo 1: el precio total se calcula como `precio * cantidad` usando aritmética de **entero de 32 bits con signo**, sin validar que la cantidad sea razonable. Pidiendo una cantidad lo bastante grande, `900 * cantidad` se desborda (overflow) y el resultado, interpretado como `int32`, se convierte en un número **negativo**. Al restar ese coste negativo del saldo (`saldo -= coste`), el saldo en realidad **aumenta** — y si el resultado de esa resta también desborda el rango de 32 bits, puede aterrizar en cualquier valor, incluyendo uno positivo y grande.

Se calculó por fuerza bruta (en Python, simulando la aritmética `int32` con wraparound) qué cantidad exacta produce un saldo final positivo y suficiente para pagar los 100000 de la flag real, evitando pedir una cantidad tan extrema que el propio saldo resultante vuelva a desbordarse a negativo.

```python
def to_i32(x):
    x = x & 0xFFFFFFFF
    if x >= 0x80000000:
        x -= 0x100000000
    return x

price, balance0 = 900, 1100
for qty in range(2_386_093, 2_386_093 + 20_000_000, 1_000_000):
    cost = to_i32(price * qty)
    newbal = to_i32(balance0 - cost)
    print(qty, cost, newbal)
# qty=9386093 -> cost=-142450892 -> nuevo saldo = 142451992 (positivo, > 100000)
```

Con eso, la secuencia completa contra el servicio real:

```bash
nc fickle-tempest.picoctf.net <PUERTO>
# 2                (Buy Flags)
# 1                (Defintely not the flag Flag, 900 c/u)
# 9386093          (cantidad: dispara el overflow, saldo final ~142,451,992)
# 2                (Buy Flags de nuevo)
# 2                (1337 Flag, la real, cuesta 100000, stock 1)
# 1                (confirmar compra de 1 unidad)
# -> YOUR FLAG IS: picoCTF{...}
```

**Importante:** cada conexión `nc` nueva reinicia el saldo a 1100 (proceso nuevo del lado del servidor). Si se hace un intento fallido que deja el saldo en un estado inútil (p. ej. muy negativo por pasarse con la cantidad), hay que **reiniciar la instancia** (botón "Restart Instance" en CyLab Academy) o simplemente reconectar con una nueva sesión `nc` — cualquiera de las dos basta, ya que el estado vive solo en el proceso del servidor, no en el contenedor completo.

## Notas adicionales
- Vulnerabilidad clásica de **integer overflow / underflow** en aritmética de precios, muy típica de retos "pwn ligero" o de lógica de negocio en CTFs (equivalente conceptual a comprar con saldo negativo en un carrito de compras mal validado).
- El propio servidor, al confirmar la compra del artículo 1, imprime el coste final ya con signo (`The final cost is: -142450892`), lo cual facilita mucho verificar la hipótesis de overflow sin necesidad de acceder al binario/código fuente.
- No hizo falta usar el binario fuente (enlace "Source" en la página) para resolverlo — bastó con interacción por `nc` y cálculo local en Python de la aritmética de 32 bits.

## Referencias
- Reto: https://learn.cylabacademy.org/library/49
- Apoyo: aritmética de overflow de enteros con signo de 32 bits (concepto general de "integer overflow" en C).
