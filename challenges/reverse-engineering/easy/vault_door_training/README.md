# Reverse Engineering — vault-door-training

## Descripción
> **Prompt oficial del reto:** "Your mission is to enter Dr. Evil's laboratory and retrieve the blueprints for his Doomsday Project. The laboratory is protected by a series of locked vault doors. Each door is controlled by a computer and requires a password to open. Unfortunately, our undercover agents have not been able to obtain the secret passwords for the vault doors, but one of our junior agents obtained the source code for each vault's computer! You will need to read the source code for each level to figure out what the password is for that vault door. As a warmup, we have created a replica vault in our training facility.  
> 
> The source code for the training vault is here: [VaultDoorTraining.java](https://challenge-files.cylabacademy.net/library/83cea9a75c072b1b2dff071720061929c5a4e9817a86613e1c51ebc0540cbc73/VaultDoorTraining.java)"

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2019
- **Autor:** Mark E. Haase

## Solución
El reto proporciona el código fuente en Java de la primera puerta de la serie "vault-door" (`VaultDoorTraining.java`).

### Análisis del código fuente

Al examinar el archivo:

```java
import java.util.*;

class VaultDoorTraining {
    public static void main(String args[]) {
        VaultDoorTraining vaultDoor = new VaultDoorTraining();
        Scanner scanner = new Scanner(System.in); 
        System.out.print("Enter vault password: ");
        String userInput = scanner.next();
	String input = userInput.substring("academy{".length(),userInput.length()-1);
	if (vaultDoor.checkPassword(input)) {
	    System.out.println("Access granted.");
	} else {
	    System.out.println("Access denied!");
	}
   }

    // The password is below. Is it safe to put the password in the source code?
    // What if somebody stole our source code? Then they would know what our
    // password is. Hmm... I will think of some ways to improve the security
    // on the other doors.
    //
    // -Minion #9567
    public boolean checkPassword(String password) {
        return password.equals("w4rm1ng_Up_w1tH_jAv4_4cfa5369b93");
    }
}
```

1. **Extracción del payload:** En `main`, el programa toma la entrada del usuario y extrae la subcadena interna descartando el prefijo `academy{` y la llave de cierre `}`:
   ```java
   String input = userInput.substring("academy{".length(), userInput.length()-1);
   ```
2. **Comprobación:** La función `checkPassword` compara directamente dicha subcadena con un literal embebido en el código:
   ```java
   return password.equals("w4rm1ng_Up_w1tH_jAv4_4cfa5369b93");
   ```
3. **Reconstrucción:** Concatenando el prefijo y sufijo estándar de bandera con el contenido comparado, se obtiene la bandera válida.

### Comandos de inspección

```bash
# Lectura e inspección del método de validación
cat VaultDoorTraining.java | grep -A 5 "checkPassword"

# Prueba interactiva compilando y ejecutando (opcional)
javac VaultDoorTraining.java
java VaultDoorTraining
# Ingresar: academy{...}
# Resultado: Access granted.
```

La flag final tiene la estructura `academy{...}`.

## Notas adicionales
- Este reto inicial ejemplifica la vulnerabilidad de almacenar secretos o contraseñas en texto plano (*hardcoded credentials*) dentro del código fuente de una aplicación cliente. En ingeniería inversa, la inspección estática del código decompilado o desensamblado es la primera vía para localizar estas constantes.

## Referencias
- Reto: https://learn.cylabacademy.org/library/7
- CWE-798: Use of Hard-coded Credentials: https://cwe.mitre.org/data/definitions/798.html
