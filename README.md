# CyLab picoCTF — Writeups

> Este repositorio es parte de **[sec-proy](https://github.com/hackadvisermx/sec-proy)**, un proyecto más amplio de soluciones a retos de ciberseguridad (CTFs, wargames y máquinas de hacking).

Writeups propios de retos de **CyLab Security Academy** ([learn.cylabacademy.org](https://learn.cylabacademy.org)), la plataforma de la Carnegie Mellon University que aloja el archivo histórico de **picoCTF** (2019–2026, picoMini, etc.) organizado en un "Challenge Library" por categoría y dificultad.

A diferencia de wargames con progresión estrictamente secuencial (Bandit, Natas), en CyLab cada reto es independiente: se navega por **categoría** (Web Exploitation, Cryptography, Reverse Engineering, Forensics, General Skills, Binary Exploitation, Blockchain, Artificial Intelligence) y **dificultad** (Easy / Medium / Hard).

> **Sobre las flags:** los writeups documentan la técnica usada para resolver cada reto, no las flags en sí. Las flags obtenidas se guardan solo localmente en `scripts/creds.txt` (excluido del repo vía `.gitignore`).

## Estado actual

| Categoría | Dificultad | Progreso |
|---|---|---|
| General Skills | Easy | ✅ 48/48 resueltos y documentados (100%) |
| General Skills | Medium | ✅ 25/25 resueltos y documentados (100%) |
| General Skills | Hard | ✅ 2/2 resueltos y documentados (100%) |
| Web Exploitation | Easy | ✅ 20/20 resueltos y documentados (100%) |
| Web Exploitation | Medium | ✅ 47/47 resueltos y documentados (100%) |
| Web Exploitation | Hard | ⏳ 12/16 resueltos y documentados |
| Forensics | Easy | ✅ 15/15 resueltos y documentados (100%) |
| Forensics | Medium | ✅ 54/54 resueltos y documentados (100%) |
| Cryptography | Easy | ✅ 8/8 resueltos y documentados (100%) |
| Cryptography | Medium | ✅ 45/45 resueltos y documentados (100%) |
| Reverse Engineering | Easy | ✅ 14/14 resueltos y documentados (100%) |
| Reverse Engineering | Medium | ⏳ 20/53 resueltos y documentados (38%) |
| Binary Exploitation | Easy | ✅ 5/5 resueltos y documentados (100%) |
| Binary Exploitation | Medium | ⏳ 0/37 resueltos y documentados |
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
    │   ├── easy/                   # 48 writeups (100%)
    │   ├── medium/                 # 25 writeups (100%)
    │   └── hard/                   # 2 writeups (100%)
    ├── web-exploitation/
    │   ├── easy/                   # 20 writeups (100%)
    │   ├── medium/                 # 47 writeups (100%)
    │   └── hard/                   # 12 writeups
    ├── forensics/
    │   ├── easy/                   # 15 writeups (100%)
    │   └── medium/                 # 54 writeups (100%)
    ├── cryptography/
        ├── easy/                   # 8 writeups (100%)
        └── medium/                 # 45 writeups (100%)
    ├── reverse-engineering/
    │   ├── easy/                   # 14 writeups (100%)
    │   └── medium/                 # 20 writeups (38%)
    └── binary-exploitation/
        └── easy/                   # 5 writeups (100%)
```

Cada writeup vive en su propia carpeta (`challenges/<categoría>/<dificultad>/<slug>/README.md`) y sigue la plantilla de [`challenges/_template/README.md`](challenges/_template/README.md): descripción oficial del reto, categoría/dificultad/evento/autor, solución paso a paso con los comandos usados, notas adicionales y referencias. Algunas carpetas incluyen también archivos de apoyo descargados del reto (código fuente, logs, binarios de análisis, reglas YARA, etc.) cuando son relevantes para seguir la solución.

## Metodología

- **Terminal local primero:** siempre que un reto se resuelve por `nc`/`ssh`/sockets, se prioriza conectar desde la terminal local en vez de depender del webshell embebido de la plataforma (que ha mostrado inestabilidad — pestañas colgadas, reconexiones fallidas — en sesiones largas o con `nc` intensivo).
- **Sin apurar instancias:** las instancias de reto son efímeras (~15–30 min); si el webshell se traba, se reintenta una vez de forma directa o se pasa al siguiente reto en vez de perder tiempo esperando.
- Un reto por carpeta, con su propio writeup — nada de flags sueltas en el historial de git.

## Próximos pasos

Con **General Skills** (Easy, Medium, Hard), **Web Exploitation** (Easy, Medium) y **Cryptography** (Easy, Medium: 45/45) al 100%, se continuará con:
1. **Cryptography Hard**
2. **Web Exploitation Hard**
3. Resto de categorías: Reverse Engineering, Forensics, Binary Exploitation, Blockchain, Artificial Intelligence. Ver [PROGRESS.md](PROGRESS.md) para el detalle.

## Aviso

Este material es para uso educativo propio sobre retos públicos (picoCTF, vía CyLab Security Academy) que autorizan explícitamente su resolución. Evita publicar las flags fuera de un contexto de práctica personal como este.
