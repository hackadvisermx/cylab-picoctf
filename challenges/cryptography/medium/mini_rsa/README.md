# Mini RSA

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Origen:** picoCTF 2021
- **Puntos:** 70
- **URL:** https://play.picoctf.org/practice/challenge/188

---

## Descripción

> What happens if you have a small exponent? There is a twist though, we padded the plaintext so that (M ** e) is just barely larger than N. Let's decrypt this.

El reto provee un archivo `ciphertext.txt` con los parámetros RSA:

```
N: 1615765684321463054078226051959887884233678317734892901740764233542899248202070981
e: 3
ciphertext (c): 1220012318588871886132524757898884422174534558055593713309088304910273991073554670238274064519915816398019050055986358866325991821761198824205928048490398392900048611
```

---

## Hints oficiales

1. "RSA encodes messages as pow(m, e, N). What is pow(m, e) if m is just a bit smaller than N?"
2. "Make sure you are using Python3 and your number precision is sufficient (don't use floats)"
3. "Look at the wikipedia page for RSA. It has helpful information on how to solve this problem."

---

## Solución

### La vulnerabilidad: exponente público pequeño (e = 3)

En RSA estándar, el cifrado se define como:

```
c = m^e mod N
```

Cuando `e` es muy pequeño (como 3), se puede presentar una vulnerabilidad conocida como **ataque de raíz cúbica**. La idea básica: si `m` es suficientemente pequeño, entonces `m^e < N`, lo que significa que el módulo no tiene ningún efecto y el cifrado es simplemente:

```
c = m^e  (sin reducción modular)
```

En ese caso, simplemente se calcula la raíz e-ésima de `c` para recuperar `m`.

### El giro: padding que supera N

El reto agrega una complicación. El mensaje está acolchado (_padded_) de modo que `m^e` es **solo un poco mayor** que `N`. Esto significa que la reducción modular ocurrió exactamente una vez (o pocas veces), es decir:

```
c = m^e mod N  =>  m^e = k * N + c   (para k pequeño, k >= 1)
```

El ataque consiste en iterar sobre valores pequeños de `k` y verificar si `k * N + c` es un cubo perfecto:

1. Para `k = 0, 1, 2, ...`:
2. Calcular `candidato = k * N + c`
3. Intentar obtener la raíz cúbica exacta de `candidato`
4. Si la raíz es exacta, se encontró `m`

En este caso la solución se encuentra con `k = 1`.

### Herramienta: gmpy2

Se usa la librería `gmpy2` porque trabaja con enteros de precisión arbitraria y puede calcular raíces enteras exactas. **No usar aritmética de punto flotante** ya que pierde precisión con números tan grandes.

```bash
pip install gmpy2
```

---

## Script de descifrado

```python
import gmpy2

N = 1615765684321463054078226051959887884233678317734892901740764233542899248202070981
e = 3
c = 1220012318588871886132524757898884422174534558055593713309088304910273991073554670238274064519915816398019050055986358866325991821761198824205928048490398392900048611

# Iterar k desde 0 hasta encontrar la raíz cúbica exacta
for k in range(1000000):
    m_cubed = k * N + c
    m, exact = gmpy2.iroot(m_cubed, e)
    if exact:
        # Convertir el entero a bytes y decodificar como string
        m_hex = hex(m)[2:]
        if len(m_hex) % 2:
            m_hex = '0' + m_hex
        plaintext = bytes.fromhex(m_hex).decode('utf-8', errors='replace')
        print(f"k={k}: {plaintext}")
        break
```

La solución se encuentra en `k=1` y el plaintext decodificado contiene la flag en formato `picoCTF{...}`.

---

## Notas adicionales

### Por qué e = 3 es peligroso

RSA con `e = 3` (o cualquier `e` muy pequeño) es históricamente problemático. Los estándares modernos (PKCS#1, RFC 8017) recomiendan usar `e = 65537` (0x10001) como exponente público estándar. Este valor es suficientemente grande como para que `m^e` siempre supere con creces a `N`, pero sigue siendo eficiente de calcular con exponenciación binaria.

### Diferencia con el ataque clásico de raíz cúbica

El ataque **clásico** (sin padding o con padding pequeño) asume `m^e < N`, por lo que `c = m^e` exactamente y basta calcular `iroot(c, e)`. Este reto añade la variante del padding deliberado: el enunciado avisa que `m^e` es _apenas mayor_ que `N`, lo que obliga a iterar `k`. Esta es la "twist" (giro) que menciona la descripción oficial.

### Por qué no usar floats

Python's `float` usa doble precisión IEEE 754 de 64 bits, lo que da aproximadamente 15-17 dígitos decimales de precisión. Los números de este reto tienen más de 70 dígitos, por lo que cualquier raíz calculada con `float` sería incorrecta. La función `gmpy2.iroot()` opera sobre enteros de precisión arbitraria (respaldada por GMP) y garantiza el resultado exacto.

---

## Referencias

- Reto oficial: https://play.picoctf.org/practice/challenge/188
- Wikipedia RSA: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
- gmpy2 docs: https://gmpy2.readthedocs.io/
- Small public exponent attack: https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Attacks_against_plain_RSA
