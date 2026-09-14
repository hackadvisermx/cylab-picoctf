# General Skills — Bases

## Descripción
> **Prompt oficial:** "What does this bDNhcm5fdGgzX3IwcDM1 mean? I think it has something to do with bases."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2019
- **Autor:** Sanjay C/Danny T

## Solución
Base64.

```bash
python3 -c "import base64; print(base64.b64decode('bDNhcm5fdGgzX3IwcDM1').decode())"
# l3arn_th3_r0p35
```

Flag: `picoCTF{l3arn_th3_r0p35}`

## Referencias
- Reto: https://learn.cylabacademy.org/library/67
