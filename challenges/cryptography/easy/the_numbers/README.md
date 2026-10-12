# Cryptography — The Numbers

## Descripción
> **Prompt oficial del reto:** "The numbers... what do they mean? `numbers`" (se entrega una imagen `the_numbers.png`).
>
> **Hints:**
> 1. The flag is in the format PICOCTF{}

- **Categoría:** Cryptography
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny

## Solución
La imagen muestra una secuencia de números: `16 9 3 15 3 20 6 { 20 8 5 14 21 13 2 5 18 19 13 1 19 15 14 }`. Es el cifrado **A1Z26** (cada número = posición de la letra en el alfabeto, A=1 ... Z=26):

```
16=P 9=I 3=C 15=O 3=C 20=T 6=F  -> PICOCTF
20=T 8=H 5=E  14=N 21=U 13=M 2=B 5=E 18=R 19=S  13=M 1=A 19=S 15=O 14=N
-> THE NUMBERS MASON
```

Flag: `PICOCTF{THENUMBERSMASON}`.

## Notas adicionales
- A1Z26 es uno de los cifrados de sustitución más básicos; la pista del formato `PICOCTF{}` confirma que el contenido decodificado ya es la flag (no hay prefijo `academy{}` aquí).

## Referencias
- Reto: https://learn.cylabacademy.org/library/68
