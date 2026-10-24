# Reverse Engineering — Safe Opener

## Descripción
> **Prompt oficial del reto:** "Can you open this safe? I forgot the key to my safe but this program is supposed to help me with retrieving the lost key. Can you help me unlock my safe? Put the password you recover into the academy flag format like: `academy{password}`"
>
> **Pistas oficiales:**
> (Ninguna pista proporcionada en la plataforma)

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** Mubarak Mikail

## Solución
El reto provee el código fuente en Java de la aplicación (`SafeOpener.java`).

### 1. Análisis del código fuente
Al abrir y examinar el archivo:

```java
public class SafeOpener {
    public static void main(String args[]) throws IOException {
        ...
        encodedkey = encoder.encodeToString(key.getBytes());
        isOpen = openSafe(encodedkey);
        ...
    }
    
    public static boolean openSafe(String password) {
        String encodedkey = "cGwzYXMzX2wzdF9tM18xbnQwX3RoM19zYWYz";
        
        if (password.equals(encodedkey)) {
            System.out.println("Sesame open");
            return true;
        }
        ...
    }
}
```

El programa lee una contraseña introducida por el usuario, la codifica en **Base64** con `encoder.encodeToString()`, y la compara contra la cadena estática `cGwzYXMzX2wzdF9tM18xbnQwX3RoM19zYWYz`.

### 2. Decodificación de la contraseña
Para obtener la contraseña en texto claro, se decodifica la cadena Base64:

```bash
echo "cGwzYXMzX2wzdF9tM18xbnQwX3RoM19zYWYz" | base64 -d
```

Salida:
```text
pl3as3_l3t_m3_1nt0_th3_saf3
```

Siguiendo las instrucciones del reto, se envuelve la contraseña en el formato de bandera: `academy{...}`.

## Notas adicionales
- Base64 es un esquema de codificación y transporte de datos binarios, no un mecanismo de cifrado o hashing seguro.

## Referencias
- Reto: https://learn.cylabacademy.org/library/294
- RFC 4648 Base64 Encoding: https://datatracker.ietf.org/doc/html/rfc4648
