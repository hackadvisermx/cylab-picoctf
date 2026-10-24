# Reverse Engineering — patchme.py

## Descripción
> **Prompt oficial del reto:** "Can you get the flag? Run this Python program in the same directory as this encrypted flag."
>
> **Pistas oficiales:**
> (Ninguna pista proporcionada en la plataforma)

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona un script en Python (`patchme.flag.py`) y un archivo binario que contiene la bandera cifrada (`flag.txt.enc`).

### 1. Análisis del código fuente
Al inspeccionar `patchme.flag.py`:

```python
def str_xor(secret, key):
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key = new_key + key[i]
        i = (i + 1) % len(key)        
    return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c,new_key_c) in zip(secret,new_key)])

flag_enc = open('flag.txt.enc', 'rb').read()

def level_1_pw_check():
    user_pw = input("Please enter correct password for flag: ")
    if( user_pw == "ak98" + "-=90" + "adfjhgj321" + "sleuth9000"):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), "utilitarian")
        print(decryption)
        return
    print("That password is incorrect")

level_1_pw_check()
```

La comprobación de contraseña evalúa la cadena concatenada `ak98-=90adfjhgj321sleuth9000`. Al ser válida, descifra el archivo `flag.txt.enc` aplicando un XOR carácter a carácter contra la clave repetida `"utilitarian"`.

### 2. Resolución
Se puede resolver directamente ejecutando la rutina de descifrado en un script independiente sin requerir la entrada del usuario:

```python
def str_xor(secret, key):
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key = new_key + key[i]
        i = (i + 1) % len(key)        
    return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c,new_key_c) in zip(secret,new_key)])

flag_enc = open('flag.txt.enc', 'rb').read()
decryption = str_xor(flag_enc.decode(), "utilitarian")
print(decryption)
```

Al ejecutar el script se imprime directamente la bandera descifrada en formato `academy{...}`.

## Notas adicionales
- El cifrado XOR con clave repetida es vulnerable al análisis de frecuencia y a la extracción directa de la clave cuando ésta se encuentra expuesta en el código fuente del cliente.

## Referencias
- Reto: https://learn.cylabacademy.org/library/287
- XOR cipher: https://en.wikipedia.org/wiki/XOR_cipher
