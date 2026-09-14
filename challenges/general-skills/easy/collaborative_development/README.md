# General Skills — Collaborative Development

## Descripción
> **Prompt oficial:** "My team has been working very hard on new features for our flag printing program! I wonder how they'll work together?"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Jeffery John

## Solución
El repo Git tiene tres ramas (`feature/part-1`, `feature/part-2`, `feature/part-3`), cada una añadiendo un `print()` con un fragmento de la flag a `flag.py`, todas partiendo del mismo commit base:

```bash
git branch -a
git log --all --oneline --graph

git show feature/part-1:flag.py   # print("picoCTF{t3@mw0rk_", end='')
git show feature/part-2:flag.py   # print("m@k3s_th3_dr3@m_", end='')
git show feature/part-3:flag.py   # print("w0rk_6c06cec1}")
```

Al intentar mezclar las tres ramas se producen conflictos de merge reales (las tres tocan la misma línea/zona del archivo), así que se resuelve a mano concatenando los tres fragmentos en orden y ejecutando el script:

```python
print("Printing the flag...")
print("picoCTF{t3@mw0rk_", end='')
print("m@k3s_th3_dr3@m_", end='')
print("w0rk_6c06cec1}")
```

```bash
python3 flag.py
# picoCTF{t3@mw0rk_m@k3s_th3_dr3@m_w0rk_6c06cec1}
```

Flag: `picoCTF{t3@mw0rk_m@k3s_th3_dr3@m_w0rk_6c06cec1}`

## Notas adicionales
- No hacía falta resolver el merge con Git de forma "correcta" (commitear la resolución, etc.); bastaba con leer el contenido de cada rama con `git show <rama>:<archivo>` y montar el resultado final a mano, ya que el objetivo es solo obtener la flag, no dejar un repo limpio.

## Referencias
- Reto: https://learn.cylabacademy.org/library/410
- Fuente combinada: `flag_merged.py` (copia en esta carpeta)
