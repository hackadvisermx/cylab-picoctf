# Reverse Engineering — crackme-py

## Descripción
> **Prompt oficial del reto:** "[crackme_gen.py](https://challenge-files.cylabacademy.net/library/bb1b40a7f19667aef0011b9d5d28b8379f06edb9244e75fd9cab306f3f1a3a16/crackme_gen.py)"
>
> **Pistas oficiales:** Ninguna

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
El reto consiste en un script de Python (`crackme_gen.py`). Al abrirlo y analizar su código fuente, encontramos la definición de varias funciones:

1. `choose_greatest()`: Función principal que solicita dos números por teclado e imprime cuál es el de mayor magnitud positiva.
2. `bezos_cc_secret`: Variable que almacena una cadena ofuscada:
   ```python
   bezos_cc_secret = "24256>JL`>0c0Abc?FE02a_53e7fe7af5gN"
   ```
3. `decode_secret(secret)`: Una función implementada pero que **nunca es llamada** durante el flujo de ejecución normal del script. La función rota los caracteres a través de una tabla de 94 caracteres imprimibles (`alphabet`) con un desplazamiento constante de 47 posiciones, lo cual corresponde al algoritmo **ROT47**:
   ```python
   def decode_secret(secret):
       rotate_const = 47
       decoded = ""
       for c in secret:
           index = alphabet.find(c)
           original_index = (index + rotate_const) % len(alphabet)
           decoded = decoded + alphabet[original_index]
       print(decoded)
   ```

### Ejecución de la rutina oculta

Para resolver el reto, basta con modificar el final del archivo o invocar la función `decode_secret` pasando como argumento `bezos_cc_secret`:

```bash
python3 -c '
import crackme_gen
crackme_gen.decode_secret(crackme_gen.bezos_cc_secret)
'
```

O editando el archivo para añadir al final:
```python
decode_secret(bezos_cc_secret)
```

Al ejecutarse, la función decodifica la cadena y muestra la bandera en formato `academy{...}`.

## Notas adicionales
En retos de ingeniería inversa en lenguajes interpretados como Python, buscar funciones huérfanas o no referenciadas (*dead/unreachable code*) a menudo revela funcionalidades críticas o rutinas de prueba dejadas por los desarrolladores.

## Referencias
- Reto: https://learn.cylabacademy.org/library/175
- Apoyo: https://en.wikipedia.org/wiki/ROT47
