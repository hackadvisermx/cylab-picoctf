# Reverse Engineering — unpackme.py

## Descripción
> **Prompt oficial del reto:** "Can you get the flag? Reverse engineer this Python program."
>
> **Pistas oficiales:**
> (Ninguna pista proporcionada en la plataforma)

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto suministra un script en Python (`unpackme.flag.py`) que implementa un descargador/desempaquetador cifrado con el módulo `cryptography.fernet`.

### 1. Análisis del código fuente
Al inspeccionar el script:

```python
import base64
from cryptography.fernet import Fernet

payload = b'gAAAAABqsz7kB3yvHgPuGHG-jyvz_Zexm0uvOQfcJmzDMDtgdWrzNOXb6V_SpgadHAMWuxZD2i1_PCP8ntLibH_270XtF8irAVLkNxNFZVnRAzsSZcZHs915XILGype7Aea_ePekULHIskj-ReBp1Tpw0ATAkt9GAYFIXcxvzHyTKKVMxHlQjUYsUR-L2UjaGNfAXwZarltInQxU1gCUzk26La2pJ10CzvKUPAZT_cJIJu75r9x0QoWDufnoJ6jjUBKUimICw9EuWq-RNIOzJCYLQJkCh2LJug=='

key_str = 'correctstaplecorrectstaplecorrec'
key_base64 = base64.b64encode(key_str.encode())
f = Fernet(key_base64)
plain = f.decrypt(payload)
exec(plain.decode())
```

El script genera una clave simétrica a partir de la cadena estática `key_str`, descifra el bloque de datos `payload` usando Fernet, y finalmente ejecuta el resultado con la función `exec()`.

### 2. Extracción estática de la carga útil
Para obtener el código fuente original sin ejecutarlo, se reemplaza la llamada a `exec(plain.decode())` por una impresión directa por consola:

```python
import base64
from cryptography.fernet import Fernet

payload = b'gAAAAABqsz7kB3yvHgPuGHG-jyvz_Zexm0uvOQfcJmzDMDtgdWrzNOXb6V_SpgadHAMWuxZD2i1_PCP8ntLibH_270XtF8irAVLkNxNFZVnRAzsSZcZHs915XILGype7Aea_ePekULHIskj-ReBp1Tpw0ATAkt9GAYFIXcxvzHyTKKVMxHlQjUYsUR-L2UjaGNfAXwZarltInQxU1gCUzk26La2pJ10CzvKUPAZT_cJIJu75r9x0QoWDufnoJ6jjUBKUimICw9EuWq-RNIOzJCYLQJkCh2LJug=='
key_str = 'correctstaplecorrectstaplecorrec'
key_base64 = base64.b64encode(key_str.encode())
f = Fernet(key_base64)
plain = f.decrypt(payload)
print(plain.decode())
```

Salida del programa:
```python
pw = input('What\'s the password? ')

if pw == 'batteryhorse':
  print('academy{...}')
else:
  print('That password is incorrect.')
```

El bloque descifrado contiene directamente la bandera en formato `academy{...}`.

## Notas adicionales
- La sustitución de `exec()` o `eval()` por `print()` es el método elemental para neutralizar cargadores (*droppers*) de primer nivel en análisis de malware o empaquetadores basados en scripts.

## Referencias
- Reto: https://learn.cylabacademy.org/library/314
- Cryptography Fernet Documentation: https://cryptography.io/en/latest/fernet/
