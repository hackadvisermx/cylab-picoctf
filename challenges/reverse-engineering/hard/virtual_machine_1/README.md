# Reverse Engineering — Virtual Machine 1

## Descripción
> **Prompt oficial del reto:** "The enemy has upgraded their mechanical analog computer. Start an instance to begin. We grabbed this design doc from enemy servers: Download. We know that the rotation of the red axle is input and the rotation of the blue axle is output. Reverse engineer the mechanism and get past their checker program: nc xebec.cylabacademy.net 49004"
>
> **Pistas oficiales:**
> 1. The supporting structure for the machine has been removed from the given design doc.
> 2. Some gears are meshed strangely, such as tooth overlapping tooth. Consider such gears as meshed correctly.
> 3. Learn enough about gear ratios to abstract details from the design doc.

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto suministra un modelo 3D en formato COLLADA (`.dae`) dentro de `Virtual-Machine-1.zip` que representa una computadora analógica mecánica compuesta por trenes de engranajes compuestos y un mecanismo diferencial.

### 1. Análisis del mecanismo cinemático
Al inspeccionar el ensamblaje mecánico en Blender:
1. El eje rojo representa la entrada de rotación ($N_{in}$).
2. El eje azul representa la salida resultante ($N_{out}$).
3. Para cada par de engranajes acoplados, la relación de transmisión elemental entre el engranaje conductor (*driver*, con $T_1$ dientes) y el engranaje conducido (*driven*, con $T_2$ dientes) es:
   $$R_i = \frac{T_1}{T_2}$$
4. En trenes de engranajes compuestos y diferenciales acoplados, la relación global del sistema se obtiene multiplicando las relaciones de cada etapa cinemática sucesiva.
5. El cálculo del tren de engranajes completo arroja una relación de reducción/multiplicación constante de:
   $$R = 9359$$
   Por cada vuelta completa del eje de entrada (rojo), el eje de salida (azul) rota exactamente $9359$ veces:
   $$N_{out} = N_{in} \times 9359$$

### 2. Interacción con el servicio remoto

```python
import socket
import re

HOST = "xebec.cylabacademy.net"
PORT = 49004

s = socket.create_connection((HOST, PORT), timeout=10)
data = b""
while b"Answer>" not in data:
    chunk = s.recv(1024)
    if not chunk:
        break
    data += chunk

text = data.decode("utf-8", errors="ignore")
match = re.search(r"is (\d+)", text)
if match:
    inp = int(match.group(1))
    ans = inp * 9359
    s.sendall(f"{ans}\n".encode())

    resp = s.recv(4096).decode("utf-8", errors="ignore")
    print("Response:", resp)
```

Al suministrar el valor calculado para la rotación requerida por la instancia remota, el programa valida el resultado y expone la bandera en formato `academy{...}`.

## Notas adicionales
- Este reto es la continuación directa de *Virtual Machine 0*. En la versión inicial, el tren de engranajes correspondía a un acoplamiento simple con relación pequeña, mientras que en *Virtual Machine 1* se incorporan engranajes compuestos de alta desmultiplicación.

## Referencias
- Reto: https://learn.cylabacademy.org/library/386
- Relaciones de transmisión en engranajes mecánicos: https://en.wikipedia.org/wiki/Gear_train
