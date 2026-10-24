# Cryptography — ChaCha Slide

## Descripción
> **Prompt oficial del reto:** "Modern authenticated-encryption ciphers like ChaCha20-Poly1305 are great, but they can quickly fall apart if their limits aren't respected. Can you violate the integrity of a message encrypted by this program?
> 
> Connect to the program with netcat: `$ nc <host> <port>`
> 
> The program's source code can be downloaded [here](https://challenge-files.cylabacademy.net/library/ded5eb9e89d0eac045123bf22a7c3836dbf343afa1016ef1d0c321259d312160/challenge.py)."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2025
- **Autor:** asinghani

## Solución
El servicio interactivo cifra dos mensajes conocidos utilizando el algoritmo autenticado `ChaCha20-Poly1305` (RFC 8439), pero comete el error crítico de reutilizar el mismo par (clave, nonce) para ambos mensajes. Posteriormente, solicita al usuario un mensaje cifrado que incluya el tag y nonce; si al descifrarlo contiene la cadena objetivo `"But it's only secure if used correctly!"`, entrega la flag.

### Vulnerabilidades de reutilización de nonce en ChaCha20-Poly1305:
1. **Pérdida de confidencialidad (ChaCha20 keystream reuse):**
   Al reutilizarse el nonce, el flujo de clave (keystream) generado por ChaCha20 es idéntico:
   $$K_s = C_1 \oplus P_1$$
   Podemos cifrar cualquier texto plano $P_{forged}$ de longitud hasta 77 bytes calculando directamente $C_{forged} = P_{forged} \oplus K_s$.
2. **Pérdida de integridad y falsificación de MAC (Poly1305 tag forgery):**
   Poly1305 deriva una clave de un solo uso $(r, s)$ a partir del primer bloque de 64 bytes de ChaCha20. Si el nonce se reutiliza, $(r, s)$ es idéntico entre mensajes.
   El tag de autenticación se evalúa como:
   $$\text{tag} \equiv P(r) + s \pmod{2^{128}}$$
   donde $P(r)$ es un polinomio cuyos coeficientes derivan de los bloques de 16 bytes del texto cifrado y los metadatos sobre $\mathbb{F}_p$ con $p = 2^{130} - 5$.
   Para dos mensajes con tags $t_1, t_2$:
   $$(P_1(r) - P_2(r)) - (t_1 - t_2 + (k_1 - k_2) \cdot 2^{128}) \equiv 0 \pmod p$$
   Probando los posibles valores enteros pequeños de $k_1, k_2 \in [0, 7]$ y calculando las raíces en $\mathbb{F}_p$ mediante `flint.fmpz_mod_poly.roots()`, recuperamos la clave secreta $r$ (que debe cumplir la máscara de clamping de Poly1305) y la clave aditiva $s$.

Una vez conocidos $(r, s)$, evaluamos el polinomio para $C_{forged}$ correspondiente al texto objetivo y calculamos su tag válido $tag_{forged} = (P_{forged}(r) + s) \bmod 2^{128}$.
Enviamos $C_{forged} \parallel tag_{forged} \parallel nonce$ en hexadecimal y el servidor valida la integridad devolviendo la flag.

```python
# Recuperación de raíces en F_p con FLINT y falsificación de Poly1305
p = 2**130 - 5
pp = 2**128
R_ctx = flint.fmpz_mod_poly_ctx(p)

# Construir polinomios P1 y P2 a partir de c1 y c2
...
for k1 in range(8):
    for k2 in range(8):
        diff_tag = (t1 + k1 * pp) - (t2 + k2 * pp)
        diff_poly = (P1 - P2) - R_ctx([diff_tag % p])
        for root_val, _ in diff_poly.roots():
            r_cand = int(root_val)
            if (r_cand & 0x0ffffffc0ffffffc0ffffffc0fffffff) == r_cand:
                s_cand = (t1 - eval_poly(coeffs1, r_cand)) % pp
                if (eval_poly(coeffs2, r_cand) + s_cand) % pp == t2:
                    r, s_val = r_cand, s_cand
                    break

# Falsificar mensaje objetivo
c_goal = bytes(a ^ b for a, b in zip(goal, ks[:len(goal)]))
tag_goal = int((eval_poly(coeffs_goal, r) + s_val) % pp).to_bytes(16, 'little')
payload = c_goal + tag_goal + nonce
```

Al enviar el payload se supera `decrypt_and_verify()` y se obtiene la flag con formato `academy{...}`.

## Notas adicionales
La seguridad de los esquemas AEAD basados en Wegman-Carter (como ChaCha20-Poly1305 y AES-GCM) depende críticamente de que los nonces nunca se repitan bajo la misma clave. Reutilizar un nonce destruye simultáneamente tanto la confidencialidad como la autenticidad del protocolo.

## Referencias
- Reto: https://learn.cylabacademy.org/library/493
- ChaCha20 and Poly1305 for IETF Protocols: https://datatracker.ietf.org/doc/html/rfc8439
- Nonce-Disrespecting Adversaries (Poly1305 Key Recovery): https://eprint.iacr.org/2016/475
