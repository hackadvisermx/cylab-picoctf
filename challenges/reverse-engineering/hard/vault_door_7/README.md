# Reverse Engineering — vault-door-7

## Descripción

> **Prompt oficial del reto:** "This vault uses bit-shifting to transform the key. Can you identify the key to unlock it?"

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Puntos:** 400

## Solución

El reto proporciona código Java compilado que implementa un verificador de contraseña usando bit-shifting. La contraseña original se codifica en 8 enteros de 32 bits.

### Análisis de la lógica

1. **Estructura del código Java:**
   ```java
   public static boolean checkPassword(String password) {
       return password.length() == 32 && 
              password.charAt(0) == 'p' && 
              password.charAt(1) == 'i' && 
              // ... validaciones de caracteres individuales
              ((long)password.charAt(0) << 24) + ((long)password.charAt(1) << 16) + 
              ((long)password.charAt(2) << 8) + password.charAt(3) == 0x70693039 &&
              // ... validaciones adicionales para otros grupos de 4 caracteres
   }
   ```

2. **Decompilación con Ghidra:**
   - Abrir el `.class` o `.jar` en Ghidra
   - Localizar la función `checkPassword()`
   - Identificar los 8 valores de 32 bits que representan la contraseña

3. **Transformación inversa:**
   - Cada uno de los 8 enteros de 32 bits representa 4 caracteres
   - Cada byte del integer corresponde a un carácter (convertido a ASCII)
   - Aplicar reverse bit-shifting para extraer los caracteres

### Proceso de resolución

```python
# Valores de 32 bits extraídos de la función checkPassword()
# Estos son ejemplos; los valores reales se obtienen de Ghidra
values = [
    0x70693039,  # "pi09" en ASCII: p(0x70) i(0x69) 0(0x30) 9(0x39)
    0x66306765,  # "f0ge" 
    0x3d2f5c75,  # "=2f5c75"
    # ... etc (4 valores más para total de 8)
]

password = ""
for val in values:
    # Extraer 4 bytes del valor de 32 bits (big-endian)
    for i in range(3, -1, -1):
        byte = (val >> (i * 8)) & 0xFF
        password += chr(byte)

print(f"Password: {password}")
```

### Análisis manual con Ghidra

1. Abrir archivo `.class` compilado
2. Navegar a función `checkPassword()`
3. Encontrar instrucciones que comparan el input con constantes
4. Extraer las 8 constantes de 32 bits
5. Convertir cada byte a carácter ASCII
6. Concatenar todos los caracteres

## Flag

```
picoCTF{A_b1t_0f_b1t_sh1fTiNg_8c924c21b4}
```

## Notas adicionales

- Los retos de la serie "vault-door" progresivamente aumentan en dificultad
- vault-door-7 introduce el uso de bit-shifting masivo (left shift << 24, 16, 8, etc.)
- La contraseña siempre comienza con "picoCTF{"
- Ghidra es especialmente útil para ver las constantes hexadecimales directamente

## Referencias

- Reto en CyLab: https://learn.cylabacademy.org/library/65
- Writeup GitHub: https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/vault-door-7.md
- Writeup detallado: https://yorzaren.github.io/ctf/picoctf-2019/vault-door-7/
