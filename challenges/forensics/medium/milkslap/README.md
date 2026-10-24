# Forensics — Milkslap

## Descripción
> **Prompt oficial del reto:** "🥛"
>
> **Hints:**
> - "Look at the problem category"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** James Lynch

## Solución
El reto presenta un sitio web interactivo con una animación en la que un vaso de leche es lanzado a la cara de una persona conforme se desplaza el ratón. Dado que la categoría es *Forensics*, el objetivo es analizar los recursos multimedia de la aplicación web en busca de información oculta mediante esteganografía.

### Paso 1: Localización del recurso de imagen
Inspeccionando el código fuente de la página o los archivos CSS cargados (`style.css`), encontramos la hoja de sprites que contiene los fotogramas de la animación:

```css
#image {
    height: 720px;
    margin-top: 5%;
    margin-bottom: 20px;
    background-image: url(concat_v.png);
    background-position: 0 0;
}
```

Descargamos el archivo `concat_v.png` directamente desde el servidor:

```bash
curl -sSL -o concat_v.png "http://<instance-host>:<port>/concat_v.png"
```

### Paso 2: Análisis esteganográfico con zsteg
Utilizamos la herramienta de análisis esteganográfico para imágenes PNG `zsteg`, la cual evalúa los bits menos significativos (LSB) en diferentes canales de color:

```bash
zsteg concat_v.png
```

La herramienta detecta una carga útil de texto legible almacenada en el canal `b1,b,lsb,xy`:
```text
b1,b,lsb,xy .. text: "academy{...}\n"
```

El contenido extraído corresponde a la flag del reto.

## Notas adicionales
- `concat_v.png` es una tira de imágenes combinadas verticalmente (*vertical sprite sheet*) con dimensiones considerables. En algunas versiones de herramientas basadas en Ruby como `zsteg`, el análisis exhaustivo de archivos de gran altura puede provocar errores de desbordamiento de pila (`SystemStackError`), resolviéndose mediante la inspección explícita de planos LSB (`zsteg -c b1,b,lsb,xy concat_v.png`).

## Referencias
- Reto: https://learn.cylabacademy.org/library/139
- Herramienta zsteg: https://github.com/zed-0xff/zsteg
