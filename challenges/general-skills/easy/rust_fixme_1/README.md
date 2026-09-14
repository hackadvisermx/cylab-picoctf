# General Skills — Rust fixme 1

## Descripción
> **Prompt oficial:** "Have you heard of Rust? Fix the syntax errors in this Rust file to print the flag! Download the Rust code here."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2025
- **Autor:** Taylor McCampbell

## Solución
El primero de la serie "Rust fixme" (más sencillo que el 2 y el 3): tres errores de **sintaxis** básica, cada uno señalado con un comentario-pista:

1. Falta el `;` al final de `let key = String::from("CSUCKS")`.
2. `ret;` no es una palabra clave válida en Rust — es `return;`.
3. `println!(":?", ...)` no interpola nada — el placeholder correcto es `"{}"` (o `"{:?}"` para debug).

```bash
tar xzf fixme1.tar.gz && cd fixme1
# aplicar las 3 correcciones de arriba en src/main.rs
cargo run
# picoCTF{...}
```

Flag: `picoCTF{4r3_y0u_4_ru$t4c30n_n0w?}`

## Notas adicionales
- Primero de la trilogía "Rust fixme" del mismo autor; los tres comparten estructura (descifrado XOR de un array hex con el crate `xor_cryptor`) pero cada uno introduce un tipo de error distinto: sintaxis básica (este), mutabilidad/borrowing (`Rust fixme 2`), y bloques `unsafe` (`Rust fixme 3`).

## Referencias
- Reto: https://learn.cylabacademy.org/library/461
- Fuente corregida: `main_fixed.rs` (copia en esta carpeta)
