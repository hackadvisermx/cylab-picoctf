# General Skills — Rust fixme 2

## Descripción
> **Prompt oficial:** "The Rust saga continues? I ask you, can I borrow that, pleeeeeaaaasseeeee? Download the Rust code here."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2025
- **Autor:** Taylor McCampbell

## Solución
Bug de **mutabilidad/borrowing** en Rust: la función recibe el string por referencia inmutable (`&String`) pero intenta mutarlo con `push_str`, y además la variable original (`party_foul`) no está declarada `mut`.

```rust
// antes
fn decrypt(encrypted_buffer: Vec<u8>, borrowed_string: &String) { ... borrowed_string.push_str(...) ... }
let party_foul = String::from("...");
decrypt(encrypted_buffer, &party_foul);

// después
fn decrypt(encrypted_buffer: Vec<u8>, borrowed_string: &mut String) { ... }
let mut party_foul = String::from("...");
decrypt(encrypted_buffer, &mut party_foul);
```

```bash
tar xzf fixme2.tar.gz && cd fixme2
# aplicar los 3 cambios de arriba en src/main.rs
cargo run
# Using memory unsafe languages is a: PARTY FOUL! Here is your flag: picoCTF{...}
```

Flag: `picoCTF{4r3_y0u_h4v1n5_fun_y31?}`

## Notas adicionales
- Los propios comentarios del código ("How do we pass values to a function that we want to change?", "Is this variable changeable?") son pistas explícitas de que el fallo es sobre mutabilidad/paso por referencia, no sobre lógica de descifrado.
- Mismo patrón de "fix the Rust bug" que `Rust fixme 3` (mismo autor, misma serie), pero aquí el error es de *ownership/borrowing* en vez de `unsafe`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/462
- Fuente corregida: `main_fixed.rs` (copia en esta carpeta)
