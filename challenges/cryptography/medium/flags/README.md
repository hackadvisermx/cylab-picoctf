# Cryptography — Flags

## Descripción

> **Prompt oficial del reto:** "What do the flags mean?"

> **Hints:**
> 1. The flag is in the format PICOCTF{}

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny

## Solución

El reto entrega un archivo de imagen `flag.png` que muestra una hilera de banderas de señales náuticas pertenecientes al **Código Internacional de Señales** (*International Code of Signals - ICS*).

### Decodificación de banderas marítimas

Cada bandera náutica representa una letra del alfabeto internacional. Siguiendo el formato de bandera indicado en la pista (`PICOCTF{...}`):

1. **Prefijo:**
   - Bandera azul con rectángulo blanco interior → **P** (Papa)
   - Bandera amarilla con punto negro central → **I** (India)
   - Bandera de cinco franjas horizontales (azul-blanco-rojo-blanco-azul) → **C** (Charlie)
   - Bandera dividida en diagonal roja y amarilla → **O** (Oscar)
   - Franjas horizontales → **C** (Charlie)
   - Franjas verticales roja-blanca-azul → **T** (Tango)
   - Bandera roja con rombo blanco central → **F** (Foxtrot)

2. **Contenido interno entre llaves:**
   Decodificando las banderas dentro de las llaves con la tabla de señales marítimas y números de sustitución (leet speak):
   - Bandera F → **F**
   - Gallardete numérico 1 → **1**
   - Bandera A → **A**
   - Bandera G → **G**
   - Gallardete numérico 5 → **5**
   - Bandera A → **A**
   - Bandera N → **N**
   - Bandera D → **D**
   - Gallardete numérico 5 → **5**
   - Bandera T → **T**
   - Bandera U → **U**
   - Bandera F → **F**
   - Bandera F → **F**

El texto resultante es:
`PICOCTF{F1AG5AND5TUFF}`

## Referencias

- [International Code of Signals (ICS) — Wikipedia](https://en.wikipedia.org/wiki/International_Code_of_Signals)
- [International Maritime Signal Flags Chart](https://www.navy.mil/Resources/International-Maritime-Signal-Flags/)
