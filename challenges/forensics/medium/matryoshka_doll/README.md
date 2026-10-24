# Forensics — Matryoshka doll

## Descripción
> **Prompt oficial del reto:** "Matryoshka dolls are a set of wooden dolls of decreasing size placed one inside another. What's the final one?
> Image: [dolls.jpg](https://challenge-files.cylabacademy.net/library/2eb277d09563812ad880fdd564d0fb59c084a64f514f6e12998534c8f7997405/dolls.jpg)"
>
> **Hints:**
> - "Wait, you can hide files inside files? But how do you find them?"
> - "Make sure to submit the flag as academy{XXXXX}"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Susie/Pandu

## Solución
El reto se basa en el concepto de muñecas rusas (*matrioshkas*), donde un objeto contiene recursivamente réplicas más pequeñas en su interior. En términos forenses, esto representa múltiples archivos de imagen concatenados con contenedores ZIP incrustados.

### Paso 1: Análisis de firmas binarias
Al analizar la imagen `dolls.jpg` con herramientas de extracción como `binwalk` o `7zz`, se observa que más allá del marcador de fin de imagen JPEG (`FF D9`), existe un archivo ZIP adosado con offset:

```bash
7zz l dolls.jpg
# Type = zip, Offset = 272492
# Contiene: base_images/2_c.jpg
```

### Paso 2: Desempaquetado recursivo
Extraemos sucesivamente cada capa oculta:

1. **Primera capa:**
   ```bash
   7zz x dolls.jpg -y
   # Extrae: base_images/2_c.jpg
   ```

2. **Segunda capa:**
   ```bash
   7zz x base_images/2_c.jpg -y
   # Extrae: base_images/3_c.jpg
   ```

3. **Tercera capa:**
   ```bash
   7zz x base_images/3_c.jpg -y
   # Extrae: base_images/4_c.jpg
   ```

4. **Cuarta capa (final):**
   ```bash
   7zz x base_images/4_c.jpg -y
   # Extrae: flag.txt
   ```

### Paso 3: Obtención de la flag
Leemos el archivo `flag.txt` resultante:

```bash
cat flag.txt
# academy{...}
```

## Notas adicionales
- Este tipo de técnica se conoce como archivo *políglota* o simplemente concatenación binaria post-EOI (*End of Image*). Dado que los visores JPEG finalizan la lectura del archivo al encontrar el marcador `FF D9`, cualquier información adjunta después de ese byte es invisible en el visor pero recuperable por descompresores y analizadores de firmas.

## Referencias
- Reto: https://learn.cylabacademy.org/library/129
- Formato de compresión ZIP: https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
