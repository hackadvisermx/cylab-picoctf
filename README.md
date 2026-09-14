# CyLab picoCTF — Writeups

> Este repositorio es parte de **[sec-proy](https://github.com/hackadvisermx/sec-proy)**, un proyecto más amplio de soluciones a retos de ciberseguridad (CTFs, wargames y máquinas de hacking).

Writeups propios de retos de **CyLab Security Academy** ([learn.cylabacademy.org](https://learn.cylabacademy.org)), la plataforma de la Carnegie Mellon University que aloja el archivo histórico de **picoCTF** (2019–2026, picoMini, etc.) organizado en un "Challenge Library" por categoría y dificultad.

A diferencia de wargames con progresión estrictamente secuencial (Bandit, Natas), en CyLab cada reto es independiente: se navega por **categoría** (Web Exploitation, Cryptography, Reverse Engineering, Forensics, General Skills, Binary Exploitation, Blockchain, Artificial Intelligence) y **dificultad** (Easy / Medium / Hard).

> **Sobre las flags:** los writeups documentan la técnica usada para resolver cada reto, no las flags en sí. Las flags obtenidas se guardan solo localmente en `scripts/creds.txt` (excluido del repo vía `.gitignore`).

## Estado actual

| Categoría | Dificultad | Progreso |
|---|---|---|
| General Skills | Easy | ✅ 48/48 resueltos y documentados |
| General Skills | Medium | ✅ 8/8 resueltos y documentados (los que estaban pendientes en esta cuenta) |
| Web Exploitation | Easy | ✅ 20/20 resueltos y documentados |
| Web Exploitation | Medium | ✅ 16/16 resueltos y documentados |
| Cryptography | — | ⏳ sin empezar |
| Reverse Engineering | — | ⏳ sin empezar |
| Forensics | — | ⏳ sin empezar |
| Binary Exploitation | — | ⏳ sin empezar |
| Blockchain | — | ⏳ sin empezar |
| Artificial Intelligence | — | ⏳ sin empezar |

El detalle reto por reto, en el orden en que aparecen en la plataforma, está en **[PROGRESS.md](PROGRESS.md)**.

## Estructura del repositorio

```
.
├── PROGRESS.md                    # Tracking detallado: tablas por categoría/dificultad, fases y notas de progreso
└── challenges/
    ├── _template/
    │   └── README.md               # Plantilla base para cada writeup nuevo
    ├── general-skills/
    │   ├── easy/                   # 48 writeups (uno por reto, en su propia carpeta)
    │   │   └── <slug>/README.md
    │   └── medium/                 # 8 writeups
    │       └── <slug>/README.md
    └── web-exploitation/
        ├── easy/                   # 20 writeups (100%)
        │   └── <slug>/README.md
        └── medium/                 # 16/16 writeups (100%)
            └── <slug>/README.md
```

Cada writeup vive en su propia carpeta (`challenges/<categoría>/<dificultad>/<slug>/README.md`) y sigue la plantilla de [`challenges/_template/README.md`](challenges/_template/README.md): descripción oficial del reto, categoría/dificultad/evento/autor, solución paso a paso con los comandos usados, notas adicionales y referencias. Algunas carpetas incluyen también archivos de apoyo descargados del reto (código fuente, logs, binarios de análisis, reglas YARA, etc.) cuando son relevantes para seguir la solución.

## Metodología

- **Terminal local primero:** siempre que un reto se resuelve por `nc`/`ssh`/sockets, se prioriza conectar desde la terminal local en vez de depender del webshell embebido de la plataforma (que ha mostrado inestabilidad — pestañas colgadas, reconexiones fallidas — en sesiones largas o con `nc` intensivo).
- **Sin apurar instancias:** las instancias de reto son efímeras (~15–30 min); si el webshell se traba, se reintenta una vez de forma directa o se pasa al siguiente reto en vez de perder tiempo esperando.
- Un reto por carpeta, con su propio writeup — nada de flags sueltas en el historial de git.

## Próximos pasos

Con General Skills, Web Exploitation Easy y Web Exploitation Medium al 100%, sigue el resto de categorías: Cryptography, Reverse Engineering, Forensics, Binary Exploitation, Blockchain, Artificial Intelligence (y Web Exploitation Hard). Ver la sección "Fases del proyecto" en [PROGRESS.md](PROGRESS.md) para el detalle completo.

## Aviso

Este material es para uso educativo propio sobre retos públicos (picoCTF, vía CyLab Security Academy) que autorizan explícitamente su resolución. Evita publicar las flags fuera de un contexto de práctica personal como este.
