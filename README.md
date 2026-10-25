# CyLab picoCTF — Writeups

> Este repositorio es parte de **[sec-proy](https://github.com/hackadvisermx/sec-proy)**, un proyecto más amplio de soluciones a retos de ciberseguridad (CTFs, wargames y máquinas de hacking).

Writeups propios de retos de **CyLab Security Academy** ([learn.cylabacademy.org](https://learn.cylabacademy.org)), la plataforma de la Carnegie Mellon University que aloja el archivo histórico de **picoCTF** (2019–2026, picoMini, etc.) organizado en un "Challenge Library" por categoría y dificultad.

A diferencia de wargames con progresión estrictamente secuencial (Bandit, Natas), en CyLab cada reto es independiente: se navega por **categoría** (Web Exploitation, Cryptography, Reverse Engineering, Forensics, General Skills, Binary Exploitation, Blockchain, Artificial Intelligence) y **dificultad** (Easy / Medium / Hard).

> **Sobre las flags:** los writeups documentan la técnica usada para resolver cada reto, no las flags en sí. Las flags obtenidas se guardan solo localmente en `creds.txt`.

## Estado actual

- **Progreso global en plataforma:** **486 / 525 retos resueltos (92.57%)**
- **Total retos pendientes:** **39**
- **Verificación:** API de CyLab, **2026-10-24** (el estado de esta sección es la fuente de verdad).

### Resumen por categoría

| Categoría | Resueltos | Total | % | Estado / Pendientes |
|---|---|---|---|---|
| Artificial Intelligence | 16 | 16 | 100.0% | ✅ Completo (Easy 16/16) |
| Blockchain | 4 | 4 | 100.0% | ✅ Completo (Medium 2/2, Hard 2/2) |
| Cryptography | 83 | 83 | 100.0% | ✅ Completo (Easy 8/8, Medium 45/45, Hard 30/30) |
| Forensics | 86 | 86 | 100.0% | ✅ Completo (Easy 15/15, Medium 54/54, Hard 17/17) |
| General Skills | 75 | 75 | 100.0% | ✅ Completo (Easy 49/49, Medium 24/24, Hard 2/2) |
| Web Exploitation | 81 | 83 | 97.6% | ⏳ 2 pendientes en Hard: `cancri-sp` [344], `msfroggenerator2` [360] |
| Reverse Engineering | 97 | 102 | 95.1% | ⏳ 5 pendientes: `speeds and feeds` [116] (Medium, mantenimiento) + 4 en Hard |
| Binary Exploitation | 44 | 76 | 57.9% | ⏳ 32 pendientes: `Binary Gauntlet 2` [143] (Medium) + 31 en Hard |
| **Total** | **486** | **525** | **92.57%** | **39 pendientes** |

### Desglose por categoría y dificultad

| Categoría | Dificultad | Resueltos | Total | % | Estado |
|---|---|---|---|---|---|
| General Skills | Easy | 49 | 49 | 100.0% | ✅ Resueltos y documentados |
| General Skills | Medium | 24 | 24 | 100.0% | ✅ Resueltos y documentados |
| General Skills | Hard | 2 | 2 | 100.0% | ✅ Resueltos y documentados |
| Web Exploitation | Easy | 20 | 20 | 100.0% | ✅ Resueltos y documentados |
| Web Exploitation | Medium | 47 | 47 | 100.0% | ✅ Resueltos y documentados |
| Web Exploitation | Hard | 14 | 16 | 87.5% | ⏳ 14 resueltos, 2 pendientes: msfroggenerator2 [360], cancri-sp [344] |
| Forensics | Easy | 15 | 15 | 100.0% | ✅ Resueltos y documentados |
| Forensics | Medium | 54 | 54 | 100.0% | ✅ Resueltos y documentados |
| Forensics | Hard | 17 | 17 | 100.0% | ✅ Resueltos y documentados |
| Cryptography | Easy | 8 | 8 | 100.0% | ✅ Resueltos y documentados |
| Cryptography | Medium | 45 | 45 | 100.0% | ✅ Resueltos y documentados |
| Cryptography | Hard | 30 | 30 | 100.0% | ✅ Resueltos y documentados |
| Reverse Engineering | Easy | 14 | 14 | 100.0% | ✅ Resueltos y documentados |
| Reverse Engineering | Medium | 52 | 53 | 98.1% | ⏳ 52 resueltos, 1 pendiente: speeds and feeds [116] (mantenimiento) |
| Reverse Engineering | Hard | 35 | 35 | 100.0% | ✅ Resueltos y documentados |
| Binary Exploitation | Easy | 5 | 5 | 100.0% | ✅ Resueltos y documentados |
| Binary Exploitation | Medium | 37 | 37 | 100.0% | ✅ Resueltos y documentados |
| Binary Exploitation | Hard | 6 | 34 | 17.6% | ⏳ 6 resueltos, 28 pendientes: Pizza Router [758], handoff [486], babygame03 [446], high frequency troubles [441], Horsetrack [353], babygame02 [346], wine [317], stack cache [306], solfire [302], ropfu [292], function overwrite [272], buffer overflow 3 [260], vr-school [218], homework [217], lockdown-horses [214], SaaS [213], Unsubscriptions Are Free [187], filtered-shellcode [184], Bizz Fuzz [181], Here's a LIBC [179], Turboflan [178], The Office [172], Kit Engine [168], Stonk Market [164], Download Horsepower [135], Guessing Game 2 [89], zero_to_hero [75], sice_cream [55] |
| Blockchain | Medium | 2 | 2 | 100.0% | ✅ Resueltos y documentados |
| Blockchain | Hard | 2 | 2 | 100.0% | ✅ Resueltos y documentados |
| Artificial Intelligence | Easy | 16 | 16 | 100.0% | ✅ Resueltos y documentados |

Los pendientes de Hard que no caben en la columna de estado están listados completos en **[PROGRESS.md](PROGRESS.md#pendientes-reales-39)**.

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
    │   └── hard/                   # 31/35 resueltos (4 pendientes)
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

Con 486 de 525 retos resueltos (92.57%) y 5 tracks al 100% (Artificial Intelligence, Blockchain, Cryptography, Forensics, General Skills), los esfuerzos se concentran en los **39 retos pendientes**:

1. **Binary Exploitation (32 pendientes):**
   - Medium: `Binary Gauntlet 2` [143].
   - Hard: 31 pendientes. Validados en plataforma: `fermat-strings` [215], `offset-cycleV2` [738] y `Heap Havoc` [763]. El resto tiene análisis técnico local, pero sus flags no fueron aceptadas (`Kit Engine`, `Download Horsepower`, `ropfu`, `buffer overflow 3`, `function overwrite`, `wine`, etc.).
2. **Reverse Engineering (5 pendientes):**
   - Medium: `speeds and feeds` [116] (en mantenimiento).
   - Hard: `Checkpass` [149], `Binary Instrumentation 3` [699], `Binary Instrumentation 4` [700], `JITFP` [737].
3. **Web Exploitation (2 pendientes):**
   - Hard: `cancri-sp` [344] y `msfroggenerator2` [360].

## Aviso

Este material es para uso educativo propio sobre retos públicos (picoCTF, vía CyLab Security Academy) que autorizan explícitamente su resolución. Evita publicar las flags fuera de un contexto de práctica personal como este.
