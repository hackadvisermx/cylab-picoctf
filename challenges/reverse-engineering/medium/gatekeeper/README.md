# Reverse Engineering — Gatekeeper

## Descripción
> **Prompt oficial del reto:** "What’s behind the numeric gate? You only get access if you enter the *right* kind of number.
> You can download the program file [here](https://challenge-files.cylabacademy.net/library/f45ca14a736a03777db2db01fea43fec6b367130dfbb4fc268b9a2ab07acca0e/gatekeeper)."
>
> **Pistas oficiales:**
> 1. Tools like **Ghidra**, **IDA Free**, or **Radare2** can analyze the binary’s logic.
> 2. The program’s output isn’t straightforward; reversing the string and cleaning out extra text may help you recover the flag.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
El reto proporciona un binario ejecutable ELF de 64 bits (`gatekeeper`) y una instancia de red a la que conectarse (`nc <host> <puerto>`).

### 1. Análisis del flujo en `main`
Desensamblando la función `main` con `objdump -d -M intel`:
1. El programa solicita una entrada mediante `scanf("%31s")`: `"Enter a numeric code (must be > 999 ): "`.
2. Mide la longitud de la cadena de entrada con `strlen`.
3. Comprueba si la entrada es decimal mediante `is_valid_decimal`:
   - Si contiene exclusivamente dígitos del 0 al 9, la convierte con `atoi`.
4. Si no es decimal, comprueba si es hexadecimal válida con `is_valid_hex`:
   - Si contiene caracteres hexadecimales (incluyendo letras `a-f`), la convierte en base 16 con `strtol(..., NULL, 16)`.
5. Valida las siguientes tres condiciones sobre el valor y la cadena:
   - `valor > 999` (`0x3e7`)
   - `valor <= 9999` (`0x270f`)
   - `strlen == 3` (`cmp dword ptr [rbp - 0x34], 0x3`)

Cualquier número decimal mayor que 999 requiere al menos 4 dígitos, por lo que es imposible satisfacer la condición `strlen == 3` con un número decimal puro. Sin embargo, en hexadecimal un número de 3 dígitos puede superar 999: por ejemplo, `3e8` en hexadecimal equivale a `1000` en decimal ($3 \times 16^2 + 14 \times 16 + 8 = 1000$).
Como `3e8` contiene la letra `e`, no es decimal puro, es aceptado por `is_valid_hex`, su valor es $1000 > 999$ y su longitud es exactamente 3 caracteres.

### 2. Análisis de `reveal_flag`
Al cumplirse las condiciones, se invoca `reveal_flag`:
1. Lee el archivo `/flag.txt`.
2. Itera desde el último carácter hacia el primero ($i = \text{len} - 1 \dots 0$):
   - Imprime `flag[i]` mediante `putchar`.
   - Si el índice original cumple $(i \ \& \ 3) == 0$, imprime intercalada la cadena constante `"ftc_oc_ip"`.

### 3. Reconstrucción de la bandera
Para recuperar la flag:
1. Conectarse a la instancia y enviar la clave `3e8`.
2. Tomar el texto generado tras `"Access granted: "`.
3. Eliminar todas las ocurrencias del patrón intercalado `"ftc_oc_ip"`.
4. Invertir la cadena resultante.

```python
import socket

s = socket.create_connection(('<host>', <puerto>))
s.recv(1024)
s.sendall(b'3e8\n')
resp = s.recv(4096).decode()

text = resp.split('Access granted:')[1].strip()
cleaned = text.replace('ftc_oc_ip', '')
flag = cleaned[::-1]
print("Flag:", flag)
```

Salida:
```text
Access granted: }ce6ftc_oc_ipf335ftc_oc_ipd_99ftc_oc_ip9_TGftc_oc_ip_xehftc_oc_ip_tigftc_oc_ipid_3ftc_oc_ip{ymeftc_oc_ipdacaftc_oc_ip

Flag: academy{...}
```

## Notas adicionales
- El nombre mismo de la flag (`3_digit_hex_GT_999`) confirma la premisa del reto: requerir un número hexadecimal de 3 caracteres cuyo valor supere 999.

## Referencias
- Reto: https://learn.cylabacademy.org/library/731
