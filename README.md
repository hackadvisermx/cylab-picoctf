# CyLab picoCTF — Writeups

> Este repositorio es parte de **[sec-proy](https://github.com/hackadvisermx/sec-proy)**, un proyecto más amplio de soluciones a retos de ciberseguridad (CTFs, wargames y máquinas de hacking).

Writeups propios de retos de **CyLab Security Academy** ([learn.cylabacademy.org](https://learn.cylabacademy.org)), la plataforma de la Carnegie Mellon University que aloja el archivo histórico de **picoCTF** (2019–2026, picoMini, etc.) organizado en un "Challenge Library" por categoría y dificultad.

A diferencia de wargames con progresión estrictamente secuencial (Bandit, Natas), en CyLab cada reto es independiente: se navega por **categoría** (Web Exploitation, Cryptography, Reverse Engineering, Forensics, General Skills, Binary Exploitation, Blockchain, Artificial Intelligence) y **dificultad** (Easy / Medium / Hard).

> **Sobre las flags:** los writeups documentan la técnica usada para resolver cada reto, no las flags en sí. Las flags obtenidas se guardan solo localmente en `scripts/creds.txt` (excluido del repo vía `.gitignore`).

## Estado actual

- **Progreso global en plataforma:** **481 / 525 retos resueltos (91.62%)**
- **Total retos pendientes:** **44**

### Resumen por categoría

| Categoría | Resueltos | Total | % | Estado / Pendientes |
|---|---|---|---|---|
| Artificial Intelligence | 16 | 16 | 100.0% | ✅ Completo (Easy 16/16) |
| Blockchain | 4 | 4 | 100.0% | ✅ Completo (Medium 2/2, Hard 2/2) |
| Cryptography | 83 | 83 | 100.0% | ✅ Completo (Easy 8/8, Medium 45/45, Hard 30/30) |
| Forensics | 86 | 86 | 100.0% | ✅ Completo (Easy 15/15, Medium 54/54, Hard 17/17) |
| General Skills | 75 | 75 | 100.0% | ✅ Completo (Easy 49/49, Medium 24/24, Hard 2/2) |
| Web Exploitation | 81 | 83 | 97.6% | ⏳ 2 pendientes (Easy 20/20, Medium 47/47, Hard 14/16: cancri-sp [344], msfroggenerator2 [360]) |
| Reverse Engineering | 92 | 102 | 90.2% | ⏳ 10 pendientes (Easy 14/14, Medium 52/53 [speeds and feeds - 116 en mantenimiento], Hard 26/35 [9 pendientes]) |
| Binary Exploitation | 44 | 76 | 57.9% | ⏳ 32 pendientes (Easy 5/5, Medium 36/37 [Binary Gauntlet 2 - 143], Hard 3/34 [fermat-strings - 215, Kit Engine, Download Horsepower resueltos; 31 pendientes]) |
| **Total** | **481** | **525** | **91.62%** | **44 pendientes** |

### Desglose por categoría y dificultad

| Categoría | Dificultad | Resueltos | Total | % | Estado |
|---|---|---|---|---|---|
| General Skills | Easy | 49 | 49 | 100% | ✅ Resueltos y documentados |
| General Skills | Medium | 24 | 24 | 100% | ✅ Resueltos y documentados |
| General Skills | Hard | 2 | 2 | 100% | ✅ Resueltos y documentados |
| Web Exploitation | Easy | 20 | 20 | 100% | ✅ Resueltos y documentados |
| Web Exploitation | Medium | 47 | 47 | 100% | ✅ Resueltos y documentados |
| Web Exploitation | Hard | 14 | 16 | 87.5% | ⏳ 14 resueltos, 2 pendientes (cancri-sp [344], msfroggenerator2 [360]) |
| Forensics | Easy | 15 | 15 | 100% | ✅ Resueltos y documentados |
| Forensics | Medium | 54 | 54 | 100% | ✅ Resueltos y documentados |
| Forensics | Hard | 17 | 17 | 100% | ✅ Resueltos y documentados |
| Cryptography | Easy | 8 | 8 | 100% | ✅ Resueltos y documentados |
| Cryptography | Medium | 45 | 45 | 100% | ✅ Resueltos y documentados |
| Cryptography | Hard | 30 | 30 | 100% | ✅ Resueltos y documentados |
| Reverse Engineering | Easy | 14 | 14 | 100% | ✅ Resueltos y documentados |
| Reverse Engineering | Medium | 52 | 53 | 98.1% | ⏳ 52 resueltos, 1 pendiente: speeds and feeds [116] (en mantenimiento) |
| Reverse Engineering | Hard | 26 | 35 | 74.3% | ⏳ 26 resueltos, 9 pendientes |
| Binary Exploitation | Easy | 5 | 5 | 100% | ✅ Resueltos y documentados |
| Binary Exploitation | Medium | 36 | 37 | 97.3% | ⏳ 36 resueltos, 1 pendiente: Binary Gauntlet 2 [143] |
| Binary Exploitation | Hard | 3 | 34 | 8.8% | ⏳ 3 resueltos (fermat-strings [215], Kit Engine, Download Horsepower), 31 pendientes |
| Blockchain | Medium | 2 | 2 | 100% | ✅ Resueltos y documentados |
| Blockchain | Hard | 2 | 2 | 100% | ✅ Resueltos y documentados |
| Artificial Intelligence | Easy | 16 | 16 | 100% | ✅ Resueltos y documentados |

El detalle reto por reto, en el orden en que aparecen en la plataforma, está en **[PROGRESS.md](PROGRESS.md)**.

## Estructura del repositorio

```
.
├── PROGRESS.md                    # Tracking detallado: tablas por categoría/dificultad, fases y notas de progreso
└── challenges/
    ├── _template/
    │   └── README.md               # Plantilla base para cada writeup nuevo
    ├── general-skills/
    │   ├── easy/                   # 49 retos (100%)
    │   ├── medium/                 # 24 retos (100%)
    │   └── hard/                   # 2 retos (100%)
    ├── web-exploitation/
    │   ├── easy/                   # 20 retos (100%)
    │   ├── medium/                 # 47 retos (100%)
    │   └── hard/                   # 14/16 resueltos (2 pendientes)
    ├── forensics/
    │   ├── easy/                   # 15 retos (100%)
    │   ├── medium/                 # 54 retos (100%)
    │   └── hard/                   # 17 retos (100%)
    ├── cryptography/
    │   ├── easy/                   # 8 retos (100%)
    │   ├── medium/                 # 45 retos (100%)
    │   └── hard/                   # 30 retos (100%)
    ├── reverse-engineering/
    │   ├── easy/                   # 14 retos (100%)
    │   ├── medium/                 # 52/53 resueltos (1 pendiente)
    │   └── hard/                   # 26/35 resueltos (9 pendientes)
    ├── binary-exploitation/
    │   ├── easy/                   # 5 retos (100%)
    │   ├── medium/                 # 36/37 resueltos (1 pendiente)
    │   └── hard/                   # 3/34 resueltos (31 pendientes)
    ├── blockchain/
    │   ├── medium/                 # 2 retos (100%)
    │   └── hard/                   # 2 retos (100%)
    └── artificial-intelligence/
        └── easy/                   # 16 retos (100%)
```

Cada writeup vive en su propia carpeta (`challenges/<categoría>/<dificultad>/<slug>/README.md`) y sigue la plantilla de [`challenges/_template/README.md`](challenges/_template/README.md): descripción oficial del reto, categoría/dificultad/evento/autor, solución paso a paso con los comandos usados, notas adicionales y referencias. Algunas carpetas incluyen también archivos de apoyo descargados del reto (código fuente, logs, binarios de análisis, reglas YARA, etc.) cuando son relevantes para seguir la solución.

## Metodología

- **Terminal local primero:** siempre que un reto se resuelve por `nc`/`ssh`/sockets, se prioriza conectar desde la terminal local en vez de depender del webshell embebido de la plataforma (que ha mostrado inestabilidad — pestañas colgadas, reconexiones fallidas — en sesiones largas o con `nc` intensivo).
- **Sin apurar instancias:** las instancias de reto son efímeras (~15–30 min); si el webshell se traba, se reintenta una vez de forma directa o se pasa al siguiente reto en vez de perder tiempo esperando.
- Un reto por carpeta, con su propio writeup — nada de flags sueltas en el historial de git.

## Próximos pasos

Con 481 de 525 retos resueltos (91.62%) y 5 tracks al 100% (Artificial Intelligence, Blockchain, Cryptography, Forensics, General Skills), los esfuerzos se concentran en los **44 retos pendientes**:

1. **Binary Exploitation (32 pendientes):**
   - Medium: `Binary Gauntlet 2` [143] (1 pendiente).
   - Hard: 31 retos pendientes (con `fermat-strings` [215], `Kit Engine` y `Download Horsepower` resueltos).
2. **Reverse Engineering (10 pendientes):**
   - Medium: `speeds and feeds` [116] (1 pendiente, bajo mantenimiento en plataforma).
   - Hard: 9 retos pendientes (26/35 resueltos).
3. **Web Exploitation (2 pendientes):**
   - Hard: `cancri-sp` [344] y `msfroggenerator2` [360] (2 pendientes).

## Aviso

Este material es para uso educativo propio sobre retos públicos (picoCTF, vía CyLab Security Academy) que autorizan explícitamente su resolución. Evita publicar las flags fuera de un contexto de práctica personal como este.
