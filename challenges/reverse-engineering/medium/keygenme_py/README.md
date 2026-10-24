# Reverse Engineering — keygenme-py

## Descripción
> **Prompt oficial del reto:** "[keygenme-trial.py](https://challenge-files.cylabacademy.net/library/31247278e77f2e7816292c5e1edf37cd08c91b283367d7284edfe15070baf89c/keygenme-trial.py)"
>
> **Pistas oficiales:** Ninguna

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
El reto consiste en un script de Python (`keygenme-trial.py`) que simula una versión de prueba (*trial*) de un software con un sistema de verificación de licencia (*keygenme*).

Al analizar el código:
1. Define las variables base de la licencia:
   ```python
   bUsername_trial = b"MILLER"
   key_part_static1_trial = "academy{1n_7h3_kk3y_of_"
   key_part_dynamic1_trial = "xxxxxxxx"
   key_part_static2_trial = "}"
   key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial
   ```
2. La función `check_key(key, username_trial)` valida la clave ingresada:
   - Comprueba que la longitud coincida con la plantilla completa.
   - Comprueba que la primera parte coincida con `key_part_static1_trial`.
   - Comprueba los 8 caracteres dinámicos intermedios contra posiciones específicas del hash SHA-256 de `bUsername_trial`:
     - `key[i] == hashlib.sha256(username_trial).hexdigest()[4]`
     - `key[i] == hashlib.sha256(username_trial).hexdigest()[5]`
     - `key[i] == hashlib.sha256(username_trial).hexdigest()[3]`
     - `key[i] == hashlib.sha256(username_trial).hexdigest()[6]`
     - `key[i] == hashlib.sha256(username_trial).hexdigest()[2]`
     - `key[i] == hashlib.sha256(username_trial).hexdigest()[7]`
     - `key[i] == hashlib.sha256(username_trial).hexdigest()[1]`
     - `key[i] == hashlib.sha256(username_trial).hexdigest()[8]`
   - Comprueba que el último carácter sea el cierre `}`.

### Generador de Clave (Keygen)

Podemos escribir un generador que reproduzca exactamente las reglas de validación para el usuario `b"MILLER"`:

```python
import hashlib

username = b"MILLER"
prefix = "academy{1n_7h3_kk3y_of_"
suffix = "}"

h = hashlib.sha256(username).hexdigest()
indices = [4, 5, 3, 6, 2, 7, 1, 8]
dynamic = "".join(h[idx] for idx in indices)

full_key = prefix + dynamic + suffix
print("Clave completa:", full_key)
```

Al ejecutar el script de generación:

```bash
python3 keygen.py
```

Se obtiene la clave válida, la cual cumple la condición de validación y corresponde a la bandera en formato `academy{...}`.

## Notas adicionales
Al estudiar un sistema de protección por clave de producto (*product activation / key validation*), si la función de verificación utiliza funciones unidireccionales (como SHA-256) sobre datos conocidos (como el nombre de usuario de prueba), el generador se deriva directamente extrayendo la secuencia exacta de índices utilizados por el algoritmo de comprobación.

## Referencias
- Reto: https://learn.cylabacademy.org/library/121
- Apoyo: https://docs.python.org/3/library/hashlib.html
