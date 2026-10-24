# Cryptography — Ricochet

## Descripción
> **Prompt oficial del reto:** "I bought this robot to help me locate flags, but the controller is stuck in a demo loop where the robot just goes in circles. Can you exploit the encryption between the controller to navigate the robot to the flag?
> 
> Go to this web page for more instructions on how to interface with this challenge. All connections to the challenge will be made via the browser and/or HTTP requests to the server. You will need to use the functions provided in radio_interface.py to interface with the server. The source code for the robot and controller will be useful as well: robot.py; robotcontroller.py; crypto.py"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2025
- **Autor:** asinghani

## Solución
El reto simula una red de radio virtualizada (`/radio_tx` y `/radio_rx`) donde un robot (dirección `0x20` = 32) y su controlador (dirección original `0x10` = 16) se comunican mediante un canal cifrado con intercambio de claves Diffie-Hellman (`X25519` vía Monocypher) y autenticación HMAC basada en BLAKE2b con una clave estática precompartida (`shared_hmac_key`).

### 1. Análisis del Sistema y del Tablero
El robot se mueve sobre una cuadrícula de $10 \times 10$ llena de obstáculos:
- El robot se desplaza en línea recta en la dirección indicada hasta chocar contra un obstáculo o el borde exterior (mecánica estilo *Ricochet Robots*).
- La bandera se ubica en $(4, 8)$, protegida por un obstáculo en $(5, 8)$.
- El único camino factible para detenerse exactamente sobre la bandera requiere alcanzar $(0, 8)$ y descender hacia el sur.
- La secuencia óptima (única en el tablero) consta de 9 movimientos:
  `['south', 'east', 'north', 'west', 'south', 'east', 'north', 'east', 'south']`.

### 2. El Bucle Demo y el Límite de Movimientos
El controlador emite movimientos en un ciclo continuo: `east`, `south`, `west`, `north` ($0, 1, 2, 3$).
Cada cambio de dirección en nuestra ruta de 9 pasos requiere un giro antihorario ($+3 \pmod 4$), avanzando el índice de movimientos del controlador:
$$1 \xrightarrow{+3} 4 \xrightarrow{+3} 7 \xrightarrow{+3} 10 \xrightarrow{+3} 13 \xrightarrow{+3} 16 \xrightarrow{+3} 19 \xrightarrow{+1} 20 \xrightarrow{+1} 21$$
Por tanto, el movimiento 8 (`east`) corresponde al índice 20 del controlador (nonce 41), y el movimiento 9 (`south`) al índice 21 (nonce 43).

Sin embargo, el robot solo ejecuta hasta 20 comandos por ciclo (`for _ in range(20): cmd = await self.read_command()`). En una ejecución normal, el bucle se detiene tras el movimiento 19 (nonce 39).

### 3. Vulnerabilidades del Protocolo Criptográfico
1. **Reasignación de Dirección no Autenticada:**
   El mensaje `set_addr` no requiere autenticación:
   ```python
   if msg_type == "set_addr":
       self.address = int(msg["new_addr"]) & 0xFF
   ```
   Podemos mover el controlador legítimo de la dirección 16 a la dirección 48 (`0x30`), permitiendo interponernos como Man-in-the-Middle (MITM) en la dirección 16.

2. **Ataque de Rebote (Ricochet Reflection Attack):**
   En `read_command()`, el robot solicita movimientos enviando un paquete vacío en `recv_secure_data()`:
   `{"message": "", "nonce": nonce, "hmac": compute_hmac("", nonce, key)}`
   Si el atacante refleja este paquete idéntico hacia el robot como si fuera la respuesta `secure_data_response`:
   - El robot valida el HMAC (es su propio HMAC para `""` en ese nonce).
   - El robot descifra un mensaje vacío (`""`).
   - Dado que `resp == ""`, `read_command()` no retorna ningún movimiento (el robot no se desplaza ni consume iteraciones de su contador de 20 movimientos).
   - Sin embargo, `self.nonce` se incrementa en 1, permitiendo avanzar el nonce del robot sin moverlo en la cuadrícula.

3. **Inmutabilidad y Reutilización de HMACs entre Sesiones:**
   La clave `keys["shared_hmac_key"]` es estática. Cualquier mensaje con HMAC capturado en una sesión anterior puede ser reproducido si el nonce coincide.

### 4. Explotación en 3 Fases
1. **Captura y Registro:** Se corre un ciclo demo interponiéndose entre el robot y el controlador para registrar pares completos de comandos y acuses de recibo para los nonces 0 al 39.
2. **Adelanto Sintético en Segundo Plano:** En la carrera guiada, tras iniciar el robot y negociar DH con ambas partes, se inicia el Paso 1 (`south`). Mientras el robot se desplaza físicamente hacia el sur (~5 segundos), el script inyecta en segundo plano los 40 mensajes registrados al controlador en la dirección 48, adelantando el controlador a nonce 40 sin bloquear ni interferir con la radio del robot.
3. **Navegación Guiada y Obtención en Vivo de Nonces 40-43:**
   - Para los pasos 1 a 7 (nonces 0 a 39), los movimientos no deseados se saltan con paquetes ricochet y los movimientos objetivo (`south`, `east`, `north`, `west`, `south`, `east`, `north`) se entregan usando las respuestas pregrabadas, situando al robot en $(0, 6)$.
   - Al finalizar el paso 7, el robot solicita el siguiente comando en nonce 40.
   - El controlador se encuentra esperando exactamente en nonce 40: se reenvía la solicitud viva del robot al controlador, obteniendo en vivo el movimiento 20 (`east`, nonce 41), llevando al robot a $(0, 8)$.
   - A continuación, se reenvía la solicitud de nonce 42, obteniendo en vivo el movimiento 21 (`south`, nonce 43), llevando al robot a $(4, 8)$.

El robot aterriza directamente sobre la casilla de la bandera en $(4, 8)$ y el endpoint `/state` revela la flag en formato `academy{...}`.

```bash
# Ejecutar el exploit interactivo en Python
./tmp/venv313/bin/python tmp/perfect_solve.py
```

## Notas adicionales
- Las funciones de `crypto.py` calculan `compute_hmac(message, nonce, key)` mediante concatenación directa `(message + str(nonce) + key.hex())`, lo que además abre la puerta a colisiones de delimitador entre el cuerpo del mensaje y el nonce.
- Mantener al controlador separado en una dirección privada (`0x30`) permite alimentar mensajes de sincronización de manera determinista sin alertar al autómata.

## Referencias
- Reto: https://learn.cylabacademy.org/library/495
- PicoCTF 2025: Ricochet (asinghani)
- Monocypher Cryptographic Library: https://monocypher.org/
