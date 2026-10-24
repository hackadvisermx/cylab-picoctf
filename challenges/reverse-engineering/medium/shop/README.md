# Reverse Engineering — Shop

## Descripción
> **Prompt oficial del reto:** "Best Stuff - Cheap Stuff, Buy Buy Buy...
> Store Instance: [source](https://challenge-files.cylabacademy.net/library/da44ce1b454aafad66dc88600f0832f7697618db1105eb22e12087eed1955762/source). The shop is open for business at `nc <host> <port>`."
>
> **Pistas oficiales:**
> 1. Always check edge cases when programming

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** thelshell

## Solución
El reto ofrece un servicio interactivo a través de netcat que simula una tienda en línea y un archivo ejecutable denominado `source`.

Al conectarse al servicio:
```text
Welcome to the market!
=====================
You have 40 coins
	Item		Price	Count
(0) Quiet Quiches	10	12
(1) Average Apple	15	8
(2) Fruitful Flag	100	1
(3) Sell an Item
(4) Exit
Choose an option:
```

El usuario comienza con 40 monedas y el objeto `Fruitful Flag` cuesta 100 monedas.

### Vulnerabilidad: Validación insuficiente de enteros (Entrada negativa)

Al comprar un artículo, el programa solicita: `"How many do you want to buy?"`.
Si ingresamos un número negativo (por ejemplo `-10`):
1. El costo total calculado es: `precio * cantidad = 10 * (-10) = -100`.
2. El saldo de monedas se actualiza restando el costo: `saldo = saldo - costo = 40 - (-100) = 140`.
3. El programa no verifica que la cantidad sea estrictamente mayor que cero (`cantidad > 0`), por lo que el saldo del usuario se incrementa a 140 monedas.
4. Con saldo suficiente (140 monedas), seleccionamos la opción `(2) Fruitful Flag` y compramos 1 unidad.

### Respuesta del servidor

El servidor responde imprimiendo la bandera como una lista de valores ASCII decimales:
```text
Flag is:  [97 99 97 100 101 109 121 123 98 52 100 95 ...]
```

### Script de explotación y decodificación

```python
import socket

s = socket.create_connection(('<host>', <port>))

def recv_until(target):
    buf = b""
    while target not in buf:
        chunk = s.recv(1024)
        if not chunk: break
        buf += chunk
    return buf.decode()

# Comprar cantidad negativa del item 0 para aumentar monedas
recv_until(b"Choose an option: ")
s.sendall(b"0\n")
recv_until(b"buy?")
s.sendall(b"-10\n")

# Comprar el objeto Fruitful Flag (opcion 2)
recv_until(b"Choose an option: ")
s.sendall(b"2\n")
recv_until(b"buy?")
s.sendall(b"1\n")

response = s.recv(4096).decode()
s.close()

# Extraer y decodificar números ASCII
import re
numbers = [int(x) for x in re.findall(r'\d+', response)]
flag = "".join(chr(c) for c in numbers).strip()
print("Flag:", flag)
```

Al convertir cada entero decimal a su carácter ASCII correspondiente, se obtiene la bandera en formato `academy{...}`.

## Notas adicionales
Este tipo de vulnerabilidad por omisión de comprobación de rangos (*missing bound check / signed integer misuse*) es un clásico fallo de lógica de negocio y aritmética en aplicaciones en lenguaje C o ensamblador.

## Referencias
- Reto: https://learn.cylabacademy.org/library/134
- Apoyo: https://cwe.mitre.org/data/definitions/128.html
