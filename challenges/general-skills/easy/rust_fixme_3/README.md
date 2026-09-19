# General Skills — Rust fixme 3

## Descripción
> **Prompt oficial:** "Have you heard of Rust? Fix the syntax errors in this Rust file to print the flag! Download the Rust code here."
>
> **Hints:**
> 1. Read the comments...darn it!

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2025
- **Autor:** Taylor McCampbell

## Solución
El proyecto (`fixme3.tar.gz`, un crate de Cargo) no compila: `std::slice::from_raw_parts` es una función **`unsafe`** de Rust y se llama fuera de un bloque `unsafe { ... }`. El propio código deja ver, comentado, que originalmente estaba envuelto en `unsafe { }` (con una explicación didáctica sobre por qué Rust exige marcar explícitamente ese tipo de operaciones).

Corrección (una sola línea):

```rust
// antes
let decrypted_slice = std::slice::from_raw_parts(decrypted_ptr, decrypted_len);

// después
let decrypted_slice = unsafe { std::slice::from_raw_parts(decrypted_ptr, decrypted_len) };
```

```bash
tar xzf fixme3.tar.gz
cd fixme3
# aplicar la corrección de arriba en src/main.rs
cargo run
# Using memory unsafe languages is a: PARTY FOUL! Here is your flag: picoCTF{...}
```

Flag: `picoCTF{n0w_y0uv3_f1x3d_1h3m_411}`

## Notas adicionales
- Rust y Cargo estaban ya instalados localmente (`~/.cargo/bin`), así que se compiló y ejecutó directamente en la máquina local en vez de depender del webshell (que de hecho el propio reto marca como "This problem is not solvable with the webshell").
- El resto del programa (descifrado XOR de un array de hex mediante el crate `xor_cryptor`) no necesitaba tocarse — el único error real era la falta de la palabra clave `unsafe`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/463
- Fuente corregida: `main_fixed.rs` (copia en esta carpeta)
