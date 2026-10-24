# Reverse Engineering — Virtual Machine 0

## Descripción
> **Prompt oficial del reto:** "Can you crack this black box? We grabbed this design doc from enemy servers: Download. We know that the rotation of the red axle is input and the rotation of the blue axle is output. The following input gives the flag as output: Download."
>
> **Pistas oficiales:**
> 1. Rotating the axle that number of times is obviously not feasible. Can you model the mathematical relationship between red and blue?

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona un archivo comprimido `Virtual-Machine-0.zip` que contiene un modelo 3D en formato COLLADA (`Virtual-Machine-0.dae`), y un archivo de texto `input.txt` con un entero de gran magnitud (más de 70 dígitos).

### 1. Modelado del tren de engranajes
Al inspeccionar el archivo `.dae` en un visor 3D o analizar la geometría de las partes (ruedas dentadas):
- El eje de entrada (rojo) está conectado a un engranaje conductor de **40 dientes**.
- El eje de salida (azul) está impulsado por un engranaje conducido de **8 dientes**.

La relación de transmisión (gear ratio) entre el eje rojo de entrada y el eje azul de salida es:
$$\text{Ratio} = \frac{\text{Dientes de entrada}}{\text{Dientes de salida}} = \frac{40}{8} = 5$$

Por cada vuelta del eje rojo, el eje azul gira exactamente 5 veces.

### 2. Cálculo y decodificación
Multiplicando el valor numérico de `input.txt` por 5, el resultado entero obtenido representa la codificación en bytes de la bandera en formato hexadecimal:

```python
import binascii

with open("input.txt", "r") as f:
    input_num = int(f.read().strip())

output_num = input_num * 5
hex_str = hex(output_num)[2:]
if len(hex_str) % 2 != 0:
    hex_str = '0' + hex_str

flag = binascii.unhexlify(hex_str).decode('utf-8')
print("Flag:", flag)
```

Al convertir la cadena hexadecimal a texto plano, se revela la bandera en formato `academy{...}`.

## Notas adicionales
- Los archivos COLLADA (`.dae`) son documentos XML abiertos. A través del análisis de las etiquetas `<mesh>` o mediante herramientas de modelado como Blender, es posible verificar las dimensiones y el recuento de vértices de cada diente de los engranajes sin necesidad de simulación física.

## Referencias
- Reto: https://learn.cylabacademy.org/library/385
- COLLADA Specification: https://www.khronos.org/collada/
