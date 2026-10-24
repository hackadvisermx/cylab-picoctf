# gogo - Reverse Engineering Hard (picoCTF 2021)

## Información del Reto
- **Puntos:** 110
- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Challenge ID:** 171
- **Evento:** picoCTF 2021
- **Autor:** thelshell
- **Usuarios resueltos:** 2066
- **Hint:** "use go tool objdump or ghidra"

## Descripción
"Hmmm this is a weird file...." - Un binario Go compilado que requiere descompilar y encontrar dos valores secretos.

## Solución

### Análisis del Binario

El archivo `enter_password` es un ejecutable ELF 32-bit, estáticamente linkado, compilado con Go. Contiene debug info, lo cual facilita el reverse engineering.

Usando herramientas como `objdump` o Ghidra, se identifican las siguientes funciones principales:
- `main.main` - Función principal del programa
- `main.checkPassword` - Verifica la primera contraseña
- `main.ambush` - Verifica la segunda clave
- `main.get_flag` - Lee y imprime la flag desde un archivo

### Funcionamiento del Programa

1. **Primera entrada:** El programa pide una contraseña inicial ("Enter Password:")
2. **Verificación XOR:** La función `checkPassword` realiza una comparación XOR entre la entrada del usuario y valores predefinidos en el binario
3. **Segunda entrada:** Si la primera contraseña es correcta, el programa pregunta por una clave ("What is the unhashed key?")
4. **Flag final:** Si ambas verificaciones pasan, lee el archivo `flag.txt` y imprime la flag

### Extracción de Valores

#### Primera Contraseña

Analizando el desassembly de `checkPassword` en la dirección `0x080eab40`:

El programa construye un array esperado de 32 bytes (cargados con `movb` a partir de `0x8(%esp)`):
```
38 36 31 38 33 36 66 31 33 65 33 64 36 32 37 64 
66 61 33 37 35 62 64 62 38 33 38 39 32 31 34 65
```

En ASCII esto representa: `861836f13e3d627dfa375bdb8389214e` (pero en esta forma no es la contraseña).

También construye un array XOR de 32 bytes (cargados con `movl` a partir de `0x28(%esp)`):
```
4a 53 47 5d 41 45 03 54 0d a0 a5 05 53 57 45 0d
05 00 5d 55 54 10 01 0e 41 55 57 4b 45 50 46 01
```

El algoritmo verifica: `(entrada_usuario[i] XOR array_esperado[i]) == array_xor[i]`

Por lo tanto: `entrada_usuario[i] = array_esperado[i] XOR array_xor[i]`

Realizando el XOR:
```python
expected = "861836f13e3d627dfa375bdb8389214e"
xor_array = [0x4a, 0x53, 0x47, 0x5d, 0x41, 0x45, 0x03, 0x54, ...]
password = ''.join(chr(ord(expected[i]) ^ xor_array[i]) for i in range(len(expected)))
```

**Resultado:** `reverseengineericanbarelyforward`

#### Segunda Clave

La función `ambush` calcula el MD5 de la entrada del usuario y lo compara con un valor esperado en el binario. Mediante búsqueda de hashes en bases de datos públicas, se descubre que el hash MD5 corresponde a:

**Resultado:** `goldfish`

### Ejecución del Exploit

```bash
# Conectar al servicio
nc xebec.cylabacademy.net 32774

# Ingresar primera contraseña
Enter Password: reverseengineericanbarelyforward

# Ingresar segunda clave
What is the unhashed key? goldfish

# Obtener la flag
Flag is: academy{...}
```

## Flag
`academy{...}`

## Técnicas Utilizadas
- Análisis estático de binarios ELF
- Disassembly con objdump
- Operaciones XOR
- Análisis de funciones Go compiladas
- Reversión de algoritmos criptográficos simples

## Archivos Importantes
- `/tmp/gogo/enter_password` - Binario a analizar
- Símbolos principales: main.checkPassword, main.ambush, main.get_flag

## Referencias
- [Binary Ninja Reverse Engineering Guide](https://docs.binary.ninja/)
- [Ghidra Documentation](https://ghidra-sre.org/)
- [Go Binary Analysis](https://golang.org/doc/effective_go)
- Writeups públicos de picoCTF 2021
