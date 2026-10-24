# Cryptography — rsa-pop-quiz

## Descripción
> **Prompt oficial del reto:** "Class, take your seats! It's PRIME-time for a quiz..."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** wparks/nmontierth

## Solución
El reto presenta un cuestionario interactivo sobre los fundamentos matemáticos del criptosistema RSA. Para cada pregunta, el servidor proporciona ciertos parámetros conocidos, define una incógnita objetivo y pregunta si es posible y computacionalmente factible calcular dicho objetivo (`IS THIS POSSIBLE and FEASIBLE? (Y/N)`).

Si es factible, se responde `Y` y se ingresa el valor entero en base decimal; de lo contrario, se responde `N`.

### Reglas matemáticas de RSA evaluadas
1. **$p, q \to n$**: Factible. $n = p \cdot q$.
2. **$p, n \to q$**: Factible. $q = n // p$.
3. **$e, n \to p, q$**: No factible con números de 2048 bits (problema de factorización entera clásica).
4. **$p, q \to \text{totient}(n)$**: Factible. $\phi(n) = (p-1)(q-1)$.
5. **$\text{plaintext}, e, n \to \text{ciphertext}$**: Factible. $c = m^e \pmod n$.
6. **$\text{ciphertext}, e, n \to \text{plaintext}$**: No factible sin la clave privada ni la factorización de $n$.
7. **$e, p, q \to d$**: Factible. $\phi(n) = (p-1)(q-1)$, $d = e^{-1} \pmod{\phi(n)}$.
8. **$\text{ciphertext}, e, n, p \to \text{plaintext}$**: Factible. $q = n // p$, $\phi = (p-1)(q-1)$, $d = e^{-1} \pmod \phi$, $m = c^d \pmod n$.

Al responder satisfactoriamente la octava pregunta, el texto plano devuelto corresponde a la bandera codificada en formato numérico (Big Endian).

### Script de automatización
```bash
python3 - << 'EOF'
import socket
import re
from Crypto.Util.number import long_to_bytes

s = socket.create_connection(("chatelaine.cylabacademy.net", 31857))

def recv_until(sock, markers):
    buf = ""
    while True:
        chunk = sock.recv(1024).decode("utf-8", errors="ignore")
        if not chunk: break
        buf += chunk
        for m in markers:
            if m in buf: return buf
    return buf

while True:
    buf = recv_until(s, ["IS THIS POSSIBLE and FEASIBLE? (Y/N):", "academy{", "plaintext:"])
    if "IS THIS POSSIBLE and FEASIBLE? (Y/N):" not in buf:
        # Fin del quiz o mensaje final
        extra = s.recv(4096).decode("utf-8", errors="ignore")
        print(buf + extra)
        break

    prob = buf.split("#### NEW PROBLEM ####")[-1]
    params = {}
    for line in prob.split("\n"):
        if " : " in line:
            k, v = line.split(" : ", 1)
            try: params[k.strip()] = int(v.strip())
            except: pass

    target_match = re.search(r"PRODUCE THE FOLLOWING ####\s*([^\n\r]+)", prob)
    target = target_match.group(1).strip() if target_match else ""

    ans = None
    if "totient" in target and "p" in params and "q" in params:
        ans = (params["p"] - 1) * (params["q"] - 1)
    elif target == "n" and "p" in params and "q" in params:
        ans = params["p"] * params["q"]
    elif target == "q" and "n" in params and "p" in params:
        ans = params["n"] // params["p"]
    elif target == "p" and "n" in params and "q" in params:
        ans = params["n"] // params["q"]
    elif target in ("p\nq", "p", "q") and "e" in params and "n" in params and len(params) == 2:
        ans = None
    elif target == "d" and "p" in params and "q" in params and "e" in params:
        ans = pow(params["e"], -1, (params["p"] - 1) * (params["q"] - 1))
    elif "ciphertext" in target and "plaintext" in params and "e" in params and "n" in params:
        ans = pow(params["plaintext"], params["e"], params["n"])
    elif "plaintext" in target and "ciphertext" in params and "e" in params and "n" in params and "p" in params:
        q = params["n"] // params["p"]
        d = pow(params["e"], -1, (params["p"] - 1) * (q - 1))
        ans = pow(params["ciphertext"], d, params["n"])
    elif "plaintext" in target and "ciphertext" in params and "e" in params and "n" in params:
        ans = None

    if ans is not None:
        s.sendall(b"y\n")
        # Esperar prompt para valor
        p_buf = ""
        while not p_buf.endswith(": "):
            p_buf += s.recv(1).decode("utf-8", errors="ignore")
        s.sendall(f"{ans}\n".encode())
    else:
        s.sendall(b"n\n")

s.close()
EOF
```

Convirtiendo el último entero `plaintext` a bytes:
```python
long_to_bytes(plaintext).decode()
```
Se obtiene la bandera en formato `academy{...}`.

## Notas adicionales
- Las preguntas demuestran la diferencia entre operaciones polinomiales eficientes (multiplicación, división, inversión modular con el algoritmo extendido de Euclides, exponenciación modular) y problemas intratables (factorización de enteros grandes sin información auxiliar).

## Referencias
- Reto: https://learn.cylabacademy.org/library/61
- Apoyo: Rivest, Shamir, Adleman (1978), *A Method for Obtaining Digital Signatures and Public-Key Cryptosystems*
