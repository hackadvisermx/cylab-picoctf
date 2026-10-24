# Forensics — SideChannel

## Descripción
> **Prompt oficial del reto:** "There's something fishy about this PIN-code checker, can you figure out the PIN and get the flag? Download the PIN checker program here [pin_checker](https://challenge-files.cylabacademy.net/library/2d62bc623a510c8cd7edbbfbcb1d515444f151b0871f35aef29af36f99479c94/pin_checker)"
>
> **Hints:**
> 1. Read about "timing-based side-channel attacks."
> 2. Attempting to reverse-engineer or exploit the binary won't help you, you can figure out the PIN just by interacting with it and measuring certain properties about it.
> 3. Don't run your attacks against the master server, it is secured against them. The PIN code you get from the `pin_checker` binary is the same as the one for the master server.

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2022
- **Autor:** Anish Singhani

## Solución
El reto proporciona un ejecutable compilado (`pin_checker`) y un servicio remoto en red.

1. **Ataque de canal lateral basado en tiempos (*Timing Side-Channel*):**
   - El programa solicita un código PIN numérico de 8 dígitos y realiza una validación dígito a dígito de izquierda a derecha.
   - Cada coincidencia correcta introduce un retraso deliberado o ejecuta ciclos adicionales de cómputo antes de proceder con el siguiente carácter o retornar `Access denied`.
   - Midiendo con precisión el tiempo de respuesta del ejecutable para cada suposición en una posición determinada, el dígito que produce consistentemente un tiempo de ejecución mayor corresponde al dígito correcto.
   - Esto reduce el espacio de búsqueda de $10^8$ combinaciones totales a solo $8 \times 10 = 80$ comprobaciones.

2. **Automatización del ataque:**
   - Se ejecuta un script en Python que prueba dígitos del `0` al `9` para cada posición, acumulando y promediando los tiempos de ejecución.
   - El PIN descubierto corresponde a `48390513`.

3. **Conexión al servidor principal:**
   - Con el PIN validado localmente, se establece conexión con la instancia maestra en red mediante `nc` o sockets en Python, introduciendo el PIN de 8 dígitos para recibir la bandera legítima.

```python
#!/usr/bin/env python3
import time
import subprocess

pin = ""
for pos in range(8):
    best_digit = None
    max_duration = 0
    for d in "0123456789":
        test_pin = pin + d + "0" * (7 - len(pin))
        start = time.perf_counter()
        proc = subprocess.Popen(
            ["./pin_checker"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        proc.communicate(input=f"{test_pin}\n".encode())
        duration = time.perf_counter() - start
        if duration > max_duration:
            max_duration = duration
            best_digit = d
    pin += best_digit
    print(f"Progreso PIN: {pin}")

print(f"PIN final descubierto: {pin}")
```

```bash
# Conectar al servidor maestro y enviar el PIN descubierto
nc chatelaine.cylabacademy.net <puerto>
```

## Notas adicionales
- Las implementaciones seguras de verificación de secretos deben ejecutarse en tiempo constante (*constant-time comparison*) para evitar la fuga de información mediante canales laterales temporales.

## Referencias
- Reto: https://learn.cylabacademy.org/library/298
- Timing attack fundamentals: https://en.wikipedia.org/wiki/Timing_attack
