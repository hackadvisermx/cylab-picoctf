# Cryptography — Mr-Worldwide

## Descripción

> **Prompt oficial del reto:** "A musician left us a message. What's it mean?"

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** speeeday/Danny

## Solución

El reto entrega un archivo `message.txt` con el formato:
```
academy{(35.028309, 135.753082)(46.469391, 30.740883)(39.758949, -84.191605)(41.015137, 28.979530)(24.466667, 54.366669)(3.140853, 101.693207)_(9.005401, 38.763611)(-3.989038, -79.203560)(52.377956, 4.897070)(41.085651, -73.858467)(57.790001, -152.407227)(31.205753, 29.924526)}
```

El título "Mr-Worldwide" hace referencia al apodo del cantante Pitbull (y a una famosa campaña viral en la que fue enviado a una tienda en Kodiak, Alaska). Cada par de coordenadas representa la latitud y longitud de una ciudad del mundo. Tomando la **primera letra** del nombre en inglés de cada ciudad se obtiene la palabra correspondiente:

### Primera palabra

1. `(35.028309, 135.753082)` → **K**yoto, Japón
2. `(46.469391, 30.740883)` → **O**desa, Ucrania
3. `(39.758949, -84.191605)` → **D**ayton, Ohio, EE. UU.
4. `(41.015137, 28.979530)` → **I**stanbul, Turquía
5. `(24.466667, 54.366669)` → **A**bu Dhabi, Emiratos Árabes Unidos
6. `(3.140853, 101.693207)` → **K**uala Lumpur, Malasia

Resultado: **`KODIAK`**

### Segunda palabra

7. `(9.005401, 38.763611)` → **A**ddis Ababa, Etiopía
8. `(-3.989038, -79.203560)` → **L**oja, Ecuador
9. `(52.377956, 4.897070)` → **A**msterdam, Países Bajos
10. `(41.085651, -73.858467)` → **S**leepy Hollow, Nueva York, EE. UU.
11. `(57.790001, -152.407227)` → **K**odiak, Alaska, EE. UU.
12. `(31.205753, 29.924526)` → **A**lexandria, Egipto

Resultado: **`ALASKA`**

Uniendo ambas partes con el guion bajo: `KODIAK_ALASKA`.

## Referencias

- [Geographic coordinate system — Wikipedia](https://en.wikipedia.org/wiki/Geographic_coordinate_system)
- [OpenStreetMap / Nominatim Reverse Geocoding](https://nominatim.openstreetmap.org/)
