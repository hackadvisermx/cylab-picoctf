# Características de la plataforma CyLab Security Academy (para réplica futura)

Notas técnicas sobre `learn.cylabacademy.org`, recopiladas mientras se resuelven retos, con vistas a poder replicar en un futuro un entorno local equivalente (contenedores/CTFd) para práctica sin depender de la plataforma en línea.

## Qué es
- Portal de entrenamiento ("CyLab Security Academy") con un **Challenge Library** que incluye el archivo histórico de **picoCTF** (picoCTF 2024, 2025, 2026, picoMini by CMU-Africa, etc.) más retos propios (p. ej. serie "Perceptron"/"Neuron" de IA, "AI Foundations I").
- Navegación: `https://learn.cylabacademy.org/library?page=N`, con filtros por `category`, `difficulty` y `event` reflejados en la query string (p. ej. `?page=1&category=1`).
- Categorías observadas: Web Exploitation, Cryptography, Reverse Engineering, Forensics, General Skills, Binary Exploitation, Blockchain, Artificial Intelligence.
- Cada tarjeta de reto muestra: nombre, autor, categoría, dificultad (Easy/Medium/Hard con barras de "señal"), evento de origen, % de resolución y nº de resuelves.
- Existe un botón "Open Workspace" (entorno de trabajo integrado, pendiente de explorar) y un "Progress Tracker" desplegable en la parte superior de la librería.

## Acceso / autenticación
- Requiere cuenta de usuario (sesión ya iniciada en esta sesión de trabajo). Pendiente documentar el flujo de login/registro si hace falta reproducirlo.

## Mecánica de los retos (confirmado, primera sesión)
- Cada reto se abre en un modal/"Workspace" con: descripción, botón **Launch Instance** (levanta un contenedor efímero, con temporizador de expiración ~30 min y botón "Restart Instance"), lista de **Hints** (ocultos hasta pulsar "Reveal hint", probablemente con coste de puntos), y campo **Flag** con botón Submit que valida en el momento ("Correct flag!" / error), sin necesidad de plataforma externa tipo CTFd.
- El **Workspace** (botón "Open Workspace" o "Open in Workspace") añade un panel lateral con pestañas: **Terminal** (webshell), **CyberChef** (herramienta de codificación/decodificación embebida) y **CTF Primer** (guía para principiantes). Muy útil: no hace falta terminal local para nada de esto.
- **El Terminal es un webshell compartido y persistente** (usuario `castr-academy@webshell`, con `~` persistente entre sesiones según el MOTD, aunque el resto del sistema de archivos no persiste). Ojo: el `$HOME` puede contener **restos de retos anteriores** resueltos por la cuenta (se vieron archivos sueltos tipo `serpentine.py`, `ltdis.x86_64.txt` de otros challenges) — no asumir que un archivo en `~` pertenece al reto actual.
- Para retos de **red/servicio** (típico picoCTF: pwn, algunos General Skills), la descripción muestra un enlace **Source** (código fuente, cuando aplica) y una línea `Connect with nc <host>.picoctf.net <puerto>` — el propio webshell tiene `nc` disponible y conectividad de red saliente (con límites, ver `usage`), así que no hace falta abrir un terminal local.
- **El estado del reto vive en el proceso del servicio, no en el contenedor completo**: para "resetear" un servicio de red al que se le rompió el estado (p. ej. una variable quedó en un valor inútil), basta **reconectar con una nueva sesión `nc`** (cada conexión = proceso nuevo del lado del servidor) — no hace falta pulsar "Restart Instance" salvo que la propia instancia (puerto/host) haya dejado de responder. "Restart Instance" sí cambia el puerto asignado (visto: 58701 → 60455) y tarda unos 10-20s en volver a quedar "RUNNING".
- Cada instancia lanzada aparece como una tarjeta flotante en la esquina inferior derecha (nombre, cronómetro de expiración, botón de recargar/reiniciar y botón de detener) — se pueden tener varias instancias corriendo a la vez (una por reto abierto), conviene **detener las que no se usan** para no acumular contenedores.
- Formato de flag confirmado: `picoCTF{...}` (idéntico al picoCTF original), validado en la propia página (no hace falta un portal externo).
- **La cuenta usada arrastra progreso previo**: muchos retos ya aparecen como "Solved by you" antes de tocarlos en esta sesión. El filtro **"Hide Solved"** en la Challenge Library es la forma correcta de encontrar qué falta por hacer en cada categoría/dificultad.

## Herramientas usadas para automatizar
(se irá completando: curl, nc, python, pwntools, etc. según se necesiten)

## Lecciones de automatización con navegador (esta sesión)
- Los retos con **instancia SSH activa** embebida en el Workspace (p. ej. `SansAlpha`, categoría con tag `ssh`) pueden dejar la pestaña del navegador en un estado donde `screenshot`/`get_page_text`/`read_page` fallan repetidamente con timeout ("Page still loading" / "Script injection timed out"), aparentemente porque el terminal usa un WebSocket de larga duración que el navegador interpreta como "página aún cargando". **Solución que funcionó**: cerrar esa pestaña y abrir una nueva (`tabs_close_mcp` + `navigate`), en vez de insistir esperando o navegando en la misma pestaña.
- El editor online de Rockstar (https://codewithrockstar.com/online, basado en un editor tipo CodeMirror) puede **perder la mayoría de las pulsaciones** al automatizar `type` con textos multilínea largos (probablemente por un manejo especial de teclado/autocompletado del editor) — para programas Rockstar cortos y sencillos funcionó bien, pero para depurar cambios pequeños es más fiable **ejecutar el intérprete de referencia localmente en Node** (repo `RockstarLang/rockstar`, carpeta `satriani/`) que lidiar con la automatización del editor web.

## Ideas para la réplica local (fase futura)
- Dado que gran parte del contenido es picoCTF, una alternativa más simple que replicar CyLab Academy completo es usar el propio repositorio open-source de picoCTF (`picoCTF/picoCTF` en GitHub) con CTFd o el "picoCTF-web" original para levantar una copia local de los retos ya resueltos.
- Documentar aquí, reto a reto, qué necesitaría un contenedor local (lenguaje del servicio, puertos, dependencias) para los retos que si sean específicos de CyLab (no picoCTF) como la serie Perceptron/Neuron de IA.
