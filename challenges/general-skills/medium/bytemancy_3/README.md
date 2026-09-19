# General Skills — bytemancy 3

## Descripción
> **Prompt oficial del reto:** "Can you conjure the right bytes? The program's source code can be downloaded here and the compiled spellbook binary can be downloaded here. Connect to the program with netcat."
>
> **Hints:**
> 1. `objdump -t spellbook` reveals the symbol table.
> 2. Send the addresses as 4 raw bytes in little-endian order.
> 3. `pwnlib.util.packing.p32()` simplifies crafting the payloads.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

## Solución
Se entregan `app.py` (el servidor que corre por `nc`) y el binario `spellbook` (ELF 32-bit, no *stripped*) que el servidor carga con `pwntools.ELF`. El servidor elige al azar 3 de 4 nombres de función (`ember_sigil`, `glyph_conflux`, `astral_spark`, `binding_word`) y por cada uno pide, en texto plano, su **dirección de 4 bytes little-endian** dentro del binario (`p32(elf.symbols[symbol])`).

Como el binario no está *stripped*, sus símbolos son públicos — no hace falta ni ejecutar el programa, solo leer su tabla de símbolos localmente:

```bash
nm spellbook | grep -E "ember_sigil|glyph_conflux|astral_spark|binding_word"
# 080491c1 T astral_spark
# 080491e3 T binding_word
# 08049176 T ember_sigil
# 0804919a T glyph_conflux
```

Con las 4 direcciones ya conocidas de antemano, basta con parsear qué símbolo pide el servidor en cada ronda (aparece en el propio texto del prompt) y responder con `struct.pack("<I", addr)`:

```python
import socket, struct, re

ADDRS = {
    "astral_spark": 0x080491c1, "binding_word": 0x080491e3,
    "ember_sigil": 0x08049176, "glyph_conflux": 0x0804919a,
}
s = socket.create_connection(("<host>", <puerto>), timeout=10)

def recv_until_prompt():
    buf = b""
    s.settimeout(3)
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk: break
            buf += chunk
            if b"==> " in buf: break
    except socket.timeout:
        pass
    return buf

for _ in range(3):
    text = recv_until_prompt().decode(errors="replace")
    name = re.search(r"procedure '([a-z_]+)'", text).group(1)
    s.sendall(struct.pack("<I", ADDRS[name]))

print(recv_until_prompt().decode(errors="replace"))  # -> flag
```

## Notas adicionales
- El propio servidor documenta la técnica en el nombre de la flag: `0bjdump_m4g1c` — el reto es en esencia un ejercicio de usar `nm`/`objdump`/`readelf` para leer la tabla de símbolos de un binario no-stripped, en vez de desensamblar nada.
- No fue necesario usar `pwntools` (no instalado localmente): `nm` del binario ya da las direcciones exactas que el propio servidor calcula con `elf.symbols[...]`, ya que ambos leen la misma tabla de símbolos ELF.
- El orden y subconjunto de símbolos preguntados es aleatorio (`random.sample`) en cada conexión, pero como las 4 direcciones se conocen de antemano (son fijas para ese binario), no importa qué combinación pida el servidor.

## Referencias
- Reto: https://learn.cylabacademy.org/library/730
