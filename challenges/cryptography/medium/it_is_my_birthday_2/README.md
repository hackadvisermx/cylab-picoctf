# It is my Birthday 2

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Fuente:** picoCTF 2021  
**ID CyLab:** 169  
**Puntos:** (on-demand)

---

## Descripción

> My birthday is coming up again, but I want to have a very exclusive party for only the best cryptologists. See if you can solve my challenge, upload 2 valid PDFs that are different but have the same SHA1 hash. They should both have the same 1000 bytes at the end as the original invite.

El servidor provee un PDF original (`invite.pdf`) y requiere que subamos dos PDFs que:
1. Sean archivos diferentes
2. Tengan el mismo hash SHA-1
3. Los últimos 1000 bytes coincidan con los últimos 1000 bytes de `invite.pdf`
4. Sean PDFs válidos

---

## Pistas Clave

1. "This isn't REALLY a birthday attack problem" — No es fuerza bruta de colisión
2. [https://shattered.io/](https://shattered.io/) — Colisión SHA-1 real pre-computada
3. Los PDFs deben ser diferentes
4. Los PDFs deben ser válidos
5. Los últimos 1000 bytes deben coincidir con el PDF original

---

## Análisis

### Colisión SHA-1 con shattered.io

El proyecto [SHAttered](https://shattered.io/) demostró en 2017 la primera colisión práctica de SHA-1. Provee dos PDFs distintos (`shattered-1.pdf` y `shattered-2.pdf`, 422435 bytes cada uno) que producen exactamente el mismo hash SHA-1:

```
SHA1(shattered-1.pdf) = 38762cf7f55934b34d179ae6a4c80cadccbb7f0a
SHA1(shattered-2.pdf) = 38762cf7f55934b34d179ae6a4c80cadccbb7f0a
```

Los PDFs difieren en bytes 192–319 (el bloque de colisión), pero gracias a la construcción Merkle-Damgård de SHA-1, el estado interno converge al mismo valor al final del procesamiento.

### Restricción de los últimos 1000 bytes

El `invite.pdf` tiene 2,247,830 bytes. Sus últimos 1000 bytes son distintos a los de los shattered PDFs.

### Propiedad de extensión de longitud (Length Extension)

La clave es la **propiedad de extensión de Merkle-Damgård**: si `SHA1(M1) = SHA1(M2)` y `len(M1) = len(M2)`, entonces para cualquier sufijo `S`:

```
SHA1(M1 || S) = SHA1(M2 || S)
```

Esto se debe a que el estado interno de SHA-1 después de procesar todos los bloques de M1 y M2 (sin padding final) es **idéntico** — eso es exactamente lo que la colisión garantiza. Al agregar el mismo sufijo `S` a ambos, se procesa desde el mismo estado inicial y se obtiene el mismo hash.

---

## Solución

### Paso 1: Descargar los shattered PDFs

```bash
curl -L https://shattered.io/static/shattered-1.pdf -o shattered-1.pdf
curl -L https://shattered.io/static/shattered-2.pdf -o shattered-2.pdf
```

Verificar colisión:
```bash
openssl sha1 shattered-1.pdf shattered-2.pdf
# SHA1(shattered-1.pdf)= 38762cf7f55934b34d179ae6a4c80cadccbb7f0a
# SHA1(shattered-2.pdf)= 38762cf7f55934b34d179ae6a4c80cadccbb7f0a
```

### Paso 2: Obtener el invite.pdf de la instancia

La API de CyLab retorna la URL del servidor y del invite.pdf al arrancar la instancia (vía `PUT /api/challenges/169/instance/`).

### Paso 3: Crear PDFs modificados

```python
# Extraer últimos 1000 bytes de invite.pdf
with open('invite.pdf', 'rb') as f:
    invite_data = f.read()
last_1000 = invite_data[-1000:]

# Leer shattered PDFs
with open('shattered-1.pdf', 'rb') as f:
    data1 = f.read()
with open('shattered-2.pdf', 'rb') as f:
    data2 = f.read()

# Agregar el sufijo a ambos (preserva la colisión SHA-1)
mod1 = data1 + last_1000
mod2 = data2 + last_1000

# Verificar
import hashlib
assert hashlib.sha1(mod1).hexdigest() == hashlib.sha1(mod2).hexdigest()
assert mod1 != mod2
assert mod1[-1000:] == last_1000
```

Resultado:
- `SHA1(mod1.pdf) = SHA1(mod2.pdf) = 133f99dc4ac356ad2b2b611f82d51fda3451d352`
- Archivos diferentes ✓
- Últimos 1000 bytes == últimos 1000 bytes de invite.pdf ✓

### Paso 4: Subir al servidor del challenge

```python
import requests

CHALLENGE_SERVER = "http://xebec.cylabacademy.net:19214"  # URL dinámica
with open('mod1.pdf', 'rb') as f1, open('mod2.pdf', 'rb') as f2:
    files = {
        'file1': ('mod1.pdf', f1, 'application/pdf'),
        'file2': ('mod2.pdf', f2, 'application/pdf'),
    }
    r = requests.post(CHALLENGE_SERVER + '/upload', files=files)
    print(r.text)
```

El servidor responde con la flag en un alert de Bootstrap:
```
Flag: academy{h4ppy_b1rthd4y_2_m3_8248ffdd}
```

---

## Conceptos Clave

| Concepto | Descripción |
|----------|-------------|
| **Colisión SHA-1** | Dos mensajes distintos con el mismo hash SHA-1 |
| **SHAttered** | Primera colisión SHA-1 práctica (Google/CWI, 2017) |
| **Merkle-Damgård** | Construcción iterativa de SHA-1 por bloques de 512 bits |
| **Length Extension** | Si SHA1(M1)=SHA1(M2) y len(M1)=len(M2), entonces SHA1(M1\|\|S)=SHA1(M2\|\|S) para todo S |

---

## Herramientas

- `curl` — Descarga de PDFs de shattered.io
- `openssl sha1` — Verificación de hashes
- `python3` / `requests` — Construcción de PDFs modificados y upload al servidor

---

*Cuenta: hackadvisermx — CyLab Academy*
