# Reverse Engineering — Pico Bank

## Descripción
> **Prompt oficial del reto:** "In a bustling city where innovation meets finance, Pico Bank has emerged as a beacon of cutting-edge security. Promising state-of-the-art protection for your assets, the bank claims its mobile application is impervious to all forms of cyber threats. Pico Bank’s tagline, "Security Beyond the Limits," echoes through its high-tech marketing campaigns, assuring users of their utmost safety.
>
> As a cybersecurity enthusiast, your mission is to test these bold claims. You’ve been hired by a secretive organization to put Pico Bank’s mobile app through a rigorous security assessment. The flag might be in one or more locations, and additional information reveals that a Pico Bank user’s credentials were leaked in an unusual way. Your task is to crack the username and password based on the following profile information: His name is Alex Johnson with the email johnson@picobank.com, Date of Birth: March 14, 1990, Last Transaction Amount: $345.67, Pet name: tricky, and Favorite Color: Blue.
>
> To perform this challenge, you can use any Android emulator. Some examples include [Genymotion Android Emulator](https://www.genymotion.com/product-desktop/download/) or [Android Studio](https://developer.android.com/studio).
> Access the Pico Bank Website and download the application."
>
> **Pistas oficiales:**
> 1. Use tools like JadxGUI or apktool to inspect the APK.
> 2. Look at the app's network requests, especially for login and OTP.
> 3. The flag has two parts.
> 4. Check the server’s response after entering the correct OTP.
> 5. Investigate the transaction history for unusual data.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoMini by CMU-Africa
- **Autor:** Prince Niyonshuti N.

## Solución
El reto involucra una aplicación móvil Android (`pico-bank.apk`) descargada desde el servidor web de la instancia on-demand (`http://<host>:<puerto>/download/pico-bank.apk`). La bandera está dividida en dos fragmentos independientes.

### 1. Extracción del APK y credenciales
Descomprimiendo el APK (`unzip pico-bank.apk -d apk_extracted/`) o descompilándolo con `jadx`:
- En la clase `Login` se encuentran las credenciales codificadas:
  - **Username:** `johnson`
  - **Password:** `tricky1990` (combinación del nombre de la mascota y el año de nacimiento dados en la descripción).

### 2. Parte 1 de la bandera: Historial de transacciones
Al inspeccionar `MainActivity`, los montos de las transacciones bancarias están formateados como cadenas binarias precedidas por `$ `:
```python
transactions = [
    "1110000", "1101001", "1100011", "1101111", "1000011", "1010100", "1000110", "1111011",
    "110001", "1011111", "1101100", "110001", "110011", "1100100", "1011111", "110100",
    "1100010", "110000", "1110101", "1110100", "1011111", "1100010", "110011", "110001",
    "1101110", "1100111", "1011111"
]
part1 = ''.join(chr(int(b, 2)) for b in transactions)
print(part1)  # academy{1_l13d_4b0ut_b31ng_
```
La primera parte corresponde a: `academy{1_l13d_4b0ut_b31ng_`.

### 3. Parte 2 de la bandera: Endpoint de OTP
En la clase `OTP`, el código define un valor de código único (OTP) estático `9673` y realiza una petición POST hacia el endpoint `/verify-otp`. Interactuando directamente con el servidor de la instancia mediante `curl`:

```bash
curl -X POST http://<host>:<puerto>/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"otp":"9673"}'
```

Respuesta del servidor:
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "flag": "s3cur3d_m0b1l3_l0g1n_...}",
  "hint": "The other part of the flag is hidden in the app"
}
```

### 4. Bandera completa
Concatenando la primera mitad extraída de las transacciones con la segunda mitad obtenida del servidor OTP:
```text
academy{...}
```

## Notas adicionales
- El reto demuestra dos malas prácticas comunes en el desarrollo móvil:
  1. Ofuscación superficial de datos confidenciales en interfaces de usuario mediante representaciones binarias triviales.
  2. Implementación insegura de autenticación multifactor (MFA/OTP) donde el valor del OTP se encuentra fijado en el cliente y validado de forma estática en la API.

## Referencias
- Reto: https://learn.cylabacademy.org/library/529
- JADX Decompiler: https://github.com/skylot/jadx
