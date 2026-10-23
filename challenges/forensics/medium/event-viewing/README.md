# Forensics — Event-Viewing

## Descripción
> **Prompt oficial del reto:** "One of the employees at your company has their computer infected by malware! Turns out every time they try to switch on the computer, it shuts down right after they log in. The story given by the employee is as follows:  
> 1. They installed software using an installer they downloaded online  
> 2. They ran the installed software but it seemed to do nothing  
> 3. Now every time they bootup and login to their computer, a black command prompt screen quickly opens and closes and their computer shuts down instantly.  
>  
> See if you can find evidence for the each of these events and retrieve the flag (split into 3 pieces) from the correct logs!  
>  
> Download the Windows Log file here"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** Venax

> **Pistas oficiales:**
> 1. Try to filter the logs with the right event ID
> 2. What could the software have done when it was ran that causes the shutdowns every time the system starts up?

## Solución
El reto provee un archivo de registro de eventos de Windows (`Windows_Logs.evtx`). La bandera se encuentra dividida en 3 fragmentos codificados en Base64, cada uno correspondiente a un paso de la secuencia reportada por el usuario.

1. **Paso 1: Instalación del software (Event ID 1033 - MsiInstaller):**
   Filtramos los eventos de instalación de paquetes MSI (`MsiInstaller`). En el registro correspondiente a la instalación de `Totally_Legit_Software.msi` (Registro 75, Event ID 1033):
   ```xml
   <EventData>
     <Data>Totally_Legit_Software</Data>
     <Data>1.3.3.7</Data>
     <Data>0</Data>
     <Data>0</Data>
     <Data>YWNhZGVteXtFdjNudF92aTN3djNyXw==</Data>
   </EventData>
   ```
   Decodificando `YWNhZGVteXtFdjNudF92aTN3djNyXw==`:
   `academy{Ev3nt_vi3wv3r_` (Parte 1).

2. **Paso 2: Persistencia tras la ejecución (Event ID 4657 - Registry Modification):**
   Al ejecutarse el malware, este creó una clave de persistencia en el registro de Windows para ejecutarse al inicio de sesión del usuario (`HKLM\Software\Microsoft\Windows\CurrentVersion\Run`). En el Registro 186 (Event ID 4657, Security Auditing):
   ```xml
   <Data Name="ObjectName">\REGISTRY\MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run</Data>
   <Data Name="ObjectValueName">Immediate Shutdown (MXNfYV9wcjN0dHlfdXMzZnVsXw==)</Data>
   <Data Name="NewValue">C:\Program Files (x86)\Totally_Legit_Software\custom_shutdown.exe</Data>
   ```
   Decodificando `MXNfYV9wcjN0dHlfdXMzZnVsXw==`:
   `1s_a_pr3tty_us3ful_` (Parte 2).

3. **Paso 3: Apagado del sistema al iniciar sesión (Event ID 1074 - User32 Shutdown):**
   Al ejecutarse el binario `custom_shutdown.exe` / `shutdown.exe`, se registra el motivo de apagado en los registros del sistema (Registro 5575, Event ID 1074, User32):
   ```xml
   <Data Name="param1">C:\Windows\system32\shutdown.exe</Data>
   <Data Name="param5">shutdown</Data>
   <Data Name="param6">dDAwbF84MWJhM2ZlOX0=</Data>
   ```
   Decodificando `dDAwbF84MWJhM2ZlOX0=`:
   `t0ol_81ba3fe9}` (Parte 3).

4. **Reconstrucción de la bandera:**
   Concatenando las 3 partes obtenidas:
   Parte 1 + Parte 2 + Parte 3 = Bandera completa de la academia.

```python
import base64

p1 = base64.b64decode("YWNhZGVteXtFdjNudF92aTN3djNyXw==").decode()
p2 = base64.b64decode("MXNfYV9wcjN0dHlfdXMzZnVsXw==").decode()
p3 = base64.b64decode("dDAwbF84MWJhM2ZlOX0=").decode()

print(p1 + p2 + p3)
```

## Notas adicionales
- El análisis forense de registros EVTX en Windows permite rastrear la cadena de infección completa (*kill chain*): vector de entrega/instalación (ID 1033), persistencia en registro (ID 4657) e impacto en el sistema (ID 1074).
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/456
- Microsoft Security Auditing (Event 4657): https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4657
- Microsoft User32 Shutdown (Event 1074): https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/event-id-1074-logged-when-system-shuts-down
