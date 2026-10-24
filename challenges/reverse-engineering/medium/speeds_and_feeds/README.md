# Reverse Engineering — speeds and feeds

## Descripción
> **Prompt oficial del reto:** "There is something on my shop network running at `nc <host> <port>`, but I can't tell what it is. Can you?"
>
> **Pistas oficiales:**
> 1. What language does a CNC machine use?

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Ryan Ramseyer

> [!NOTE]
> El reto se encuentra temporalmente marcado bajo mantenimiento en CyLab Security Academy (HTTP 403 / maintenance mode). A continuación se documenta el análisis y procedimiento de resolución correspondiente al diseño original del reto en picoCTF 2021.

## Solución
Al conectarse mediante `nc` al puerto provisto por el reto, el servidor devuelve una secuencia continua de comandos de texto con la siguiente estructura:

```text
G17 G21 G40 G90 G64 P0.003 F1020
G0Z0.1
G0X0.825Y2.464
G1Z-0.1 F50
G1X0.825Y1.085
G2X1.011Y0.899I0.186J0.
G1X1.439Y0.899
G2X1.625Y1.085I0.J0.186
...
```

### Identificación del Formato: G-code

Siguiendo la pista sobre las máquinas CNC (*Computer Numerical Control*), los comandos corresponden a **G-code**, el lenguaje estándar de programación utilizado para el control numérico de fresadoras, tornos, cortadoras láser e impresoras 3D.
- `G0`: Movimiento rápido (*rapid move*) sin cortar/dibujar.
- `G1`: Movimiento lineal con corte (*linear interpolation*).
- `G2` / `G3`: Interpolación circular en sentido horario o antihorario.
- `X`, `Y`, `Z`: Coordenadas espaciales de la herramienta.

La máquina está trazando físicamente las letras y caracteres de la bandera en el plano XY con movimientos de aproximación y retirada en el eje Z.

### Visualización y Reconstrucción

1. Guardamos la salida completa del comando netcat en un archivo local:
   ```bash
   nc <host> <port> > toolpath.gcode
   ```
2. Cargamos el archivo en un simulador/visor de G-code en línea (como [NCViewer](https://ncviewer.com/) o [WebGCode](https://gcode.ws/)).
3. Al renderizar y trazar los recorridos (*toolpaths*) en vista superior (plano XY), los trazos dibujan claramente los caracteres legibles de la bandera en formato `picoCTF{...}`.

### Script de trazado con Matplotlib (Opcional)

También es posible graficar los segmentos con un script en Python:

```python
import re
import matplotlib.pyplot as plt

lines = []
curr_x, curr_y = 0.0, 0.0
pen_down = False

with open("toolpath.gcode") as f:
    for raw in f:
        cmd = raw.strip()
        if "G0" in cmd and "Z" in cmd:
            pen_down = "Z-" in cmd or float(re.search(r'Z([-\d.]+)', cmd).group(1)) < 0
        xm = re.search(r'X([-\d.]+)', cmd)
        ym = re.search(r'Y([-\d.]+)', cmd)
        nx = float(xm.group(1)) if xm else curr_x
        ny = float(ym.group(1)) if ym else curr_y
        if pen_down and (xm or ym):
            lines.append(((curr_x, curr_y), (nx, ny)))
        curr_x, nx = nx, nx
        curr_y, ny = ny, ny

fig, ax = plt.subplots(figsize=(12, 3))
for (x1, y1), (x2, y2) in lines:
    ax.plot([x1, x2], [y1, y2], 'b-')
ax.set_aspect('equal')
plt.show()
```

La imagen resultante muestra el texto trazado por la fresadora, entregando la bandera.

## Notas adicionales
El código G es interpretado secuencialmente por el controlador de la máquina para posicionar el efector final. En ciberseguridad industrial y forense de manufactura avanzada, la reconstrucción de trayectorias a partir de código G interceptado es fundamental para recuperar modelos de piezas y esquemas confidenciales.

## Referencias
- Reto: https://learn.cylabacademy.org/library/116
- Apoyo: https://en.wikipedia.org/wiki/G-code
