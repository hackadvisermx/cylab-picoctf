# Forensics — scrambled-bytes

## Descripción
> **Prompt oficial del reto:** "I sent my secret flag over the wires, but the bytes got all mixed up!"

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoMini by redpwn
- **Autor:** kfb

## Solución
El reto involucra una transmisión de red desordenada que envía los bytes de un archivo de bandera a través de paquetes UDP individuales.

1. **Análisis del protocolo y algoritmo de transmisión (`send.py`):**
   - El script de transmisión lee la carga útil completa del archivo de la bandera.
   - Inicializa el generador de números pseudoaleatorios de Python con la marca de tiempo Unix actual en segundos enteros: `random.seed(int(time()))`.
   - Desordena aleatoriamente el orden de los bytes del archivo original usando `random.shuffle(payload)`.
   - Transmite cada byte individualmente dentro de la carga útil de un paquete UDP (`dport=56742`), ofuscándolo mediante una operación XOR con un byte aleatorio (`b ^ random.randrange(256)`) y asignando un puerto de origen aleatorio (`sport=random.randrange(65536)`).

2. **Reversión del proceso y reconstrucción del archivo:**
   - La semilla del PRNG corresponde al timestamp Unix del primer paquete capturado en el archivo `capture.pcapng`.
   - Inicializando `random.seed(timestamp)`, se replica exactamente la secuencia determinista de operaciones aleatorias de Python: la misma permutación de `random.shuffle` y la misma secuencia de claves XOR de `random.randrange(256)`.
   - Al invertir las operaciones XOR y reordenar cada byte en su posición original, se reconstruye un archivo de imagen en formato PNG que contiene la bandera escrita a mano.

```python
#!/usr/bin/env python3
import random
from scapy.all import rdpcap, UDP, Raw

# Leer paquetes dirigidos al puerto de destino
packets = [p for p in rdpcap("capture.pcapng") if UDP in p and p[UDP].dport == 56742]
data = bytearray(b"".join(bytes(p[UDP][Raw].load) for p in packets))

# Inicializar PRNG con el timestamp del primer paquete
seed_time = int(packets[0].time)
random.seed(seed_time)

# Reconstruir permutación original
indices = list(range(len(data)))
random.shuffle(indices)

recovered = bytearray(len(data))
for i in range(len(data)):
    _ = random.randrange(65536)  # Sincronización del puerto de origen
    recovered[indices[i]] = data[i] ^ random.randrange(256)

with open("recovered_flag.png", "wb") as f:
    f.write(recovered)

print("Archivo PNG recuperado exitosamente como recovered_flag.png")
```

## Notas adicionales
- Los generadores de números pseudoaleatorios basados en el algoritmo Mersenne Twister (`random` en Python) no son criptográficamente seguros (CSPRNG) y reproducen secuencias idénticas si se conoce la semilla inicial.

## Referencias
- Reto: https://learn.cylabacademy.org/library/206
- Python `random` module documentation: https://docs.python.org/3/library/random.html
- Scapy packet manipulation library: https://scapy.net/
