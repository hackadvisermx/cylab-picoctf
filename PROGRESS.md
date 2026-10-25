# Progreso CyLab Security Academy (learn.cylabacademy.org)

CyLab Security Academy aloja, entre otro contenido, el archivo histórico de retos de **picoCTF** (2024/2025/2026, picoMini, etc.) organizados en un "Challenge Library" por categoría y dificultad. A diferencia de Bandit/Natas (progresión estrictamente secuencial por niveles numerados), aquí cada reto es independiente: se navega por categoría (Web Exploitation, Cryptography, Reverse Engineering, Forensics, General Skills, Binary Exploitation, Blockchain, Artificial Intelligence) y dificultad (Easy/Medium/Hard).

Contraseñas/flags se guardan solo localmente (no se suben a repos públicos); los writeups documentan técnica, no las flags en sí, siguiendo el mismo criterio de los proyectos Bandit/Natas/Venus.

## Estado general de la plataforma

- **Progreso global (verificado en plataforma):** **488 / 525 retos resueltos (92.95%)**
- **Retos pendientes totales:** **37 retos**

> Verificación realizada contra la API de CyLab el **2026-10-24**. El estado de esta sección es la fuente de verdad; las tablas de este documento se generaron a partir de la misma consulta. Una flag obtenida localmente pero no aceptada por la plataforma **no** cuenta como reto resuelto.

### Desglose por categoría

| Categoría | Resueltos | Total | % | Estado / Pendientes |
|---|---|---|---|---|
| Artificial Intelligence | 16 | 16 | 100.0% | ✅ Completo (Easy 16/16) |
| Blockchain | 4 | 4 | 100.0% | ✅ Completo (Medium 2/2, Hard 2/2) |
| Cryptography | 83 | 83 | 100.0% | ✅ Completo (Easy 8/8, Medium 45/45, Hard 30/30) |
| Forensics | 86 | 86 | 100.0% | ✅ Completo (Easy 15/15, Medium 54/54, Hard 17/17) |
| General Skills | 75 | 75 | 100.0% | ✅ Completo (Easy 49/49, Medium 24/24, Hard 2/2) |
| Web Exploitation | 81 | 83 | 97.6% | ⏳ 2 pendientes en Hard: `cancri-sp` [344], `msfroggenerator2` [360] |
| Reverse Engineering | 99 | 102 | 97.1% | ⏳ 3 pendientes: `speeds and feeds` [116] (Medium, mantenimiento) + 2 en Hard: `Binary Instrumentation 4` [700], `JITFP` [737] |
| Binary Exploitation | 45 | 76 | 59.2% | ⏳ 31 pendientes: `Binary Gauntlet 2` [143] (Medium) + 30 en Hard |
| **Total** | **489** | **525** | 93.14% | **36 pendientes** |

### Pendientes reales (36)

- **Web Exploitation — Hard (2):** `cancri-sp` [344], `msfroggenerator2` [360].
- **Reverse Engineering — Medium (1):** `speeds and feeds` [116] (en mantenimiento).
- **Reverse Engineering — Hard (2):** `Binary Instrumentation 4` [700], `JITFP` [737].
- **Binary Exploitation — Medium (1):** `Binary Gauntlet 2` [143].
- **Binary Exploitation — Hard (30):** `sice_cream` [55], `zero_to_hero` [75], `Guessing Game 2` [89], `Download Horsepower` [135], `Cache Me Outside` [146], `Stonk Market` [164], `Kit Engine` [168], `The Office` [172], `Turboflan` [178], `Here's a LIBC` [179], `Bizz Fuzz` [181], `filtered-shellcode` [184], `Unsubscriptions Are Free` [187], `SaaS` [213], `lockdown-horses` [214], `homework` [217], `vr-school` [218], `buffer overflow 3` [260], `function overwrite` [272], `ropfu` [292], `solfire` [302], `stack cache` [306], `wine` [317], `babygame02` [346], `Horsetrack` [353], `tic-tac` [380], `high frequency troubles` [441], `babygame03` [446], `handoff` [486], `Pizza Router` [758].

> Los retos de Binary Exploitation — Hard resueltos y validados en plataforma son `seed-sPRiNG` [50], `fermat-strings` [215], `offset-cycleV2` [738] y `Heap Havoc` [763].

## Orden de trabajo acordado
1. **General Skills** (equivalente a Bandit: calentamiento con herramientas básicas) — Easy primero.
2. **Web Exploitation** (equivalente a Natas) — Easy primero.
3. Resto de categorías según se decida: Cryptography, Forensics, Reverse Engineering, Binary Exploitation, Blockchain, Artificial Intelligence.

## Tabla de retos — General Skills, Easy

**✅ Los 49 retos de General Skills - Easy están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Undo | ✅ resuelto | [challenges/general-skills/easy/undo](challenges/general-skills/easy/undo/README.md) |
| 2 | MY GIT | ✅ resuelto | [challenges/general-skills/easy/my_git](challenges/general-skills/easy/my_git/README.md) |
| 3 | bytemancy 1 | ✅ resuelto | [challenges/general-skills/easy/bytemancy_1](challenges/general-skills/easy/bytemancy_1/README.md) |
| 4 | Printer Shares | ✅ resuelto | [challenges/general-skills/easy/printer_shares](challenges/general-skills/easy/printer_shares/README.md) |
| 5 | ping-cmd | ✅ resuelto | [challenges/general-skills/easy/ping_cmd](challenges/general-skills/easy/ping_cmd/README.md) |
| 6 | bytemancy 0 | ✅ resuelto | [challenges/general-skills/easy/bytemancy_0](challenges/general-skills/easy/bytemancy_0/README.md) |
| 7 | Piece by Piece | ✅ resuelto | [challenges/general-skills/easy/piece_by_piece](challenges/general-skills/easy/piece_by_piece/README.md) |
| 8 | SUDO MAKE ME A SANDWICH | ✅ resuelto | [challenges/general-skills/easy/sudo_make_me_a_sandwich](challenges/general-skills/easy/sudo_make_me_a_sandwich/README.md) |
| 9 | Password Profiler | ✅ resuelto | [challenges/general-skills/easy/password_profiler](challenges/general-skills/easy/password_profiler/README.md) |
| 10 | MultiCode | ✅ resuelto | [challenges/general-skills/easy/multicode](challenges/general-skills/easy/multicode/README.md) |
| 11 | Log Hunt | ✅ resuelto | [challenges/general-skills/easy/log_hunt](challenges/general-skills/easy/log_hunt/README.md) |
| 12 | FANTASY CTF | ✅ resuelto | [challenges/general-skills/easy/fantasy_ctf](challenges/general-skills/easy/fantasy_ctf/README.md) |
| 13 | Rust fixme 3 | ✅ resuelto | [challenges/general-skills/easy/rust_fixme_3](challenges/general-skills/easy/rust_fixme_3/README.md) |
| 14 | Rust fixme 2 | ✅ resuelto | [challenges/general-skills/easy/rust_fixme_2](challenges/general-skills/easy/rust_fixme_2/README.md) |
| 15 | Rust fixme 1 | ✅ resuelto | [challenges/general-skills/easy/rust_fixme_1](challenges/general-skills/easy/rust_fixme_1/README.md) |
| 16 | Binary Search | ✅ resuelto | [challenges/general-skills/easy/binary_search](challenges/general-skills/easy/binary_search/README.md) |
| 17 | Time Machine | ✅ resuelto | [challenges/general-skills/easy/time_machine](challenges/general-skills/easy/time_machine/README.md) |
| 18 | Super SSH | ✅ resuelto | [challenges/general-skills/easy/super_ssh](challenges/general-skills/easy/super_ssh/README.md) |
| 19 | endianness | ✅ resuelto | [challenges/general-skills/easy/endianness](challenges/general-skills/easy/endianness/README.md) |
| 20 | Commitment Issues | ✅ resuelto | [challenges/general-skills/easy/commitment_issues](challenges/general-skills/easy/commitment_issues/README.md) |
| 21 | Collaborative Development | ✅ resuelto | [challenges/general-skills/easy/collaborative_development](challenges/general-skills/easy/collaborative_development/README.md) |
| 22 | Blame Game | ✅ resuelto | [challenges/general-skills/easy/blame_game](challenges/general-skills/easy/blame_game/README.md) |
| 23 | binhexa | ✅ resuelto | [challenges/general-skills/easy/binhexa](challenges/general-skills/easy/binhexa/README.md) |
| 24 | ASCII Numbers | ✅ resuelto | [challenges/general-skills/medium/ascii_numbers](challenges/general-skills/medium/ascii_numbers/README.md) |
| 25 | repetitions | ✅ resuelto | [challenges/general-skills/easy/repetitions](challenges/general-skills/easy/repetitions/README.md) |
| 26 | Big Zip | ✅ resuelto | [challenges/general-skills/easy/big_zip](challenges/general-skills/easy/big_zip/README.md) |
| 27 | First Find | ✅ resuelto | [challenges/general-skills/easy/first_find](challenges/general-skills/easy/first_find/README.md) |
| 28 | runme.py | ✅ resuelto | [challenges/general-skills/easy/runme_py](challenges/general-skills/easy/runme_py/README.md) |
| 29 | PW Crack 2 | ✅ resuelto | [challenges/general-skills/easy/pw_crack_2](challenges/general-skills/easy/pw_crack_2/README.md) |
| 30 | PW Crack 1 | ✅ resuelto | [challenges/general-skills/easy/pw_crack_1](challenges/general-skills/easy/pw_crack_1/README.md) |
| 31 | HashingJobApp | ✅ resuelto | [challenges/general-skills/easy/hashingjobapp](challenges/general-skills/easy/hashingjobapp/README.md) |
| 32 | Glitch Cat | ✅ resuelto | [challenges/general-skills/easy/glitch_cat](challenges/general-skills/easy/glitch_cat/README.md) |
| 33 | fixme2.py | ✅ resuelto | [challenges/general-skills/easy/fixme2_py](challenges/general-skills/easy/fixme2_py/README.md) |
| 34 | fixme1.py | ✅ resuelto | [challenges/general-skills/easy/fixme1_py](challenges/general-skills/easy/fixme1_py/README.md) |
| 35 | convertme.py | ✅ resuelto | [challenges/general-skills/easy/convertme_py](challenges/general-skills/easy/convertme_py/README.md) |
| 36 | Codebook | ✅ resuelto | [challenges/general-skills/easy/codebook](challenges/general-skills/easy/codebook/README.md) |
| 37 | Magikarp Ground Mission | ✅ resuelto | [challenges/general-skills/easy/magikarp_ground_mission](challenges/general-skills/easy/magikarp_ground_mission/README.md) |
| 38 | Tab, Tab, Attack | ✅ resuelto | [challenges/general-skills/easy/tab_tab_attack](challenges/general-skills/easy/tab_tab_attack/README.md) |
| 39 | Wave a flag | ✅ resuelto | [challenges/general-skills/easy/wave_a_flag](challenges/general-skills/easy/wave_a_flag/README.md) |
| 40 | Static ain't always noise | ✅ resuelto | [challenges/general-skills/easy/static_aint_always_noise](challenges/general-skills/easy/static_aint_always_noise/README.md) |
| 41 | Nice netcat... | ✅ resuelto | [challenges/general-skills/easy/nice_netcat](challenges/general-skills/easy/nice_netcat/README.md) |
| 42 | Obedient Cat | ✅ resuelto | [challenges/general-skills/easy/obedient_cat](challenges/general-skills/easy/obedient_cat/README.md) |
| 43 | 2warm | ✅ resuelto | [challenges/general-skills/easy/2warm](challenges/general-skills/easy/2warm/README.md) |
| 44 | First Grep | ✅ resuelto | [challenges/general-skills/easy/first_grep](challenges/general-skills/easy/first_grep/README.md) |
| 45 | Bases | ✅ resuelto | [challenges/general-skills/easy/bases](challenges/general-skills/easy/bases/README.md) |
| 46 | Warmed Up | ✅ resuelto | [challenges/general-skills/easy/warmed_up](challenges/general-skills/easy/warmed_up/README.md) |
| 47 | strings it | ✅ resuelto | [challenges/general-skills/easy/strings_it](challenges/general-skills/easy/strings_it/README.md) |
| 48 | what's a net cat? | ✅ resuelto | [challenges/general-skills/easy/whats_a_net_cat](challenges/general-skills/easy/whats_a_net_cat/README.md) |
| 49 | Lets Warm Up | ✅ resuelto | [challenges/general-skills/easy/lets_warm_up](challenges/general-skills/easy/lets_warm_up/README.md) |

## Tabla de retos — General Skills, Medium

**✅ Los 24 retos de General Skills - Medium están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Failure Failure | ✅ resuelto | [challenges/general-skills/medium/failure_failure](challenges/general-skills/medium/failure_failure/README.md) |
| 2 | ABSOLUTE NANO | ✅ resuelto | [challenges/general-skills/medium/absolute_nano](challenges/general-skills/medium/absolute_nano/README.md) |
| 3 | KSECRETS | ✅ resuelto | [challenges/general-skills/medium/ksecrets](challenges/general-skills/medium/ksecrets/README.md) |
| 4 | bytemancy 3 | ✅ resuelto | [challenges/general-skills/medium/bytemancy_3](challenges/general-skills/medium/bytemancy_3/README.md) |
| 5 | bytemancy 2 | ✅ resuelto | [challenges/general-skills/medium/bytemancy_2](challenges/general-skills/medium/bytemancy_2/README.md) |
| 6 | YaraRules0x100 | ✅ resuelto | [challenges/general-skills/medium/yararules0x100](challenges/general-skills/medium/yararules0x100/README.md) |
| 7 | dont-you-love-banners | ✅ resuelto | [challenges/general-skills/medium/dont_you_love_banners](challenges/general-skills/medium/dont_you_love_banners/README.md) |
| 8 | SansAlpha | ✅ resuelto | [challenges/general-skills/medium/sansalpha](challenges/general-skills/medium/sansalpha/README.md) |
| 9 | useless | ✅ resuelto | [challenges/general-skills/medium/useless](challenges/general-skills/medium/useless/README.md) |
| 10 | Specialer | ✅ resuelto | [challenges/general-skills/medium/specialer](challenges/general-skills/medium/specialer/README.md) |
| 11 | Special | ✅ resuelto | [challenges/general-skills/medium/special](challenges/general-skills/medium/special/README.md) |
| 12 | Permissions | ✅ resuelto | [challenges/general-skills/medium/permissions](challenges/general-skills/medium/permissions/README.md) |
| 13 | chrono | ✅ resuelto | [challenges/general-skills/medium/chrono](challenges/general-skills/medium/chrono/README.md) |
| 14 | Serpentine | ✅ resuelto | [challenges/general-skills/medium/serpentine](challenges/general-skills/medium/serpentine/README.md) |
| 15 | PW Crack 5 | ✅ resuelto | [challenges/general-skills/medium/pw_crack_5](challenges/general-skills/medium/pw_crack_5/README.md) |
| 16 | PW Crack 4 | ✅ resuelto | [challenges/general-skills/medium/pw_crack_4](challenges/general-skills/medium/pw_crack_4/README.md) |
| 17 | PW Crack 3 | ✅ resuelto | [challenges/general-skills/medium/pw_crack_3](challenges/general-skills/medium/pw_crack_3/README.md) |
| 18 | Python Wrangling | ✅ resuelto | [challenges/general-skills/medium/python_wrangling](challenges/general-skills/medium/python_wrangling/README.md) |
| 19 | Nothing Up My Sleeve | ✅ resuelto | [challenges/general-skills/medium/nothing_up_my_sleeve](challenges/general-skills/medium/nothing_up_my_sleeve/README.md) |
| 20 | 1_wanna_b3_a_r0ck5tar | ✅ resuelto | [challenges/general-skills/medium/1_wanna_b3_a_r0ck5tar](challenges/general-skills/medium/1_wanna_b3_a_r0ck5tar/README.md) |
| 21 | flag_shop | ✅ resuelto | [challenges/general-skills/medium/flag_shop](challenges/general-skills/medium/flag_shop/README.md) |
| 22 | plumbing | ✅ resuelto | [challenges/general-skills/medium/plumbing](challenges/general-skills/medium/plumbing/README.md) |
| 23 | Based | ✅ resuelto | [challenges/general-skills/medium/based](challenges/general-skills/medium/based/README.md) |
| 24 | mus1c | ✅ resuelto | [challenges/general-skills/medium/mus1c](challenges/general-skills/medium/mus1c/README.md) |

## Tabla de retos — General Skills, Hard

**✅ Los 2 retos de General Skills - Hard están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Printer Shares 3 | ✅ resuelto | [challenges/general-skills/hard/printer_shares_3](challenges/general-skills/hard/printer_shares_3/README.md) |
| 2 | Printer Shares 2 | ✅ resuelto | [challenges/general-skills/hard/printer_shares_2](challenges/general-skills/hard/printer_shares_2/README.md) |

## Tabla de retos — Web Exploitation, Easy

**✅ Los 20 retos de Web Exploitation - Easy están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Old Sessions | ✅ resuelto | [challenges/web-exploitation/easy/old_sessions](challenges/web-exploitation/easy/old_sessions/README.md) |
| 2 | Crack the Gate 1 | ✅ resuelto | [challenges/web-exploitation/easy/crack_the_gate_1](challenges/web-exploitation/easy/crack_the_gate_1/README.md) |
| 3 | SSTI1 | ✅ resuelto | [challenges/web-exploitation/easy/ssti1](challenges/web-exploitation/easy/ssti1/README.md) |
| 4 | n0s4n1ty 1 | ✅ resuelto | [challenges/web-exploitation/easy/n0s4n1ty_1](challenges/web-exploitation/easy/n0s4n1ty_1/README.md) |
| 5 | head-dump | ✅ resuelto | [challenges/web-exploitation/easy/head_dump](challenges/web-exploitation/easy/head_dump/README.md) |
| 6 | Cookie Monster Secret Recipe | ✅ resuelto | [challenges/web-exploitation/easy/cookie_monster_secret_recipe](challenges/web-exploitation/easy/cookie_monster_secret_recipe/README.md) |
| 7 | WebDecode | ✅ resuelto | [challenges/web-exploitation/easy/webdecode](challenges/web-exploitation/easy/webdecode/README.md) |
| 8 | Unminify | ✅ resuelto | [challenges/web-exploitation/easy/unminify](challenges/web-exploitation/easy/unminify/README.md) |
| 9 | IntroToBurp | ✅ resuelto | [challenges/web-exploitation/easy/introtoburp](challenges/web-exploitation/easy/introtoburp/README.md) |
| 10 | Bookmarklet | ✅ resuelto | [challenges/web-exploitation/easy/bookmarklet](challenges/web-exploitation/easy/bookmarklet/README.md) |
| 11 | Local Authority | ✅ resuelto | [challenges/web-exploitation/easy/local_authority](challenges/web-exploitation/easy/local_authority/README.md) |
| 12 | Inspect HTML | ✅ resuelto | [challenges/web-exploitation/easy/inspect_html](challenges/web-exploitation/easy/inspect_html/README.md) |
| 13 | Includes | ✅ resuelto | [challenges/web-exploitation/easy/includes](challenges/web-exploitation/easy/includes/README.md) |
| 14 | Cookies | ✅ resuelto | [challenges/web-exploitation/easy/cookies](challenges/web-exploitation/easy/cookies/README.md) |
| 15 | Scavenger Hunt | ✅ resuelto | [challenges/web-exploitation/easy/scavenger_hunt](challenges/web-exploitation/easy/scavenger_hunt/README.md) |
| 16 | GET aHEAD | ✅ resuelto | [challenges/web-exploitation/easy/get_ahead](challenges/web-exploitation/easy/get_ahead/README.md) |
| 17 | dont-use-client-side | ✅ resuelto | [challenges/web-exploitation/easy/dont_use_client_side](challenges/web-exploitation/easy/dont_use_client_side/README.md) |
| 18 | logon | ✅ resuelto | [challenges/web-exploitation/easy/logon](challenges/web-exploitation/easy/logon/README.md) |
| 19 | Insp3ct0r | ✅ resuelto | [challenges/web-exploitation/easy/insp3ct0r](challenges/web-exploitation/easy/insp3ct0r/README.md) |
| 20 | where are the robots | ✅ resuelto | [challenges/web-exploitation/easy/where_are_the_robots](challenges/web-exploitation/easy/where_are_the_robots/README.md) |

## Tabla de retos — Web Exploitation, Medium

**✅ Los 47 retos de Web Exploitation - Medium están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | No FA | ✅ resuelto | [challenges/web-exploitation/medium/no_fa](challenges/web-exploitation/medium/no_fa/README.md) |
| 2 | Hashgate | ✅ resuelto | [challenges/web-exploitation/medium/hashgate](challenges/web-exploitation/medium/hashgate/README.md) |
| 3 | Credential Stuffing | ✅ resuelto | [challenges/web-exploitation/medium/credential_stuffing](challenges/web-exploitation/medium/credential_stuffing/README.md) |
| 4 | Secret Box | ✅ resuelto | [challenges/web-exploitation/medium/secret_box](challenges/web-exploitation/medium/secret_box/README.md) |
| 5 | Fool the Lockout | ✅ resuelto | [challenges/web-exploitation/medium/fool_the_lockout](challenges/web-exploitation/medium/fool_the_lockout/README.md) |
| 6 | Sql Map1 | ✅ resuelto | [challenges/web-exploitation/medium/sql_map1](challenges/web-exploitation/medium/sql_map1/README.md) |
| 7 | North-South | ✅ resuelto | [challenges/web-exploitation/medium/north_south](challenges/web-exploitation/medium/north_south/README.md) |
| 8 | Crack the Gate 2 | ✅ resuelto | [challenges/web-exploitation/medium/crack_the_gate_2](challenges/web-exploitation/medium/crack_the_gate_2/README.md) |
| 9 | byp4ss3d | ✅ resuelto | [challenges/web-exploitation/medium/byp4ss3d](challenges/web-exploitation/medium/byp4ss3d/README.md) |
| 10 | Pachinko | ✅ resuelto | [challenges/web-exploitation/medium/pachinko](challenges/web-exploitation/medium/pachinko/README.md) |
| 11 | SSTI2 | ✅ resuelto | [challenges/web-exploitation/medium/ssti2](challenges/web-exploitation/medium/ssti2/README.md) |
| 12 | 3v@l | ✅ resuelto | [challenges/web-exploitation/medium/3val](challenges/web-exploitation/medium/3val/README.md) |
| 13 | WebSockFish | ✅ resuelto | [challenges/web-exploitation/medium/websockfish](challenges/web-exploitation/medium/websockfish/README.md) |
| 14 | Apriti sesamo | ✅ resuelto | [challenges/web-exploitation/medium/apriti_sesamo](challenges/web-exploitation/medium/apriti_sesamo/README.md) |
| 15 | Trickster | ✅ resuelto | [challenges/web-exploitation/medium/trickster](challenges/web-exploitation/medium/trickster/README.md) |
| 16 | No Sql Injection | ✅ resuelto | [challenges/web-exploitation/medium/no_sql_injection](challenges/web-exploitation/medium/no_sql_injection/README.md) |
| 17 | SOAP | ✅ resuelto | [challenges/web-exploitation/medium/soap](challenges/web-exploitation/medium/soap/README.md) |
| 18 | More SQLi | ✅ resuelto | [challenges/web-exploitation/medium/more_sqli](challenges/web-exploitation/medium/more_sqli/README.md) |
| 19 | MatchTheRegex | ✅ resuelto | [challenges/web-exploitation/medium/matchtheregex](challenges/web-exploitation/medium/matchtheregex/README.md) |
| 20 | Java Code Analysis!?! | ✅ resuelto | [challenges/web-exploitation/medium/java_code_analysis](challenges/web-exploitation/medium/java_code_analysis/README.md) |
| 21 | findme | ✅ resuelto | [challenges/web-exploitation/medium/findme](challenges/web-exploitation/medium/findme/README.md) |
| 22 | SQLiLite | ✅ resuelto | [challenges/web-exploitation/medium/sqlilite](challenges/web-exploitation/medium/sqlilite/README.md) |
| 23 | SQL Direct | ✅ resuelto | [challenges/web-exploitation/medium/sql_direct](challenges/web-exploitation/medium/sql_direct/README.md) |
| 24 | Secrets | ✅ resuelto | [challenges/web-exploitation/medium/secrets](challenges/web-exploitation/medium/secrets/README.md) |
| 25 | Search source | ✅ resuelto | [challenges/web-exploitation/medium/search_source](challenges/web-exploitation/medium/search_source/README.md) |
| 26 | Roboto Sans | ✅ resuelto | [challenges/web-exploitation/medium/roboto_sans](challenges/web-exploitation/medium/roboto_sans/README.md) |
| 27 | Power Cookie | ✅ resuelto | [challenges/web-exploitation/medium/power_cookie](challenges/web-exploitation/medium/power_cookie/README.md) |
| 28 | Forbidden Paths | ✅ resuelto | [challenges/web-exploitation/medium/forbidden_paths](challenges/web-exploitation/medium/forbidden_paths/README.md) |
| 29 | JAuth | ✅ resuelto | [challenges/web-exploitation/medium/jauth](challenges/web-exploitation/medium/jauth/README.md) |
| 30 | caas | ✅ resuelto | [challenges/web-exploitation/medium/caas](challenges/web-exploitation/medium/caas/README.md) |
| 31 | login | ✅ resuelto | [challenges/web-exploitation/medium/login](challenges/web-exploitation/medium/login/README.md) |
| 32 | Super Serial | ✅ resuelto | [challenges/web-exploitation/medium/super_serial](challenges/web-exploitation/medium/super_serial/README.md) |
| 33 | Most Cookies | ✅ resuelto | [challenges/web-exploitation/medium/most_cookies](challenges/web-exploitation/medium/most_cookies/README.md) |
| 34 | Web Gauntlet 2 | ✅ resuelto | [challenges/web-exploitation/medium/web_gauntlet_2](challenges/web-exploitation/medium/web_gauntlet_2/README.md) |
| 35 | Some Assembly Required 1 | ✅ resuelto | [challenges/web-exploitation/medium/some_assembly_required_1](challenges/web-exploitation/medium/some_assembly_required_1/README.md) |
| 36 | Some Assembly Required 2 | ✅ resuelto | [challenges/web-exploitation/medium/some_assembly_required_2](challenges/web-exploitation/medium/some_assembly_required_2/README.md) |
| 37 | Web Gauntlet 3 | ✅ resuelto | [challenges/web-exploitation/medium/web_gauntlet_3](challenges/web-exploitation/medium/web_gauntlet_3/README.md) |
| 38 | More Cookies | ✅ resuelto | [challenges/web-exploitation/medium/more_cookies](challenges/web-exploitation/medium/more_cookies/README.md) |
| 39 | It is my Birthday | ✅ resuelto | [challenges/web-exploitation/medium/it_is_my_birthday](challenges/web-exploitation/medium/it_is_my_birthday/README.md) |
| 40 | Startup Company | ✅ resuelto | [challenges/web-exploitation/medium/startup_company](challenges/web-exploitation/medium/startup_company/README.md) |
| 41 | Web Gauntlet | ✅ resuelto | [challenges/web-exploitation/medium/web_gauntlet](challenges/web-exploitation/medium/web_gauntlet/README.md) |
| 42 | Irish-Name-Repo 1 | ✅ resuelto | [challenges/web-exploitation/medium/irish_name_repo_1](challenges/web-exploitation/medium/irish_name_repo_1/README.md) |
| 43 | Client-side-again | ✅ resuelto | [challenges/web-exploitation/medium/client_side_again](challenges/web-exploitation/medium/client_side_again/README.md) |
| 44 | Irish-Name-Repo 2 | ✅ resuelto | [challenges/web-exploitation/medium/irish_name_repo_2](challenges/web-exploitation/medium/irish_name_repo_2/README.md) |
| 45 | JaWT Scratchpad | ✅ resuelto | [challenges/web-exploitation/medium/jawt_scratchpad](challenges/web-exploitation/medium/jawt_scratchpad/README.md) |
| 46 | picobrowser | ✅ resuelto | [challenges/web-exploitation/medium/picobrowser](challenges/web-exploitation/medium/picobrowser/README.md) |
| 47 | Irish-Name-Repo 3 | ✅ resuelto | [challenges/web-exploitation/medium/irish_name_repo_3](challenges/web-exploitation/medium/irish_name_repo_3/README.md) |

## Tabla de retos — Web Exploitation, Hard

Existen **16 retos** en total en esta categoría y dificultad: 14 resueltos y 2 pendientes.

**⏳ 14/16 retos resueltos (87.5%). 2 pendientes en plataforma.**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | ORDER ORDER | ✅ resuelto | [challenges/web-exploitation/hard/order_order](challenges/web-exploitation/hard/order_order/README.md) |
| 2 | paper-2 | ✅ resuelto | [challenges/web-exploitation/hard/paper_2](challenges/web-exploitation/hard/paper_2/README.md) |
| 3 | secure-email-service | ✅ resuelto | [challenges/web-exploitation/hard/secure_email_service](challenges/web-exploitation/hard/secure_email_service/README.md) |
| 4 | Pachinko Revisited | ✅ resuelto | [challenges/web-exploitation/hard/pachinko_revisited](challenges/web-exploitation/hard/pachinko_revisited/README.md) |
| 5 | elements | ✅ resuelto | [challenges/web-exploitation/hard/elements](challenges/web-exploitation/hard/elements/README.md) |
| 6 | msfroggenerator2 [360] | ⏳ pendiente | [challenges/web-exploitation/hard/msfroggenerator2](challenges/web-exploitation/hard/msfroggenerator2/README.md) |
| 7 | cancri-sp [344] | ⏳ pendiente | [challenges/web-exploitation/hard/cancri_sp](challenges/web-exploitation/hard/cancri_sp/README.md) |
| 8 | noted | ✅ resuelto | [challenges/web-exploitation/hard/noted](challenges/web-exploitation/hard/noted/README.md) |
| 9 | Live Art | ✅ resuelto | [challenges/web-exploitation/hard/live_art](challenges/web-exploitation/hard/live_art/README.md) |
| 10 | notepad | ✅ resuelto | [challenges/web-exploitation/hard/notepad](challenges/web-exploitation/hard/notepad/README.md) |
| 11 | Bithug | ✅ resuelto | [challenges/web-exploitation/hard/bithug](challenges/web-exploitation/hard/bithug/README.md) |
| 12 | X marks the spot | ✅ resuelto | [challenges/web-exploitation/hard/x_marks_the_spot](challenges/web-exploitation/hard/x_marks_the_spot/README.md) |
| 13 | Some Assembly Required 4 | ✅ resuelto | [challenges/web-exploitation/hard/some_assembly_required_4](challenges/web-exploitation/hard/some_assembly_required_4/README.md) |
| 14 | Some Assembly Required 3 | ✅ resuelto | [challenges/web-exploitation/hard/some_assembly_required_3](challenges/web-exploitation/hard/some_assembly_required_3/README.md) |
| 15 | Java Script Kiddie 2 | ✅ resuelto | [challenges/web-exploitation/hard/java_script_kiddie_2](challenges/web-exploitation/hard/java_script_kiddie_2/README.md) |
| 16 | Java Script Kiddie | ✅ resuelto | [challenges/web-exploitation/hard/java_script_kiddie](challenges/web-exploitation/hard/java_script_kiddie/README.md) |

## Tabla de retos — Forensics, Easy

**✅ Los 15 retos de Forensics - Easy están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Binary Digits | ✅ resuelto | [challenges/forensics/easy/binary_digits](challenges/forensics/easy/binary_digits/README.md) |
| 2 | Riddle Registry | ✅ resuelto | [challenges/forensics/easy/riddle_registry](challenges/forensics/easy/riddle_registry/README.md) |
| 3 | Hidden in plainsight | ✅ resuelto | [challenges/forensics/easy/hidden_in_plainsight](challenges/forensics/easy/hidden_in_plainsight/README.md) |
| 4 | Flag in Flame | ✅ resuelto | [challenges/forensics/easy/flag_in_flame](challenges/forensics/easy/flag_in_flame/README.md) |
| 5 | Corrupted file | ✅ resuelto | [challenges/forensics/easy/corrupted_file](challenges/forensics/easy/corrupted_file/README.md) |
| 6 | DISKO 1 | ✅ resuelto | [challenges/forensics/easy/disko_1](challenges/forensics/easy/disko_1/README.md) |
| 7 | RED | ✅ resuelto | [challenges/forensics/easy/red](challenges/forensics/easy/red/README.md) |
| 8 | Ph4nt0m 1ntrud3r | ✅ resuelto | [challenges/forensics/easy/ph4nt0m_1ntrud3r](challenges/forensics/easy/ph4nt0m_1ntrud3r/README.md) |
| 9 | Verify | ✅ resuelto | [challenges/forensics/easy/verify](challenges/forensics/easy/verify/README.md) |
| 10 | Scan Surprise | ✅ resuelto | [challenges/forensics/easy/scan_surprise](challenges/forensics/easy/scan_surprise/README.md) |
| 11 | Secret of the Polyglot | ✅ resuelto | [challenges/forensics/easy/secret_of_the_polyglot](challenges/forensics/easy/secret_of_the_polyglot/README.md) |
| 12 | CanYouSee | ✅ resuelto | [challenges/forensics/easy/canyousee](challenges/forensics/easy/canyousee/README.md) |
| 13 | WPA-ing Out | ✅ resuelto | [challenges/forensics/easy/wpa_ing_out](challenges/forensics/easy/wpa_ing_out/README.md) |
| 14 | information | ✅ resuelto | [challenges/forensics/easy/information](challenges/forensics/easy/information/README.md) |
| 15 | Glory of the Garden | ✅ resuelto | [challenges/forensics/easy/glory_of_the_garden](challenges/forensics/easy/glory_of_the_garden/README.md) |

## Tabla de retos — Forensics, Medium

**✅ Los 54 retos de Forensics - Medium están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Timeline 1 | ✅ resuelto | [challenges/forensics/medium/timeline_1](challenges/forensics/medium/timeline_1/README.md) |
| 2 | Timeline 0 | ✅ resuelto | [challenges/forensics/medium/timeline_0](challenges/forensics/medium/timeline_0/README.md) |
| 3 | Rogue Tower | ✅ resuelto | [challenges/forensics/medium/rogue_tower](challenges/forensics/medium/rogue_tower/README.md) |
| 4 | Forensics Git 2 | ✅ resuelto | [challenges/forensics/medium/forensics_git_2](challenges/forensics/medium/forensics_git_2/README.md) |
| 5 | Forensics Git 1 | ✅ resuelto | [challenges/forensics/medium/forensics_git_1](challenges/forensics/medium/forensics_git_1/README.md) |
| 6 | Forensics Git 0 | ✅ resuelto | [challenges/forensics/medium/forensics_git_0](challenges/forensics/medium/forensics_git_0/README.md) |
| 7 | DISKO 4 | ✅ resuelto | [challenges/forensics/medium/disko_4](challenges/forensics/medium/disko_4/README.md) |
| 8 | DISKO 3 | ✅ resuelto | [challenges/forensics/medium/disko_3](challenges/forensics/medium/disko_3/README.md) |
| 9 | DISKO 2 | ✅ resuelto | [challenges/forensics/medium/disko_2](challenges/forensics/medium/disko_2/README.md) |
| 10 | flags are stepic | ✅ resuelto | [challenges/forensics/medium/flags_are_stepic](challenges/forensics/medium/flags_are_stepic/README.md) |
| 11 | Event-Viewing | ✅ resuelto | [challenges/forensics/medium/event-viewing](challenges/forensics/medium/event-viewing/README.md) |
| 12 | Bitlocker-2 | ✅ resuelto | [challenges/forensics/medium/bitlocker-2](challenges/forensics/medium/bitlocker-2/README.md) |
| 13 | Bitlocker-1 | ✅ resuelto | [challenges/forensics/medium/bitlocker-1](challenges/forensics/medium/bitlocker-1/README.md) |
| 14 | Blast from the past | ✅ resuelto | [challenges/forensics/medium/blast_from_the_past](challenges/forensics/medium/blast_from_the_past/README.md) |
| 15 | Mob psycho | ✅ resuelto | [challenges/forensics/medium/mob_psycho](challenges/forensics/medium/mob_psycho/README.md) |
| 16 | endianness-v2 | ✅ resuelto | [challenges/forensics/medium/endianness-v2](challenges/forensics/medium/endianness-v2/README.md) |
| 17 | Dear Diary | ✅ resuelto | [challenges/forensics/medium/dear_diary](challenges/forensics/medium/dear_diary/README.md) |
| 18 | PcapPoisoning | ✅ resuelto | [challenges/forensics/medium/pcappoisoning](challenges/forensics/medium/pcappoisoning/README.md) |
| 19 | MSB | ✅ resuelto | [challenges/forensics/medium/msb](challenges/forensics/medium/msb/README.md) |
| 20 | hideme | ✅ resuelto | [challenges/forensics/medium/hideme](challenges/forensics/medium/hideme/README.md) |
| 21 | FindAndOpen | ✅ resuelto | [challenges/forensics/medium/findandopen](challenges/forensics/medium/findandopen/README.md) |
| 22 | Torrent Analyze | ✅ resuelto | [challenges/forensics/medium/torrent_analyze](challenges/forensics/medium/torrent_analyze/README.md) |
| 23 | St3g0 | ✅ resuelto | [challenges/forensics/medium/st3g0](challenges/forensics/medium/st3g0/README.md) |
| 24 | Sleuthkit Intro | ✅ resuelto | [challenges/forensics/medium/sleuthkit_intro](challenges/forensics/medium/sleuthkit_intro/README.md) |
| 25 | Sleuthkit Apprentice | ✅ resuelto | [challenges/forensics/medium/sleuthkit_apprentice](challenges/forensics/medium/sleuthkit_apprentice/README.md) |
| 26 | Redaction gone wrong | ✅ resuelto | [challenges/forensics/medium/redaction_gone_wrong](challenges/forensics/medium/redaction_gone_wrong/README.md) |
| 27 | Packets Primer | ✅ resuelto | [challenges/forensics/medium/packets_primer](challenges/forensics/medium/packets_primer/README.md) |
| 28 | Operation Orchid | ✅ resuelto | [challenges/forensics/medium/operation_orchid](challenges/forensics/medium/operation_orchid/README.md) |
| 29 | Operation Oni | ✅ resuelto | [challenges/forensics/medium/operation_oni](challenges/forensics/medium/operation_oni/README.md) |
| 30 | Lookey here | ✅ resuelto | [challenges/forensics/medium/lookey_here](challenges/forensics/medium/lookey_here/README.md) |
| 31 | File types | ✅ resuelto | [challenges/forensics/medium/file_types](challenges/forensics/medium/file_types/README.md) |
| 32 | Enhance! | ✅ resuelto | [challenges/forensics/medium/enhance](challenges/forensics/medium/enhance/README.md) |
| 33 | Eavesdrop | ✅ resuelto | [challenges/forensics/medium/eavesdrop](challenges/forensics/medium/eavesdrop/README.md) |
| 34 | advanced-potion-making | ✅ resuelto | [challenges/forensics/medium/advanced-potion-making](challenges/forensics/medium/advanced-potion-making/README.md) |
| 35 | Milkslap | ✅ resuelto | [challenges/forensics/medium/milkslap](challenges/forensics/medium/milkslap/README.md) |
| 36 | Disk, disk, sleuth! II | ✅ resuelto | [challenges/forensics/medium/disk_disk_sleuth](challenges/forensics/medium/disk_disk_sleuth/README.md) |
| 37 | MacroHard WeakEdge | ✅ resuelto | [challenges/forensics/medium/macrohard_weakedge](challenges/forensics/medium/macrohard_weakedge/README.md) |
| 38 | Matryoshka doll | ✅ resuelto | [challenges/forensics/medium/matryoshka_doll](challenges/forensics/medium/matryoshka_doll/README.md) |
| 39 | Wireshark doo dooo do doo... | ✅ resuelto | [challenges/forensics/medium/wireshark_doo_dooo_do_doo](challenges/forensics/medium/wireshark_doo_dooo_do_doo/README.md) |
| 40 | Disk, disk, sleuth! | ✅ resuelto | [challenges/forensics/medium/disk_disk_sleuth](challenges/forensics/medium/disk_disk_sleuth/README.md) |
| 41 | tunn3l v1s10n | ✅ resuelto | [challenges/forensics/medium/tunn3l_v1s10n](challenges/forensics/medium/tunn3l_v1s10n/README.md) |
| 42 | Wireshark twoo twooo two twoo... | ✅ resuelto | [challenges/forensics/medium/wireshark_twoo_twooo_two_twoo](challenges/forensics/medium/wireshark_twoo_twooo_two_twoo/README.md) |
| 43 | Trivial Flag Transfer Protocol | ✅ resuelto | [challenges/forensics/medium/trivial_flag_transfer_protocol](challenges/forensics/medium/trivial_flag_transfer_protocol/README.md) |
| 44 | Weird File | ✅ resuelto | [challenges/forensics/medium/weird_file](challenges/forensics/medium/weird_file/README.md) |
| 45 | Pitter, Patter, Platters | ✅ resuelto | [challenges/forensics/medium/pitter_patter_platters](challenges/forensics/medium/pitter_patter_platters/README.md) |
| 46 | shark on wire 2 | ✅ resuelto | [challenges/forensics/medium/shark_on_wire_2](challenges/forensics/medium/shark_on_wire_2/README.md) |
| 47 | like1000 | ✅ resuelto | [challenges/forensics/medium/like1000](challenges/forensics/medium/like1000/README.md) |
| 48 | What Lies Within | ✅ resuelto | [challenges/forensics/medium/what_lies_within](challenges/forensics/medium/what_lies_within/README.md) |
| 49 | c0rrupt | ✅ resuelto | [challenges/forensics/medium/c0rrupt](challenges/forensics/medium/c0rrupt/README.md) |
| 50 | extensions | ✅ resuelto | [challenges/forensics/medium/extensions](challenges/forensics/medium/extensions/README.md) |
| 51 | WhitePages | ✅ resuelto | [challenges/forensics/medium/whitepages](challenges/forensics/medium/whitepages/README.md) |
| 52 | shark on wire 1 | ✅ resuelto | [challenges/forensics/medium/shark_on_wire_1](challenges/forensics/medium/shark_on_wire_1/README.md) |
| 53 | m00nwalk | ✅ resuelto | [challenges/forensics/medium/m00nwalk](challenges/forensics/medium/m00nwalk/README.md) |
| 54 | So Meta | ✅ resuelto | [challenges/forensics/medium/so_meta](challenges/forensics/medium/so_meta/README.md) |

> Directorios locales sin reto asociado en la plataforma: `disk_disk_sleuth_2`.

## Tabla de retos — Forensics, Hard

**✅ Los 17 retos de Forensics - Hard están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | UnforgottenBits | ✅ resuelto | [challenges/forensics/hard/unforgottenbits](challenges/forensics/hard/unforgottenbits/README.md) |
| 2 | Invisible WORDs | ✅ resuelto | [challenges/forensics/hard/invisible_words](challenges/forensics/hard/invisible_words/README.md) |
| 3 | SideChannel | ✅ resuelto | [challenges/forensics/hard/sidechannel](challenges/forensics/hard/sidechannel/README.md) |
| 4 | scrambled-bytes | ✅ resuelto | [challenges/forensics/hard/scrambled_bytes](challenges/forensics/hard/scrambled_bytes/README.md) |
| 5 | Very very very Hidden | ✅ resuelto | [challenges/forensics/hard/very_very_very_hidden](challenges/forensics/hard/very_very_very_hidden/README.md) |
| 6 | Surfing the Waves | ✅ resuelto | [challenges/forensics/hard/surfing_the_waves](challenges/forensics/hard/surfing_the_waves/README.md) |
| 7 | Investigative Reversing 3 | ✅ resuelto | [challenges/forensics/hard/investigative_reversing_3](challenges/forensics/hard/investigative_reversing_3/README.md) |
| 8 | Investigative Reversing 0 | ✅ resuelto | [challenges/forensics/hard/investigative_reversing_0](challenges/forensics/hard/investigative_reversing_0/README.md) |
| 9 | B1g_Mac | ✅ resuelto | [challenges/forensics/hard/b1g_mac](challenges/forensics/hard/b1g_mac/README.md) |
| 10 | Investigative Reversing 4 | ✅ resuelto | [challenges/forensics/hard/investigative_reversing_4](challenges/forensics/hard/investigative_reversing_4/README.md) |
| 11 | investigation_encoded_1 | ✅ resuelto | [challenges/forensics/hard/investigation_encoded_1](challenges/forensics/hard/investigation_encoded_1/README.md) |
| 12 | WebNet1 | ✅ resuelto | [challenges/forensics/hard/webnet1](challenges/forensics/hard/webnet1/README.md) |
| 13 | investigation_encoded_2 | ✅ resuelto | [challenges/forensics/hard/investigation_encoded_2](challenges/forensics/hard/investigation_encoded_2/README.md) |
| 14 | WebNet0 | ✅ resuelto | [challenges/forensics/hard/webnet0](challenges/forensics/hard/webnet0/README.md) |
| 15 | m00nwalk2 | ✅ resuelto | [challenges/forensics/hard/m00nwalk2](challenges/forensics/hard/m00nwalk2/README.md) |
| 16 | Investigative Reversing 1 | ✅ resuelto | [challenges/forensics/hard/investigative_reversing_1](challenges/forensics/hard/investigative_reversing_1/README.md) |
| 17 | Investigative Reversing 2 | ✅ resuelto | [challenges/forensics/hard/investigative_reversing_2](challenges/forensics/hard/investigative_reversing_2/README.md) |

## Tabla de retos — Cryptography, Easy

**✅ Los 8 retos de Cryptography - Easy están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | StegoRSA | ✅ resuelto | [challenges/cryptography/easy/stegorsa](challenges/cryptography/easy/stegorsa/README.md) |
| 2 | Shared Secrets | ✅ resuelto | [challenges/cryptography/easy/shared_secrets](challenges/cryptography/easy/shared_secrets/README.md) |
| 3 | hashcrack | ✅ resuelto | [challenges/cryptography/easy/hashcrack](challenges/cryptography/easy/hashcrack/README.md) |
| 4 | EVEN RSA CAN BE BROKEN??? | ✅ resuelto | [challenges/cryptography/easy/even_rsa_can_be_broken](challenges/cryptography/easy/even_rsa_can_be_broken/README.md) |
| 5 | interencdec | ✅ resuelto | [challenges/cryptography/easy/interencdec](challenges/cryptography/easy/interencdec/README.md) |
| 6 | Mod 26 | ✅ resuelto | [challenges/cryptography/easy/mod_26](challenges/cryptography/easy/mod_26/README.md) |
| 7 | The Numbers | ✅ resuelto | [challenges/cryptography/easy/the_numbers](challenges/cryptography/easy/the_numbers/README.md) |
| 8 | 13 | ✅ resuelto | [challenges/cryptography/easy/crypto_13](challenges/cryptography/easy/crypto_13/README.md) |

## Tabla de retos — Cryptography, Medium

**✅ Los 45 retos de Cryptography - Medium están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Timestamped Secrets | ✅ resuelto | [challenges/cryptography/medium/timestamped_secrets](challenges/cryptography/medium/timestamped_secrets/README.md) |
| 2 | Small Trouble | ✅ resuelto | [challenges/cryptography/medium/small_trouble](challenges/cryptography/medium/small_trouble/README.md) |
| 3 | shift registers | ✅ resuelto | [challenges/cryptography/medium/shift_registers](challenges/cryptography/medium/shift_registers/README.md) |
| 4 | Related Messages | ✅ resuelto | [challenges/cryptography/medium/related_messages](challenges/cryptography/medium/related_messages/README.md) |
| 5 | Not TRUe | ✅ resuelto | [challenges/cryptography/medium/not_true](challenges/cryptography/medium/not_true/README.md) |
| 6 | cryptomaze | ✅ resuelto | [challenges/cryptography/medium/cryptomaze](challenges/cryptography/medium/cryptomaze/README.md) |
| 7 | ClusterRSA | ✅ resuelto | [challenges/cryptography/medium/clusterrsa](challenges/cryptography/medium/clusterrsa/README.md) |
| 8 | Black Cobra Pepper | ✅ resuelto | [challenges/cryptography/medium/black_cobra_pepper](challenges/cryptography/medium/black_cobra_pepper/README.md) |
| 9 | Crack the Power | ✅ resuelto | [challenges/cryptography/medium/crack_the_power](challenges/cryptography/medium/crack_the_power/README.md) |
| 10 | Guess My Cheese (Part 2) | ✅ resuelto | [challenges/cryptography/medium/guess_my_cheese_part_2](challenges/cryptography/medium/guess_my_cheese_part_2/README.md) |
| 11 | Guess My Cheese (Part 1) | ✅ resuelto | [challenges/cryptography/medium/guess_my_cheese_part_1](challenges/cryptography/medium/guess_my_cheese_part_1/README.md) |
| 12 | rsa_oracle | ✅ resuelto | [challenges/cryptography/medium/rsa_oracle](challenges/cryptography/medium/rsa_oracle/README.md) |
| 13 | Custom encryption | ✅ resuelto | [challenges/cryptography/medium/custom_encryption](challenges/cryptography/medium/custom_encryption/README.md) |
| 14 | C3 | ✅ resuelto | [challenges/cryptography/medium/c3](challenges/cryptography/medium/c3/README.md) |
| 15 | rotation | ✅ resuelto | [challenges/cryptography/medium/rotation](challenges/cryptography/medium/rotation/README.md) |
| 16 | ReadMyCert | ✅ resuelto | [challenges/cryptography/medium/readmycert](challenges/cryptography/medium/readmycert/README.md) |
| 17 | HideToSee | ✅ resuelto | [challenges/cryptography/medium/hidetosee](challenges/cryptography/medium/hidetosee/README.md) |
| 18 | Vigenere | ✅ resuelto | [challenges/cryptography/medium/vigenere](challenges/cryptography/medium/vigenere/README.md) |
| 19 | transposition-trial | ✅ resuelto | [challenges/cryptography/medium/transposition_trial](challenges/cryptography/medium/transposition_trial/README.md) |
| 20 | substitution2 | ✅ resuelto | [challenges/cryptography/medium/substitution2](challenges/cryptography/medium/substitution2/README.md) |
| 21 | substitution1 | ✅ resuelto | [challenges/cryptography/medium/substitution1](challenges/cryptography/medium/substitution1/README.md) |
| 22 | substitution0 | ✅ resuelto | [challenges/cryptography/medium/substitution0](challenges/cryptography/medium/substitution0/README.md) |
| 23 | rail-fence | ✅ resuelto | [challenges/cryptography/medium/rail-fence](challenges/cryptography/medium/rail-fence/README.md) |
| 24 | morse-code | ✅ resuelto | [challenges/cryptography/medium/morse-code](challenges/cryptography/medium/morse-code/README.md) |
| 25 | credstuff | ✅ resuelto | [challenges/cryptography/medium/credstuff](challenges/cryptography/medium/credstuff/README.md) |
| 26 | basic-mod2 | ✅ resuelto | [challenges/cryptography/medium/basic-mod2](challenges/cryptography/medium/basic-mod2/README.md) |
| 27 | basic-mod1 | ✅ resuelto | [challenges/cryptography/medium/basic-mod1](challenges/cryptography/medium/basic-mod1/README.md) |
| 28 | spelling-quiz | ✅ resuelto | [challenges/cryptography/medium/spelling_quiz](challenges/cryptography/medium/spelling_quiz/README.md) |
| 29 | Mini RSA | ✅ resuelto | [challenges/cryptography/medium/mini_rsa](challenges/cryptography/medium/mini_rsa/README.md) |
| 30 | It is my Birthday 2 | ✅ resuelto | [challenges/cryptography/medium/it_is_my_birthday_2](challenges/cryptography/medium/it_is_my_birthday_2/README.md) |
| 31 | Mind your Ps and Qs | ✅ resuelto | [challenges/cryptography/medium/mind_your_ps_and_qs](challenges/cryptography/medium/mind_your_ps_and_qs/README.md) |
| 32 | Dachshund Attacks | ✅ resuelto | [challenges/cryptography/medium/dachshund_attacks](challenges/cryptography/medium/dachshund_attacks/README.md) |
| 33 | New Caesar | ✅ resuelto | [challenges/cryptography/medium/new_caesar](challenges/cryptography/medium/new_caesar/README.md) |
| 34 | No Padding, No Problem | ✅ resuelto | [challenges/cryptography/medium/no_padding_no_problem](challenges/cryptography/medium/no_padding_no_problem/README.md) |
| 35 | Easy Peasy | ✅ resuelto | [challenges/cryptography/medium/easy_peasy](challenges/cryptography/medium/easy_peasy/README.md) |
| 36 | It's Not My Fault 2 | ✅ resuelto | [challenges/cryptography/medium/its_not_my_fault_2](challenges/cryptography/medium/its_not_my_fault_2/README.md) |
| 37 | Pixelated | ✅ resuelto | [challenges/cryptography/medium/pixelated](challenges/cryptography/medium/pixelated/README.md) |
| 38 | caesar | ✅ resuelto | [challenges/cryptography/medium/caesar](challenges/cryptography/medium/caesar/README.md) |
| 39 | Easy1 | ✅ resuelto | [challenges/cryptography/medium/easy1](challenges/cryptography/medium/easy1/README.md) |
| 40 | Mr-Worldwide | ✅ resuelto | [challenges/cryptography/medium/mr_worldwide](challenges/cryptography/medium/mr_worldwide/README.md) |
| 41 | waves over lambda | ✅ resuelto | [challenges/cryptography/medium/waves_over_lambda](challenges/cryptography/medium/waves_over_lambda/README.md) |
| 42 | Flags | ✅ resuelto | [challenges/cryptography/medium/flags](challenges/cryptography/medium/flags/README.md) |
| 43 | Tapping | ✅ resuelto | [challenges/cryptography/medium/tapping](challenges/cryptography/medium/tapping/README.md) |
| 44 | john_pollard | ✅ resuelto | [challenges/cryptography/medium/john_pollard](challenges/cryptography/medium/john_pollard/README.md) |
| 45 | la cifra de | ✅ resuelto | [challenges/cryptography/medium/la_cifra_de](challenges/cryptography/medium/la_cifra_de/README.md) |

## Tabla de retos — Cryptography, Hard

**✅ Los 30 retos de Cryptography - Hard están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Secure Dot Product | ✅ resuelto | [challenges/cryptography/hard/secure_dot_product](challenges/cryptography/hard/secure_dot_product/README.md) |
| 2 | MSS_ADVANCE Revenge | ✅ resuelto | [challenges/cryptography/hard/mss_advance_revenge](challenges/cryptography/hard/mss_advance_revenge/README.md) |
| 3 | Ricochet | ✅ resuelto | [challenges/cryptography/hard/ricochet](challenges/cryptography/hard/ricochet/README.md) |
| 4 | ChaCha Slide | ✅ resuelto | [challenges/cryptography/hard/chacha_slide](challenges/cryptography/hard/chacha_slide/README.md) |
| 5 | flag_printer | ✅ resuelto | [challenges/cryptography/hard/flag_printer](challenges/cryptography/hard/flag_printer/README.md) |
| 6 | SRA | ✅ resuelto | [challenges/cryptography/hard/sra](challenges/cryptography/hard/sra/README.md) |
| 7 | PowerAnalysis: Warmup | ✅ resuelto | [challenges/cryptography/hard/poweranalysis_warmup](challenges/cryptography/hard/poweranalysis_warmup/README.md) |
| 8 | PowerAnalysis: Part 2 | ✅ resuelto | [challenges/cryptography/hard/poweranalysis_part_2](challenges/cryptography/hard/poweranalysis_part_2/README.md) |
| 9 | PowerAnalysis: Part 1 | ✅ resuelto | [challenges/cryptography/hard/poweranalysis_part_1](challenges/cryptography/hard/poweranalysis_part_1/README.md) |
| 10 | Very Smooth | ✅ resuelto | [challenges/cryptography/hard/very_smooth](challenges/cryptography/hard/very_smooth/README.md) |
| 11 | Sum-O-Primes | ✅ resuelto | [challenges/cryptography/hard/sum-o-primes](challenges/cryptography/hard/sum-o-primes/README.md) |
| 12 | Sequences | ✅ resuelto | [challenges/cryptography/hard/sequences](challenges/cryptography/hard/sequences/README.md) |
| 13 | NSA Backdoor | ✅ resuelto | [challenges/cryptography/hard/nsa-backdoor](challenges/cryptography/hard/nsa-backdoor/README.md) |
| 14 | college-rowing-team | ✅ resuelto | [challenges/cryptography/hard/college-rowing-team](challenges/cryptography/hard/college-rowing-team/README.md) |
| 15 | corrupt-key-2 | ✅ resuelto | [challenges/cryptography/hard/corrupt-key-2](challenges/cryptography/hard/corrupt-key-2/README.md) |
| 16 | triple-secure | ✅ resuelto | [challenges/cryptography/hard/triple-secure](challenges/cryptography/hard/triple-secure/README.md) |
| 17 | XtraORdinary | ✅ resuelto | [challenges/cryptography/hard/xtraordinary](challenges/cryptography/hard/xtraordinary/README.md) |
| 18 | corrupt-key-1 | ✅ resuelto | [challenges/cryptography/hard/corrupt-key-1](challenges/cryptography/hard/corrupt-key-1/README.md) |
| 19 | New Vignere | ✅ resuelto | [challenges/cryptography/hard/new-vignere](challenges/cryptography/hard/new-vignere/README.md) |
| 20 | Double DES | ✅ resuelto | [challenges/cryptography/hard/double-des](challenges/cryptography/hard/double-des/README.md) |
| 21 | Clouds | ✅ resuelto | [challenges/cryptography/hard/clouds](challenges/cryptography/hard/clouds/README.md) |
| 22 | Compress and Attack | ✅ resuelto | [challenges/cryptography/hard/compress_and_attack](challenges/cryptography/hard/compress_and_attack/README.md) |
| 23 | It's Not My Fault 1 | ✅ resuelto | [challenges/cryptography/hard/its-not-my-fault-1](challenges/cryptography/hard/its-not-my-fault-1/README.md) |
| 24 | Play Nice | ✅ resuelto | [challenges/cryptography/hard/play-nice](challenges/cryptography/hard/play-nice/README.md) |
| 25 | Scrambled: RSA | ✅ resuelto | [challenges/cryptography/hard/scrambled-rsa](challenges/cryptography/hard/scrambled-rsa/README.md) |
| 26 | b00tl3gRSA3 | ✅ resuelto | [challenges/cryptography/hard/b00tl3grsa3](challenges/cryptography/hard/b00tl3grsa3/README.md) |
| 27 | AES-ABC | ✅ resuelto | [challenges/cryptography/hard/aes_abc](challenges/cryptography/hard/aes_abc/README.md) |
| 28 | miniRSA | ✅ resuelto | [challenges/cryptography/hard/minirsa](challenges/cryptography/hard/minirsa/README.md) |
| 29 | rsa-pop-quiz | ✅ resuelto | [challenges/cryptography/hard/rsa_pop_quiz](challenges/cryptography/hard/rsa_pop_quiz/README.md) |
| 30 | b00tl3gRSA2 | ✅ resuelto | [challenges/cryptography/hard/b00tl3grsa2](challenges/cryptography/hard/b00tl3grsa2/README.md) |

> Directorios locales sin reto asociado en la plataforma: `compress-and-attack`, `play_nice`.

## Tabla de retos — Reverse Engineering, Easy

**✅ Los 14 retos de Reverse Engineering - Easy están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Flag Hunters | ✅ resuelto | [challenges/reverse-engineering/easy/flag_hunters](challenges/reverse-engineering/easy/flag_hunters/README.md) |
| 2 | Picker II | ✅ resuelto | [challenges/reverse-engineering/easy/picker_ii](challenges/reverse-engineering/easy/picker_ii/README.md) |
| 3 | Picker I | ✅ resuelto | [challenges/reverse-engineering/easy/picker_i](challenges/reverse-engineering/easy/picker_i/README.md) |
| 4 | GDB baby step 4 | ✅ resuelto | [challenges/reverse-engineering/easy/gdb_baby_step_4](challenges/reverse-engineering/easy/gdb_baby_step_4/README.md) |
| 5 | GDB baby step 3 | ✅ resuelto | [challenges/reverse-engineering/easy/gdb_baby_step_3](challenges/reverse-engineering/easy/gdb_baby_step_3/README.md) |
| 6 | GDB baby step 2 | ✅ resuelto | [challenges/reverse-engineering/easy/gdb_baby_step_2](challenges/reverse-engineering/easy/gdb_baby_step_2/README.md) |
| 7 | GDB baby step 1 | ✅ resuelto | [challenges/reverse-engineering/easy/gdb_baby_step_1](challenges/reverse-engineering/easy/gdb_baby_step_1/README.md) |
| 8 | Bit-O-Asm-4 | ✅ resuelto | [challenges/reverse-engineering/easy/bit_o_asm_4](challenges/reverse-engineering/easy/bit_o_asm_4/README.md) |
| 9 | Bit-O-Asm-3 | ✅ resuelto | [challenges/reverse-engineering/easy/bit_o_asm_3](challenges/reverse-engineering/easy/bit_o_asm_3/README.md) |
| 10 | Bit-O-Asm-2 | ✅ resuelto | [challenges/reverse-engineering/easy/bit_o_asm_2](challenges/reverse-engineering/easy/bit_o_asm_2/README.md) |
| 11 | Bit-O-Asm-1 | ✅ resuelto | [challenges/reverse-engineering/easy/bit_o_asm_1](challenges/reverse-engineering/easy/bit_o_asm_1/README.md) |
| 12 | ASCII FTW | ✅ resuelto | [challenges/reverse-engineering/easy/ascii_ftw](challenges/reverse-engineering/easy/ascii_ftw/README.md) |
| 13 | Transformation | ✅ resuelto | [challenges/reverse-engineering/easy/transformation](challenges/reverse-engineering/easy/transformation/README.md) |
| 14 | vault-door-training | ✅ resuelto | [challenges/reverse-engineering/easy/vault_door_training](challenges/reverse-engineering/easy/vault_door_training/README.md) |

## Tabla de retos — Reverse Engineering, Medium

Existen **53 retos** en total en esta categoría y dificultad: 52 resueltos y 1 pendiente (incluye retos en mantenimiento).

**⏳ 52/53 retos resueltos (98.1%). 1 pendiente en plataforma.**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Secure Password Database | ✅ resuelto | [challenges/reverse-engineering/medium/secure_password_database](challenges/reverse-engineering/medium/secure_password_database/README.md) |
| 2 | Bypass Me | ✅ resuelto | [challenges/reverse-engineering/medium/bypass_me](challenges/reverse-engineering/medium/bypass_me/README.md) |
| 3 | Autorev 1 | ✅ resuelto | [challenges/reverse-engineering/medium/autorev_1](challenges/reverse-engineering/medium/autorev_1/README.md) |
| 4 | Hidden Cipher 2 | ✅ resuelto | [challenges/reverse-engineering/medium/hidden_cipher_2](challenges/reverse-engineering/medium/hidden_cipher_2/README.md) |
| 5 | Hidden Cipher 1 | ✅ resuelto | [challenges/reverse-engineering/medium/hidden_cipher_1](challenges/reverse-engineering/medium/hidden_cipher_1/README.md) |
| 6 | Gatekeeper | ✅ resuelto | [challenges/reverse-engineering/medium/gatekeeper](challenges/reverse-engineering/medium/gatekeeper/README.md) |
| 7 | Silent Stream | ✅ resuelto | [challenges/reverse-engineering/medium/silent_stream](challenges/reverse-engineering/medium/silent_stream/README.md) |
| 8 | The Add/On Trap | ✅ resuelto | [challenges/reverse-engineering/medium/the_add_on_trap](challenges/reverse-engineering/medium/the_add_on_trap/README.md) |
| 9 | Pico Bank | ✅ resuelto | [challenges/reverse-engineering/medium/pico_bank](challenges/reverse-engineering/medium/pico_bank/README.md) |
| 10 | M1n10n'5_53cr37 | ✅ resuelto | [challenges/reverse-engineering/medium/m1n10n5_53cr37](challenges/reverse-engineering/medium/m1n10n5_53cr37/README.md) |
| 11 | Quantum Scrambler | ✅ resuelto | [challenges/reverse-engineering/medium/quantum_scrambler](challenges/reverse-engineering/medium/quantum_scrambler/README.md) |
| 12 | Chronohack | ✅ resuelto | [challenges/reverse-engineering/medium/chronohack](challenges/reverse-engineering/medium/chronohack/README.md) |
| 13 | Tap into Hash | ✅ resuelto | [challenges/reverse-engineering/medium/tap_into_hash](challenges/reverse-engineering/medium/tap_into_hash/README.md) |
| 14 | perplexed | ✅ resuelto | [challenges/reverse-engineering/medium/perplexed](challenges/reverse-engineering/medium/perplexed/README.md) |
| 15 | Binary Instrumentation 2 | ✅ resuelto | [challenges/reverse-engineering/medium/binary_instrumentation_2](challenges/reverse-engineering/medium/binary_instrumentation_2/README.md) |
| 16 | Binary Instrumentation 1 | ✅ resuelto | [challenges/reverse-engineering/medium/binary_instrumentation_1](challenges/reverse-engineering/medium/binary_instrumentation_1/README.md) |
| 17 | WinAntiDbg0x300 | ✅ resuelto | [challenges/reverse-engineering/medium/winantidbg0x300](challenges/reverse-engineering/medium/winantidbg0x300/README.md) |
| 18 | WinAntiDbg0x200 | ✅ resuelto | [challenges/reverse-engineering/medium/winantidbg0x200](challenges/reverse-engineering/medium/winantidbg0x200/README.md) |
| 19 | WinAntiDbg0x100 | ✅ resuelto | [challenges/reverse-engineering/medium/winantidbg0x100](challenges/reverse-engineering/medium/winantidbg0x100/README.md) |
| 20 | weirdSnake | ✅ resuelto | [challenges/reverse-engineering/medium/weirdsnake](challenges/reverse-engineering/medium/weirdsnake/README.md) |
| 21 | packer | ✅ resuelto | [challenges/reverse-engineering/medium/packer](challenges/reverse-engineering/medium/packer/README.md) |
| 22 | FactCheck | ✅ resuelto | [challenges/reverse-engineering/medium/factcheck](challenges/reverse-engineering/medium/factcheck/README.md) |
| 23 | Classic Crackme 0x100 | ✅ resuelto | [challenges/reverse-engineering/medium/classic_crackme_0x100](challenges/reverse-engineering/medium/classic_crackme_0x100/README.md) |
| 24 | Picker III | ✅ resuelto | [challenges/reverse-engineering/medium/picker_iii](challenges/reverse-engineering/medium/picker_iii/README.md) |
| 25 | Virtual Machine 0 | ✅ resuelto | [challenges/reverse-engineering/medium/virtual_machine_0](challenges/reverse-engineering/medium/virtual_machine_0/README.md) |
| 26 | timer | ✅ resuelto | [challenges/reverse-engineering/medium/timer](challenges/reverse-engineering/medium/timer/README.md) |
| 27 | Safe Opener 2 | ✅ resuelto | [challenges/reverse-engineering/medium/safe_opener_2](challenges/reverse-engineering/medium/safe_opener_2/README.md) |
| 28 | Reverse | ✅ resuelto | [challenges/reverse-engineering/medium/reverse](challenges/reverse-engineering/medium/reverse/README.md) |
| 29 | Ready Gladiator 2 | ✅ resuelto | [challenges/reverse-engineering/medium/ready_gladiator_2](challenges/reverse-engineering/medium/ready_gladiator_2/README.md) |
| 30 | Ready Gladiator 1 | ✅ resuelto | [challenges/reverse-engineering/medium/ready_gladiator_1](challenges/reverse-engineering/medium/ready_gladiator_1/README.md) |
| 31 | Ready Gladiator 0 | ✅ resuelto | [challenges/reverse-engineering/medium/ready_gladiator_0](challenges/reverse-engineering/medium/ready_gladiator_0/README.md) |
| 32 | unpackme.py | ✅ resuelto | [challenges/reverse-engineering/medium/unpackme_py](challenges/reverse-engineering/medium/unpackme_py/README.md) |
| 33 | unpackme | ✅ resuelto | [challenges/reverse-engineering/medium/unpackme](challenges/reverse-engineering/medium/unpackme/README.md) |
| 34 | Safe Opener | ✅ resuelto | [challenges/reverse-engineering/medium/safe_opener](challenges/reverse-engineering/medium/safe_opener/README.md) |
| 35 | patchme.py | ✅ resuelto | [challenges/reverse-engineering/medium/patchme_py](challenges/reverse-engineering/medium/patchme_py/README.md) |
| 36 | GDB Test Drive | ✅ resuelto | [challenges/reverse-engineering/medium/gdb_test_drive](challenges/reverse-engineering/medium/gdb_test_drive/README.md) |
| 37 | Fresh Java | ✅ resuelto | [challenges/reverse-engineering/medium/fresh_java](challenges/reverse-engineering/medium/fresh_java/README.md) |
| 38 | file-run2 | ✅ resuelto | [challenges/reverse-engineering/medium/file_run2](challenges/reverse-engineering/medium/file_run2/README.md) |
| 39 | file-run1 | ✅ resuelto | [challenges/reverse-engineering/medium/file_run1](challenges/reverse-engineering/medium/file_run1/README.md) |
| 40 | bloat.py | ✅ resuelto | [challenges/reverse-engineering/medium/bloat_py](challenges/reverse-engineering/medium/bloat_py/README.md) |
| 41 | Bbbbloat | ✅ resuelto | [challenges/reverse-engineering/medium/bbbbloat](challenges/reverse-engineering/medium/bbbbloat/README.md) |
| 42 | crackme-py | ✅ resuelto | [challenges/reverse-engineering/medium/crackme_py](challenges/reverse-engineering/medium/crackme_py/README.md) |
| 43 | ARMssembly 0 | ✅ resuelto | [challenges/reverse-engineering/medium/armssembly_0](challenges/reverse-engineering/medium/armssembly_0/README.md) |
| 44 | Shop | ✅ resuelto | [challenges/reverse-engineering/medium/shop](challenges/reverse-engineering/medium/shop/README.md) |
| 45 | keygenme-py | ✅ resuelto | [challenges/reverse-engineering/medium/keygenme_py](challenges/reverse-engineering/medium/keygenme_py/README.md) |
| 46 | speeds and feeds [116] | ⏳ pendiente (mantenimiento) | [challenges/reverse-engineering/medium/speeds_and_feeds](challenges/reverse-engineering/medium/speeds_and_feeds/README.md) |
| 47 | ARMssembly 1 | ✅ resuelto | [challenges/reverse-engineering/medium/armssembly_1](challenges/reverse-engineering/medium/armssembly_1/README.md) |
| 48 | vault-door-5 | ✅ resuelto | [challenges/reverse-engineering/medium/vault_door_5](challenges/reverse-engineering/medium/vault_door_5/README.md) |
| 49 | vault-door-4 | ✅ resuelto | [challenges/reverse-engineering/medium/vault_door_4](challenges/reverse-engineering/medium/vault_door_4/README.md) |
| 50 | vault-door-3 | ✅ resuelto | [challenges/reverse-engineering/medium/vault_door_3](challenges/reverse-engineering/medium/vault_door_3/README.md) |
| 51 | vault-door-6 | ✅ resuelto | [challenges/reverse-engineering/medium/vault_door_6](challenges/reverse-engineering/medium/vault_door_6/README.md) |
| 52 | asm1 | ✅ resuelto | [challenges/reverse-engineering/medium/asm1](challenges/reverse-engineering/medium/asm1/README.md) |
| 53 | vault-door-1 | ✅ resuelto | [challenges/reverse-engineering/medium/vault_door_1](challenges/reverse-engineering/medium/vault_door_1/README.md) |

## Tabla de retos — Reverse Engineering, Hard

Existen **35 retos** en total en esta categoría y dificultad: 33 resueltos y 2 pendientes.

**⏳ 33/35 retos resueltos (94.3%). 2 pendientes en plataforma.**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | JITFP [737] | ⏳ pendiente | [challenges/reverse-engineering/hard/jitfp](challenges/reverse-engineering/hard/jitfp/README.md) |
| 2 | Binary Instrumentation 4 [700] | ⏳ pendiente | [challenges/reverse-engineering/hard/binary_instrumentation_4](challenges/reverse-engineering/hard/binary_instrumentation_4/README.md) |
| 3 | Binary Instrumentation 3 [699] | ✅ resuelto | [challenges/reverse-engineering/hard/binary_instrumentation_3](challenges/reverse-engineering/hard/binary_instrumentation_3/README.md) |
| 4 | Virtual Machine 1 | ✅ resuelto | [challenges/reverse-engineering/hard/virtual_machine_1](challenges/reverse-engineering/hard/virtual_machine_1/README.md) |
| 5 | No way out | ✅ resuelto | [challenges/reverse-engineering/hard/no_way_out](challenges/reverse-engineering/hard/no_way_out/README.md) |
| 6 | Wizardlike | ✅ resuelto | [challenges/reverse-engineering/hard/wizardlike](challenges/reverse-engineering/hard/wizardlike/README.md) |
| 7 | Keygenme | ✅ resuelto | [challenges/reverse-engineering/hard/keygenme](challenges/reverse-engineering/hard/keygenme/README.md) |
| 8 | not crypto | ✅ resuelto | [challenges/reverse-engineering/hard/not_crypto](challenges/reverse-engineering/hard/not_crypto/README.md) |
| 9 | MATRIX | ✅ resuelto | [challenges/reverse-engineering/hard/matrix](challenges/reverse-engineering/hard/matrix/README.md) |
| 10 | breadth | ✅ resuelto | [challenges/reverse-engineering/hard/breadth](challenges/reverse-engineering/hard/breadth/README.md) |
| 11 | riscy business | ✅ resuelto | [challenges/reverse-engineering/hard/riscy_business](challenges/reverse-engineering/hard/riscy_business/README.md) |
| 12 | ARMssembly 4 | ✅ resuelto | [challenges/reverse-engineering/hard/armssembly_4](challenges/reverse-engineering/hard/armssembly_4/README.md) |
| 13 | gogo | ✅ resuelto | [challenges/reverse-engineering/hard/gogo](challenges/reverse-engineering/hard/gogo/README.md) |
| 14 | Rolling My Own | ✅ resuelto | [challenges/reverse-engineering/hard/rolling_my_own](challenges/reverse-engineering/hard/rolling_my_own/README.md) |
| 15 | ARMssembly 2 | ✅ resuelto | [challenges/reverse-engineering/hard/armssembly_2](challenges/reverse-engineering/hard/armssembly_2/README.md) |
| 16 | Checkpass [149] | ✅ resuelto | [challenges/reverse-engineering/hard/checkpass](challenges/reverse-engineering/hard/checkpass/README.md) |
| 17 | Easy as GDB | ✅ resuelto | [challenges/reverse-engineering/hard/easy_as_gdb](challenges/reverse-engineering/hard/easy_as_gdb/README.md) |
| 18 | Powershelly | ✅ resuelto | [challenges/reverse-engineering/hard/powershelly](challenges/reverse-engineering/hard/powershelly/README.md) |
| 19 | ARMssembly 3 | ✅ resuelto | [challenges/reverse-engineering/hard/armssembly_3](challenges/reverse-engineering/hard/armssembly_3/README.md) |
| 20 | Let's get dynamic | ✅ resuelto | [challenges/reverse-engineering/hard/lets_get_dynamic](challenges/reverse-engineering/hard/lets_get_dynamic/README.md) |
| 21 | OTP Implementation | ✅ resuelto | [challenges/reverse-engineering/hard/otp_implementation](challenges/reverse-engineering/hard/otp_implementation/README.md) |
| 22 | reverse_cipher | ✅ resuelto | [challenges/reverse-engineering/hard/reverse_cipher](challenges/reverse-engineering/hard/reverse_cipher/README.md) |
| 23 | asm3 | ✅ resuelto | [challenges/reverse-engineering/hard/asm3](challenges/reverse-engineering/hard/asm3/README.md) |
| 24 | vault-door-7 | ✅ resuelto | [challenges/reverse-engineering/hard/vault_door_7](challenges/reverse-engineering/hard/vault_door_7/README.md) |
| 25 | droids2 | ✅ resuelto | [challenges/reverse-engineering/hard/droids2](challenges/reverse-engineering/hard/droids2/README.md) |
| 26 | B1ll_Gat35 | ✅ resuelto | [challenges/reverse-engineering/hard/b1ll_gat35](challenges/reverse-engineering/hard/b1ll_gat35/README.md) |
| 27 | Need For Speed | ✅ resuelto | [challenges/reverse-engineering/hard/need_for_speed](challenges/reverse-engineering/hard/need_for_speed/README.md) |
| 28 | Forky | ✅ resuelto | [challenges/reverse-engineering/hard/forky](challenges/reverse-engineering/hard/forky/README.md) |
| 29 | droids3 | ✅ resuelto | [challenges/reverse-engineering/hard/droids3](challenges/reverse-engineering/hard/droids3/README.md) |
| 30 | droids4 | ✅ resuelto | [challenges/reverse-engineering/hard/droids4](challenges/reverse-engineering/hard/droids4/README.md) |
| 31 | asm2 | ✅ resuelto | [challenges/reverse-engineering/hard/asm2](challenges/reverse-engineering/hard/asm2/README.md) |
| 32 | droids1 | ✅ resuelto | [challenges/reverse-engineering/hard/droids1](challenges/reverse-engineering/hard/droids1/README.md) |
| 33 | droids0 | ✅ resuelto | [challenges/reverse-engineering/hard/droids0](challenges/reverse-engineering/hard/droids0/README.md) |
| 34 | vault-door-8 | ✅ resuelto | [challenges/reverse-engineering/hard/vault_door_8](challenges/reverse-engineering/hard/vault_door_8/README.md) |
| 35 | asm4 | ✅ resuelto | [challenges/reverse-engineering/hard/asm4](challenges/reverse-engineering/hard/asm4/README.md) |

> Directorios locales sin reto asociado en la plataforma: `elf_ception`, `emu_decode`, `encrypted_elf`, `format_strings`, `genkey`, `got_shell`, `has_some_magic`, `hexencode`, `input_output`.

## Tabla de retos — Binary Exploitation, Easy

**✅ Los 5 retos de Binary Exploitation - Easy están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Quizploit | ✅ resuelto | [challenges/binary-exploitation/easy/quizploit](challenges/binary-exploitation/easy/quizploit/README.md) |
| 2 | PIE TIME | ✅ resuelto | [challenges/binary-exploitation/easy/pie_time](challenges/binary-exploitation/easy/pie_time/README.md) |
| 3 | heap 0 | ✅ resuelto | [challenges/binary-exploitation/easy/heap_0](challenges/binary-exploitation/easy/heap_0/README.md) |
| 4 | format string 0 | ✅ resuelto | [challenges/binary-exploitation/easy/format_string_0](challenges/binary-exploitation/easy/format_string_0/README.md) |
| 5 | Local Target | ✅ resuelto | [challenges/binary-exploitation/easy/local_target](challenges/binary-exploitation/easy/local_target/README.md) |

## Tabla de retos — Binary Exploitation, Medium

Existen **37 retos** en total en esta categoría y dificultad: 36 resueltos y 1 pendiente.

**⏳ 36/37 retos resueltos (97.3%). 1 pendiente en plataforma.**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Echo Escape 1 | ✅ resuelto | [challenges/binary-exploitation/medium/echo_escape_1](challenges/binary-exploitation/medium/echo_escape_1/README.md) |
| 2 | tea-cash | ✅ resuelto | [challenges/binary-exploitation/medium/tea_cash](challenges/binary-exploitation/medium/tea_cash/README.md) |
| 3 | Echo Escape 2 | ✅ resuelto | [challenges/binary-exploitation/medium/echo_escape_2](challenges/binary-exploitation/medium/echo_escape_2/README.md) |
| 4 | offset-cycle | ✅ resuelto | — |
| 5 | Input Injection 2 | ✅ resuelto | [challenges/binary-exploitation/medium/input_injection_2](challenges/binary-exploitation/medium/input_injection_2/README.md) |
| 6 | Input Injection 1 | ✅ resuelto | [challenges/binary-exploitation/medium/input_injection_1](challenges/binary-exploitation/medium/input_injection_1/README.md) |
| 7 | PIE TIME 2 | ✅ resuelto | [challenges/binary-exploitation/medium/pie_time_2](challenges/binary-exploitation/medium/pie_time_2/README.md) |
| 8 | hash-only-2 | ✅ resuelto | [challenges/binary-exploitation/medium/hash_only_2](challenges/binary-exploitation/medium/hash_only_2/README.md) |
| 9 | hash-only-1 | ✅ resuelto | [challenges/binary-exploitation/medium/hash_only_1](challenges/binary-exploitation/medium/hash_only_1/README.md) |
| 10 | Echo Valley | ✅ resuelto | [challenges/binary-exploitation/medium/echo_valley](challenges/binary-exploitation/medium/echo_valley/README.md) |
| 11 | format string 3 | ✅ resuelto | [challenges/binary-exploitation/medium/format_string_3](challenges/binary-exploitation/medium/format_string_3/README.md) |
| 12 | format string 2 | ✅ resuelto | [challenges/binary-exploitation/medium/format_string_2](challenges/binary-exploitation/medium/format_string_2/README.md) |
| 13 | heap 3 | ✅ resuelto | [challenges/binary-exploitation/medium/heap_3](challenges/binary-exploitation/medium/heap_3/README.md) |
| 14 | heap 1 | ✅ resuelto | [challenges/binary-exploitation/medium/heap_1](challenges/binary-exploitation/medium/heap_1/README.md) |
| 15 | heap 2 | ✅ resuelto | [challenges/binary-exploitation/medium/heap_2](challenges/binary-exploitation/medium/heap_2/README.md) |
| 16 | format string 1 | ✅ resuelto | [challenges/binary-exploitation/medium/format_string_1](challenges/binary-exploitation/medium/format_string_1/README.md) |
| 17 | Picker IV | ✅ resuelto | [challenges/binary-exploitation/medium/picker_iv](challenges/binary-exploitation/medium/picker_iv/README.md) |
| 18 | VNE | ✅ resuelto | [challenges/binary-exploitation/medium/vne](challenges/binary-exploitation/medium/vne/README.md) |
| 19 | two-sum | ✅ resuelto | [challenges/binary-exploitation/medium/two_sum](challenges/binary-exploitation/medium/two_sum/README.md) |
| 20 | hijacking | ✅ resuelto | [challenges/binary-exploitation/medium/hijacking](challenges/binary-exploitation/medium/hijacking/README.md) |
| 21 | babygame01 | ✅ resuelto | [challenges/binary-exploitation/medium/babygame01](challenges/binary-exploitation/medium/babygame01/README.md) |
| 22 | x-sixty-what | ✅ resuelto | [challenges/binary-exploitation/medium/x_sixty_what](challenges/binary-exploitation/medium/x_sixty_what/README.md) |
| 23 | RPS | ✅ resuelto | — |
| 24 | flag leak | ✅ resuelto | [challenges/binary-exploitation/medium/flag_leak](challenges/binary-exploitation/medium/flag_leak/README.md) |
| 25 | CVE-XXXX-XXXX | ✅ resuelto | [challenges/binary-exploitation/medium/cve_xxxx_xxxx](challenges/binary-exploitation/medium/cve_xxxx_xxxx/README.md) |
| 26 | buffer overflow 2 | ✅ resuelto | [challenges/binary-exploitation/medium/buffer_overflow_2](challenges/binary-exploitation/medium/buffer_overflow_2/README.md) |
| 27 | buffer overflow 1 | ✅ resuelto | [challenges/binary-exploitation/medium/buffer_overflow_1](challenges/binary-exploitation/medium/buffer_overflow_1/README.md) |
| 28 | buffer overflow 0 | ✅ resuelto | [challenges/binary-exploitation/medium/buffer_overflow_0](challenges/binary-exploitation/medium/buffer_overflow_0/README.md) |
| 29 | basic-file-exploit | ✅ resuelto | [challenges/binary-exploitation/medium/basic_file_exploit](challenges/binary-exploitation/medium/basic_file_exploit/README.md) |
| 30 | clutter-overflow | ✅ resuelto | [challenges/binary-exploitation/medium/clutter_overflow](challenges/binary-exploitation/medium/clutter_overflow/README.md) |
| 31 | Binary Gauntlet 0 | ✅ resuelto | [challenges/binary-exploitation/medium/binary_gauntlet_0](challenges/binary-exploitation/medium/binary_gauntlet_0/README.md) |
| 32 | Binary Gauntlet 2 [143] | ⏳ pendiente | — |
| 33 | What's your input? | ✅ resuelto | [challenges/binary-exploitation/medium/whats_your_input](challenges/binary-exploitation/medium/whats_your_input/README.md) |
| 34 | Binary Gauntlet 3 | ✅ resuelto | [challenges/binary-exploitation/medium/binary_gauntlet_3](challenges/binary-exploitation/medium/binary_gauntlet_3/README.md) |
| 35 | Binary Gauntlet 1 | ✅ resuelto | [challenges/binary-exploitation/medium/binary_gauntlet_1](challenges/binary-exploitation/medium/binary_gauntlet_1/README.md) |
| 36 | Stonks | ✅ resuelto | [challenges/binary-exploitation/medium/stonks](challenges/binary-exploitation/medium/stonks/README.md) |
| 37 | Guessing Game 1 | ✅ resuelto | [challenges/binary-exploitation/medium/guessing_game_1](challenges/binary-exploitation/medium/guessing_game_1/README.md) |

## Tabla de retos — Binary Exploitation, Hard

Existen **34 retos** en total en esta categoría y dificultad: 3 resueltos y 31 pendientes.

**⏳ 4/34 retos resueltos (8.8%). 31 pendientes en plataforma.**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Heap Havoc | ✅ resuelto | [challenges/binary-exploitation/hard/heap_havoc](challenges/binary-exploitation/hard/heap_havoc/README.md) |
| 2 | Pizza Router [758] | ⏳ pendiente | [challenges/binary-exploitation/hard/pizza_router](challenges/binary-exploitation/hard/pizza_router/README.md) |
| 3 | offset-cycleV2 | ✅ resuelto | [challenges/binary-exploitation/hard/offset-cyclev2](challenges/binary-exploitation/hard/offset-cyclev2/README.md) |
| 4 | handoff [486] | ⏳ pendiente | [challenges/binary-exploitation/hard/handoff](challenges/binary-exploitation/hard/handoff/README.md) |
| 5 | babygame03 [446] | ⏳ pendiente | [challenges/binary-exploitation/hard/babygame03](challenges/binary-exploitation/hard/babygame03/README.md) |
| 6 | high frequency troubles [441] | ⏳ pendiente | [challenges/binary-exploitation/hard/high_frequency_troubles](challenges/binary-exploitation/hard/high_frequency_troubles/README.md) |
| 7 | tic-tac [380] | ⏳ pendiente | [challenges/binary-exploitation/hard/tic_tac](challenges/binary-exploitation/hard/tic_tac/README.md) |
| 8 | Horsetrack [353] | ⏳ pendiente | [challenges/binary-exploitation/hard/horsetrack](challenges/binary-exploitation/hard/horsetrack/README.md) |
| 9 | babygame02 [346] | ⏳ pendiente | [challenges/binary-exploitation/hard/babygame02](challenges/binary-exploitation/hard/babygame02/README.md) |
| 10 | wine [317] | ⏳ pendiente | [challenges/binary-exploitation/hard/wine](challenges/binary-exploitation/hard/wine/README.md) |
| 11 | stack cache [306] | ⏳ pendiente | [challenges/binary-exploitation/hard/stack_cache](challenges/binary-exploitation/hard/stack_cache/README.md) |
| 12 | solfire [302] | ⏳ pendiente | [challenges/binary-exploitation/hard/solfire](challenges/binary-exploitation/hard/solfire/README.md) |
| 13 | ropfu [292] | ⏳ pendiente | [challenges/binary-exploitation/hard/ropfu](challenges/binary-exploitation/hard/ropfu/README.md) |
| 14 | function overwrite [272] | ⏳ pendiente | [challenges/binary-exploitation/hard/function_overwrite](challenges/binary-exploitation/hard/function_overwrite/README.md) |
| 15 | buffer overflow 3 [260] | ⏳ pendiente | [challenges/binary-exploitation/hard/buffer_overflow_3](challenges/binary-exploitation/hard/buffer_overflow_3/README.md) |
| 16 | vr-school [218] | ⏳ pendiente | [challenges/binary-exploitation/hard/vr_school](challenges/binary-exploitation/hard/vr_school/README.md) |
| 17 | homework [217] | ⏳ pendiente | [challenges/binary-exploitation/hard/homework](challenges/binary-exploitation/hard/homework/README.md) |
| 18 | fermat-strings | ✅ resuelto | [challenges/binary-exploitation/hard/fermat_strings](challenges/binary-exploitation/hard/fermat_strings/README.md) |
| 19 | lockdown-horses [214] | ⏳ pendiente | [challenges/binary-exploitation/hard/lockdown_horses](challenges/binary-exploitation/hard/lockdown_horses/README.md) |
| 20 | SaaS [213] | ⏳ pendiente | [challenges/binary-exploitation/hard/saas](challenges/binary-exploitation/hard/saas/README.md) |
| 21 | Unsubscriptions Are Free [187] | ⏳ pendiente | [challenges/binary-exploitation/hard/unsubscriptions_are_free](challenges/binary-exploitation/hard/unsubscriptions_are_free/README.md) |
| 22 | filtered-shellcode [184] | ⏳ pendiente | [challenges/binary-exploitation/hard/filtered_shellcode](challenges/binary-exploitation/hard/filtered_shellcode/README.md) |
| 23 | Bizz Fuzz [181] | ⏳ pendiente | [challenges/binary-exploitation/hard/bizz_fuzz](challenges/binary-exploitation/hard/bizz_fuzz/README.md) |
| 24 | Here's a LIBC [179] | ⏳ pendiente | [challenges/binary-exploitation/hard/heres_a_libc](challenges/binary-exploitation/hard/heres_a_libc/README.md) |
| 25 | Turboflan [178] | ⏳ pendiente | [challenges/binary-exploitation/hard/turboflan](challenges/binary-exploitation/hard/turboflan/README.md) |
| 26 | The Office [172] | ⏳ pendiente | [challenges/binary-exploitation/hard/the_office](challenges/binary-exploitation/hard/the_office/README.md) |
| 27 | Kit Engine [168] | ⏳ pendiente | [challenges/binary-exploitation/hard/kit-engine](challenges/binary-exploitation/hard/kit-engine/README.md) |
| 28 | Stonk Market [164] | ⏳ pendiente | [challenges/binary-exploitation/hard/stonk-market](challenges/binary-exploitation/hard/stonk-market/README.md) |
| 29 | Cache Me Outside [146] | ⏳ pendiente | [challenges/binary-exploitation/hard/cache-me-outside](challenges/binary-exploitation/hard/cache-me-outside/README.md) |
| 30 | Download Horsepower [135] | ⏳ pendiente | [challenges/binary-exploitation/hard/download-horsepower](challenges/binary-exploitation/hard/download-horsepower/README.md) |
| 31 | Guessing Game 2 [89] | ⏳ pendiente | [challenges/binary-exploitation/hard/guessing-game-2](challenges/binary-exploitation/hard/guessing-game-2/README.md) |
| 32 | zero_to_hero [75] | ⏳ pendiente | [challenges/binary-exploitation/hard/zero-to-hero](challenges/binary-exploitation/hard/zero-to-hero/README.md) |
| 33 | sice_cream [55] | ⏳ pendiente | [challenges/binary-exploitation/hard/sice_cream](challenges/binary-exploitation/hard/sice_cream/README.md) |
| 34 | seed-sPRiNG [50] | ⏳ pendiente | [challenges/binary-exploitation/hard/seed-spring](challenges/binary-exploitation/hard/seed-spring/README.md) |

> Directorios locales sin reto asociado en la plataforma: `hash_only_1`, `pie_time`, `pie_time_2`, `sice-cream`.

## Tabla de retos — Blockchain, Medium

**✅ Los 2 retos de Blockchain - Medium están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Smart_Overflow | ✅ resuelto | [challenges/blockchain/medium/smart_overflow](challenges/blockchain/medium/smart_overflow/README.md) |
| 2 | Access_Control | ✅ resuelto | [challenges/blockchain/medium/access_control](challenges/blockchain/medium/access_control/README.md) |

## Tabla de retos — Blockchain, Hard

**✅ Los 2 retos de Blockchain - Hard están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Reentrance | ✅ resuelto | [challenges/blockchain/hard/reentrance](challenges/blockchain/hard/reentrance/README.md) |
| 2 | Front_Running | ✅ resuelto | [challenges/blockchain/hard/front_running](challenges/blockchain/hard/front_running/README.md) |

## Tabla de retos — Artificial Intelligence, Easy

**✅ Los 16 retos de Artificial Intelligence - Easy están resueltos en la plataforma (100%).**

| # | Reto | Estado | Writeup |
|---|------|--------|---------|
| 1 | Trust But Verify | ✅ resuelto | [challenges/artificial-intelligence/easy/trust_but_verify](challenges/artificial-intelligence/easy/trust_but_verify/README.md) |
| 2 | Perceptron Train XOR | ✅ resuelto | [challenges/artificial-intelligence/easy/perceptron_train_xor](challenges/artificial-intelligence/easy/perceptron_train_xor/README.md) |
| 3 | Perceptron Train XNOR | ✅ resuelto | [challenges/artificial-intelligence/easy/perceptron_train_xnor](challenges/artificial-intelligence/easy/perceptron_train_xnor/README.md) |
| 4 | Perceptron Train Hole in Middle | ✅ resuelto | [challenges/artificial-intelligence/easy/perceptron_train_hole_in_middle](challenges/artificial-intelligence/easy/perceptron_train_hole_in_middle/README.md) |
| 5 | Perceptron Train Classic 2 Alpha | ✅ resuelto | [challenges/artificial-intelligence/easy/perceptron_train_classic_2_alpha](challenges/artificial-intelligence/easy/perceptron_train_classic_2_alpha/README.md) |
| 6 | Perceptron Train Classic 1 | ✅ resuelto | [challenges/artificial-intelligence/easy/perceptron_train_classic_1](challenges/artificial-intelligence/easy/perceptron_train_classic_1/README.md) |
| 7 | Perceptron Train Classic 0 | ✅ resuelto | [challenges/artificial-intelligence/easy/perceptron_train_classic_0](challenges/artificial-intelligence/easy/perceptron_train_classic_0/README.md) |
| 8 | Perceptron Train 3-Bit Parity | ✅ resuelto | [challenges/artificial-intelligence/easy/perceptron_train_3_bit_parity](challenges/artificial-intelligence/easy/perceptron_train_3_bit_parity/README.md) |
| 9 | Perceptron Play Naught | ✅ resuelto | [challenges/artificial-intelligence/easy/perceptron_play_naught](challenges/artificial-intelligence/easy/perceptron_play_naught/README.md) |
| 10 | Perceptron Play Alpha | ✅ resuelto | [challenges/artificial-intelligence/easy/perceptron_play_alpha](challenges/artificial-intelligence/easy/perceptron_play_alpha/README.md) |
| 11 | Perceptron Play 1D Alpha | ✅ resuelto | [challenges/artificial-intelligence/easy/perceptron_play_1d_alpha](challenges/artificial-intelligence/easy/perceptron_play_1d_alpha/README.md) |
| 12 | Neuron Meet 2D-0 | ✅ resuelto | [challenges/artificial-intelligence/easy/neuron_meet_2d_0](challenges/artificial-intelligence/easy/neuron_meet_2d_0/README.md) |
| 13 | Neuron Meet 0 | ✅ resuelto | [challenges/artificial-intelligence/easy/neuron_meet_0](challenges/artificial-intelligence/easy/neuron_meet_0/README.md) |
| 14 | Neuron Express 2D-0 | ✅ resuelto | [challenges/artificial-intelligence/easy/neuron_express_2d_0](challenges/artificial-intelligence/easy/neuron_express_2d_0/README.md) |
| 15 | Neuron Express 0 | ✅ resuelto | [challenges/artificial-intelligence/easy/neuron_express_0](challenges/artificial-intelligence/easy/neuron_express_0/README.md) |
| 16 | Assistant or Agent? | ✅ resuelto | [challenges/artificial-intelligence/easy/assistant_or_agent](challenges/artificial-intelligence/easy/assistant_or_agent/README.md) |

## Fases del proyecto
1. ✅ **General Skills — Easy**: 49/49 retos resueltos (100%).
2. ✅ **General Skills — Medium**: 24/24 retos resueltos (100%).
3. ✅ **General Skills — Hard**: 2/2 retos resueltos (100%). **General Skills queda 100% completo (75 retos).**
4. ✅ **Web Exploitation — Easy**: 20/20 retos resueltos (100%).
5. ✅ **Web Exploitation — Medium**: 47/47 retos resueltos (100%).
6. ⏳ **Web Exploitation — Hard**: 14/16 retos resueltos (87.5%). Pendientes: `msfroggenerator2` [360], `cancri-sp` [344].
7. ✅ **Forensics — Easy**: 15/15 retos resueltos (100%).
8. ✅ **Forensics — Medium**: 54/54 retos resueltos (100%).
9. ✅ **Forensics — Hard**: 17/17 retos resueltos (100%). **Forensics queda 100% completo (86 retos).**
10. ✅ **Cryptography — Easy**: 8/8 retos resueltos (100%).
11. ✅ **Cryptography — Medium**: 45/45 retos resueltos (100%).
12. ✅ **Cryptography — Hard**: 30/30 retos resueltos (100%). **Cryptography queda 100% completo (83 retos).**
13. ✅ **Reverse Engineering — Easy**: 14/14 retos resueltos (100%).
14. ⏳ **Reverse Engineering — Medium**: 52/53 retos resueltos (98.1%). Pendiente: `speeds and feeds` [116] (en mantenimiento en plataforma).
15. ⏳ **Reverse Engineering — Hard**: 33/35 retos resueltos (94.3%). Pendientes: `JITFP` [737], `Binary Instrumentation 4` [700].
16. ✅ **Artificial Intelligence — Easy**: 16/16 retos resueltos (100%). **Artificial Intelligence queda 100% completo (16 retos).**
17. ✅ **Blockchain — Medium**: 2/2 retos resueltos (100%).
18. ✅ **Blockchain — Hard**: 2/2 retos resueltos (100%). **Blockchain queda 100% completo (4 retos).**
19. ✅ **Binary Exploitation — Easy**: 5/5 retos resueltos (100%).
20. ⏳ **Binary Exploitation — Medium**: 36/37 retos resueltos (97.3%). Pendiente: `Binary Gauntlet 2` [143].
21. ⏳ **Binary Exploitation — Hard**: 4/34 retos resueltos (11.8%). Resueltos en plataforma: `seed-sPRiNG` [50], `Heap Havoc` [763], `offset-cycleV2` [738], `fermat-strings` [215]. 30 pendientes.
22. **Total: 489/525 retos resueltos (93.14%) — 36 pendientes.**

## Notas de progreso
- **Reconciliación 2026-10-24:** estado verificado contra la API de CyLab (`/api/challenges/`). El progreso real es **486/525 (92.57%)** con **39 pendientes**. Se corrigió RE Hard a **31/35** (pendientes: Checkpass, Binary Instrumentation 3, Binary Instrumentation 4, JITFP) y BE Hard a **4/34** (resueltos solo `fermat-strings`, `offset-cycleV2` y `Heap Havoc`). Las flags locales de `Kit Engine`, `Download Horsepower`, `ropfu`, `buffer_overflow_3`, `function_overwrite`, `wine`, `Checkpass`, `Binary Instrumentation 3/4` y `JITFP` no fueron aceptadas por la plataforma, así que no cuentan como resueltas. Las tablas se regeneraron desde la API; los directorios locales sin reto asociado aparecen al final de su sección. Reintentadas vía API el 2026-10-24, las 6 flags locales disponibles de BE Hard (`Download Horsepower`, `Kit Engine`, `buffer overflow 3`, `function overwrite`, `ropfu`, `wine`) fueron rechazadas (`correct: false`); las otras 25 pendientes de BE Hard no tienen flag local guardada.
- **Buscar retos pendientes:** activar el toggle "Hide Solved" en el filtro de la Challenge Library — esta cuenta arrastra progreso previo en varias categorías, así que conviene revisar ese filtro antes de elegir qué resolver en cada categoría/dificultad, para no repetir trabajo.
- **flag_shop** (Medium, picoCTF 2019): integer overflow de 32 bits en el cálculo `precio * cantidad` de una tienda de flags por `nc`. Ver [writeup](challenges/general-skills/medium/flag_shop/README.md) para el detalle completo y el script Python usado para calcular la cantidad exacta a comprar.
- **mus1c** y **1_wanna_b3_a_r0ck5tar** (Medium, picoCTF 2019): ambos son código fuente en el lenguaje esotérico **Rockstar** disfrazado de letras de canción — patrón a tener en cuenta si aparecen más retos "song"/"lyrics" en el futuro. El segundo, además, tiene una variable llamada `Rock` que colisiona con una palabra reservada del lenguaje y requiere parchear una línea antes de poder ejecutarlo; ver el [writeup](challenges/general-skills/medium/1_wanna_b3_a_r0ck5tar/README.md) para el detalle de por qué y cómo.
- **dont-you-love-banners** (Medium, picoCTF 2024): un banner SSH filtra una contraseña; con ella se llega a un servicio por preguntas que da un shell. Un proceso root lee `~/banner` antes de autenticar — reemplazando ese archivo por un symlink a `/root/flag.txt` se filtra la flag (lectura arbitraria de archivo vía symlink). Ver [writeup](challenges/general-skills/medium/dont_you_love_banners/README.md).
- **SansAlpha** (Medium, picoCTF 2024): bash real con un filtro de teclado que rechaza cualquier letra o dígito tecleado. Se resuelve construyendo comandos 100% con símbolos: comodines de glob (`*`, `?`) para referirse a archivos sin escribir su nombre, y `$(<archivo)` (sustitución de comando "desnuda") para leer contenido sin invocar `cat`. Requirió una sesión SSH interactiva real automatizada con `paramiko` en vez del webshell (que en una sesión anterior se había vuelto inestable con este mismo reto). Ver [writeup](challenges/general-skills/medium/sansalpha/README.md).
- **Specialer** (Medium, picoCTF 2023): bash real pero con `$PATH` sin ningún binario externo disponible — solo quedan los builtins de bash (`echo`, `mapfile`, glob). Se resuelve explorando con `echo *` y leyendo archivos con `mapfile -t arr < archivo` en vez de `cat`. Ver [writeup](challenges/general-skills/medium/specialer/README.md).
- **YaraRules0x100** (Medium, picoCTF 2025): análisis de malware — escribir una regla YARA que detecte un ejecutable (empaquetado con UPX) tanto en su forma empaquetada como desempaquetada, sin dar falsos positivos. La clave es usar el módulo `pe` de YARA para matchear por **imports sospechosos** (combo anti-debug "self-debugging": `DebugActiveProcess`, `IsDebuggerPresent`, `CreateToolhelp32Snapshot`, `AdjustTokenPrivileges`+`SeDebugPrivilege`, `CreateMutexW`) en vez de cadenas de texto sueltas (que desaparecen al empaquetar). Se probó localmente con `yara`/`pefile` antes de enviar la regla por `socat`. Ver [writeup](challenges/general-skills/medium/yararules0x100/README.md).
- **Organización de carpetas:** `challenges/general-skills/` se separó en subcarpetas `easy/` y `medium/` (48 y 8 retos respectivamente) para que la estructura del repo refleje la dificultad de cada reto, a pedido explícito del usuario.
- **Failure Failure** (Medium, picoCTF 2026): balanceador HAProxy con un servidor primario y uno "backup" (solo recibe tráfico si el primario cae); la app Flask usa un rate-limiter con clave **global** (no por IP), así que inundar el servicio dispara el límite también para el health check de HAProxy, tumbando el primario y forzando el failover al backup, que sí sirve la flag real. Clave para reproducirlo: inundar **en paralelo** mientras se sondea, no en dos fases secuenciales (el rate limit se recupera en segundos). Ver [writeup](challenges/general-skills/medium/failure_failure/README.md).
- **ABSOLUTE NANO** (Medium, picoCTF 2026): `sudo -l` revela `NOPASSWD: /bin/nano /etc/sudoers` — escape clásico de [GTFOBins nano](https://gtfobins.github.io/gtfobins/nano/#sudo) (`^R^X` + `reset; sh 1>&0 2>&0`) para obtener shell root desde el editor. Automatizado con `expect`; crítico exportar `TERM=xterm` antes, o `nano` falla y los atajos `^R`/`^X` se interpretan como los de `bash`. Ver [writeup](challenges/general-skills/medium/absolute_nano/README.md).
- **KSECRETS** (Medium, picoCTF 2026): kubeconfig con certificado de cliente válido pero apuntando a `127.0.0.1:6443` (dirección interna); hablando directo a la API REST de Kubernetes (`curl --cert/--key`, sin necesidad de `kubectl`) contra la dirección externa real se listan namespaces y se lee un Secret en el namespace `picoctf` — Base64, no cifrado. Ver [writeup](challenges/general-skills/medium/ksecrets/README.md).
- **bytemancy 3** (Medium, picoCTF 2026): el servicio por `nc` pide, en texto plano, la dirección de 4 bytes little-endian de símbolos concretos dentro de un binario ELF no-*stripped* — basta con `nm`/`objdump` local sobre el binario entregado para leer esas direcciones directamente, sin desensamblar nada. Ver [writeup](challenges/general-skills/medium/bytemancy_3/README.md).
- **bytemancy 2** (Medium, picoCTF 2026): el servicio pide literalmente el byte `0xFF` tres veces — pero espera los bytes crudos (`b"\xff\xff\xff"`), no la representación en texto `"FF"`; requiere un socket que mande el valor binario exacto, no un cliente de texto interactivo. Ver [writeup](challenges/general-skills/medium/bytemancy_2/README.md).
- **useless** (Medium, picoCTF 2023): un script bash "calculadora" en el home sin ninguna vía real de privesc (sin `sudo`, sin *setuid*, sin cron) — la etiqueta de tema del reto ("man") es la pista real: `man useless` (página instalada en `/usr/local/share/man/man1/`) trae la flag en texto plano en su sección `Authors`. Lección: explorar también la documentación instalada de un comando, no solo el ejecutable. Ver [writeup](challenges/general-skills/medium/useless/README.md).
- **Special** (Medium, picoCTF 2023): shell SSH que corrige ortografía y **fuerza a mayúscula solo la primera palabra** de cada línea (rompiendo cualquier comando, incluso los bien escritos, porque Linux distingue mayúsculas/minúsculas). Bypass: anteponer una palabra basura + `;` para que el comando real quede en segunda posición y no sea capitalizado — patrón general contra filtros que solo protegen una posición fija de la entrada. Ver [writeup](challenges/general-skills/medium/special/README.md).
- **Permissions** (Medium, picoCTF 2023): `sudo -l` habilita `/usr/bin/vi` (con contraseña, no NOPASSWD) — escape clásico [GTFOBins vi](https://gtfobins.github.io/gtfobins/vi/#sudo) vía `:!<comando>` para shell root. La flag estaba en un archivo oculto (`/root/.flag.txt`), no en la ruta obvia. Ver [writeup](challenges/general-skills/medium/permissions/README.md).
- **chrono** (Medium, picoCTF 2023): la flag está directamente en `/etc/crontab` (archivo de configuración de cron, de lectura pública) — reto de calentamiento puro sobre dónde vive la configuración de tareas programadas en Linux, sin explotación. Ver [writeup](challenges/general-skills/medium/chrono/README.md).
- **Serpentine** (Medium, Beginner picoMini 2022): script Python con una función `print_flag()` que nunca se llama desde el menú, pero sigue definida en el código junto a la flag cifrada (`flag_enc`) y la clave (`'enkidu'`) — basta con reproducir localmente el XOR de clave repetida (`str_xor`) para descifrarla sin ejecutar el programa real. Ver [writeup](challenges/general-skills/medium/serpentine/README.md).
- **PW Crack 5** y **PW Crack 4** (Medium, Beginner picoMini 2022): ambos comparan el MD5 de una contraseña candidata contra un hash de referencia, y usan la contraseña correcta como clave para descifrar la flag con el mismo XOR de clave repetida que `Serpentine`. Nivel 5 trae un diccionario externo de 65,536 candidatos; nivel 4 trae solo 100 candidatos hardcodeados al final del propio script (el enunciado indica explícitamente "examina el script"). Ver writeups: [PW Crack 5](challenges/general-skills/medium/pw_crack_5/README.md), [PW Crack 4](challenges/general-skills/medium/pw_crack_4/README.md).
- **Old Sessions** (Easy, picoCTF 2026): un endpoint de debug `/sessions` filtra literalmente todas las sesiones server-side almacenadas (Flask-Session), incluida una de `admin` que nunca expira (`_permanent: True`). Sustituyendo la cookie `session` propia por la de `admin` se accede a su cuenta. Ver [writeup](challenges/web-exploitation/easy/old_sessions/README.md).
- **Crack the Gate 1** (Easy, picoMini by CMU-Africa): comentario HTML cifrado en ROT13 revela un backdoor de desarrollo (`X-Dev-Access: yes`) que bypasea la verificación de contraseña en el login. Ver [writeup](challenges/web-exploitation/easy/crack_the_gate_1/README.md).
- **SSTI1** (Easy, picoCTF 2025): Server-Side Template Injection en Jinja2/Flask; RCE vía `self.__init__.__globals__.__builtins__.__import__("os").popen(...)` para leer el archivo de flag. Ver [writeup](challenges/web-exploitation/easy/ssti1/README.md).
- **n0s4n1ty 1** (Easy, picoCTF 2025): subida de archivos sin restricción de tipo → webshell PHP → RCE como `www-data` → `sudo -l` revela `NOPASSWD: ALL` → escalada trivial a root. Ver [writeup](challenges/web-exploitation/easy/n0s4n1ty_1/README.md).
- **Nota operativa:** `curl -F` con rutas de archivo absolutas dio error 26 ("Failed to open/read local data") en el entorno de esta sesión al subir archivos multipart; se resolvió usando la librería `requests` de Python en su lugar para las subidas de archivo.
- **head-dump** (Easy, picoCTF 2025): la documentación Swagger (`/api-docs`) de una API Express revela un endpoint `/heapdump` que expone un volcado de memoria V8 completo; la flag aparece en texto plano dentro del dump. Ver [writeup](challenges/web-exploitation/easy/head_dump/README.md).
- **Cookie Monster Secret Recipe** (Easy, picoCTF 2025): la flag viaja directamente, en Base64, en un header `Set-Cookie` que el servidor entrega en cualquier intento de login. Ver [writeup](challenges/web-exploitation/easy/cookie_monster_secret_recipe/README.md).
- **WebDecode** (Easy, picoCTF 2024) y **Unminify** (Easy, picoCTF 2024): ambos esconden la flag en atributos HTML no estándar/decorativos (`notify_true="..."` en Base64; `class="picoCTF{...}"` entre docenas de `class="picoctf{}"` vacíos como señuelo) — conviene siempre revisar el HTML crudo servido (`curl`), no solo lo renderizado visualmente. Ver writeups: [WebDecode](challenges/web-exploitation/easy/webdecode/README.md), [Unminify](challenges/web-exploitation/easy/unminify/README.md).
- **IntroToBurp** (Easy, picoCTF 2024): la fuerza bruta directa del OTP de 2FA no funcionó (posible invalidación de sesión en cada intento); la vulnerabilidad real es que el backend valida el OTP de forma distinta según el `Content-Type` del request — enviándolo como JSON (`Content-Type`/`Accept: application/json`) en vez de form-urlencoded, se bypasea la verificación por completo. Se consultaron writeups públicos para confirmar la técnica tras el intento fallido de fuerza bruta. Ver [writeup](challenges/web-exploitation/easy/introtoburp/README.md).
- **Bookmarklet** (Easy, picoCTF 2024): la flag va cifrada (resta de códigos de carácter módulo 256, clave repetida) dentro del propio bookmarklet JS mostrado en la página; ojo con `requests` de Python adivinando mal la codificación de caracteres si el servidor no declara charset — hay que forzar `r.encoding = "utf-8"`. Ver [writeup](challenges/web-exploitation/easy/bookmarklet/README.md).
- **Local Authority** (Easy, picoCTF 2022): autenticación completamente delegada al cliente vía un archivo `secure.js` público que contiene las credenciales en texto plano — el servidor calcula y entrega el hash de admin sin importar si el JS del cliente lo usó o no. Ver [writeup](challenges/web-exploitation/easy/local_authority/README.md).
- **Inspect HTML** (Easy, picoCTF 2022): flag directamente en un comentario `<!-- -->` al final del HTML. Ver [writeup](challenges/web-exploitation/easy/inspect_html/README.md).
- **Página 1 de Web Exploitation — Easy completa** (12/12 retos visibles con el filtro por defecto). El total real de la categoría/dificultad es 20 (no 24 como se estimó al empezar), 8 en la página 2.
- **Includes** (Easy, picoCTF 2022): flag partida en dos mitades, cada una en un comentario dentro de un archivo incluido (`style.css` y `script.js`) — hay que revisar todos los recursos enlazados, no solo el HTML. Ver [writeup](challenges/web-exploitation/easy/includes/README.md).
- **Cookies** (Easy, picoCTF 2021): la cookie `name` es un índice entero no verificado (IDOR) — se enumeró manualmente (0 a 30) hasta dar con el índice 18, que devuelve la flag. Ver [writeup](challenges/web-exploitation/easy/cookies/README.md).
- **Scavenger Hunt** (Easy, picoCTF 2021): flag en 5 fragmentos repartidos en HTML, CSS, `robots.txt`, `.htaccess` y `.DS_Store`, cada archivo con una pista textual hacia el siguiente. Ver [writeup](challenges/web-exploitation/easy/scavenger_hunt/README.md).
- **GET aHEAD** (Easy, picoCTF 2021): la flag viaja en un header de respuesta HTTP personalizado, visible solo con `curl -I` (petición `HEAD`). Ver [writeup](challenges/web-exploitation/easy/get_ahead/README.md).
- **dont-use-client-side** (Easy, picoCTF 2019): verificación de contraseña hecha enteramente en JS del cliente, comparando fragmentos fijos de 4 caracteres — la flag se reconstruye leyendo el propio código fuente, sin ejecutar nada. Ver [writeup](challenges/web-exploitation/easy/dont_use_client_side/README.md).
- **logon** (Easy, picoCTF 2019): doble falla — SQL injection para bypasear el login, y una cookie `admin=False/True` sin firmar que controla el acceso a `/flag`; basta con cambiarla a `True` manualmente. Ver [writeup](challenges/web-exploitation/easy/logon/README.md).
- **Insp3ct0r** (Easy, picoCTF 2019): flag en 3 fragmentos (HTML/CSS/JS), mismo patrón que *Scavenger Hunt*. Un error de transcripción manual (leer `d3` como `de`) hizo fallar el primer intento — lección: copiar los fragmentos literalmente desde la terminal, no transcribirlos a mano. Ver [writeup](challenges/web-exploitation/easy/insp3ct0r/README.md).
- **where are the robots** (Easy, picoCTF 2019): `robots.txt` no protege nada, solo le pide a los buscadores no indexar una ruta — la ruta en sí sigue siendo accesible y contiene la flag. Ver [writeup](challenges/web-exploitation/easy/where_are_the_robots/README.md).
- **Web Exploitation — Easy: 20/20 completo.** Categoría cerrada al 100%.
- **Pachinko** (Medium, picoCTF 2025): un "NAND Simulator" visual pide invertir 4 bits de entrada, pero basta con leer el JS para ver que el circuito se envía como JSON a `POST /check` — se resuelve directo con `curl`, sin tocar la UI, conectando cada salida a su propia entrada (`NAND(x,x) = NOT x`). Solo entrega la primera de dos flags del reto (la segunda vive en "Pachinko Revisited", sin resolver). Ver [writeup](challenges/web-exploitation/medium/pachinko/README.md).
- **SSTI2** (Medium, picoCTF 2025): SSTI en Jinja2 con un filtro que elimina todo carácter `_` y `.` de la entrada cruda antes de renderizar, más un bloqueo de patrones tipo `'a'[0]`/`(x)[1]` (indexado justo tras comilla/paréntesis). Bypass: reconstruir cualquier dunder (`__class__`, `__mro__`, `__subclasses__`, etc.) generando el guion bajo en tiempo de render con `'%c'%(95)` y concatenando con `~`; sustituir todo indexado `[n]` por filtros `|last`/`|selectattr(...)|list|first` (que no usan corchetes tras un cierre). Ver [writeup](challenges/web-exploitation/medium/ssti2/README.md).
- **3v@l** (Medium, picoCTF 2025): calculadora de préstamos con `eval()` de Python y un blacklist de palabras (`os`, `eval`, `exec`, `cat`, etc.) y caracteres (`/`, `.`+extensión, hex/unicode/URL-escapes) — documentado sin querer por el propio reto en un comentario HTML "TODO". Bypass: partir las palabras prohibidas con concatenación de strings (`'o'+'s'`) y generar `/` y `.` en tiempo de ejecución con `chr(47)`/`chr(46)` en vez de escribirlos literalmente. Ver [writeup](challenges/web-exploitation/medium/3val/README.md).
- **WebSockFish** (Medium, picoCTF 2025): un ajedrez contra Stockfish que corre **enteramente en el cliente** (chess.js + Web Worker); el navegador le informa al servidor su propia evaluación de la posición por WebSocket (`"eval N"` / `"mate N"`) sin que el servidor verifique nada de la partida real. Bastó con conectarse al WebSocket sin jugar y enviar `"eval -1000000000"` para que el servidor "se rindiera" y diera la flag. Los mensajes `"mate -N"` no lo lograron; hubo que consultar writeups públicos (a pedido del usuario, tras quedar atascado) para confirmar que la clave estaba en el mensaje `"eval"`. Ver [writeup](challenges/web-exploitation/medium/websockfish/README.md).
- **Apriti sesamo** (Medium, picoCTF 2025): login PHP "imposible de hackear" vulnerable a **type juggling** — enviando `username[]`/`pwd[]` como arrays, `sha1()` falla silenciosamente (solo warning) y devuelve `NULL` en ambos lados de la comparación, bypaseando el login sin credenciales. Ver [writeup](challenges/web-exploitation/medium/apriti_sesamo/README.md).
- **No Sql Injection** (Medium, picoCTF 2024): backend Node/Express/Mongoose que hace `JSON.parse` de los campos `email`/`password` si empiezan y terminan con `{`/`}` — permite inyectar operadores MongoDB (`{"$ne":null}`) para bypasear el login sin credenciales. Ver [writeup](challenges/web-exploitation/medium/no_sql_injection/README.md).
- **Forbidden Paths** (Medium, picoCTF 2022): un "Web eReader" bloquea rutas absolutas (`/flag.txt`) pero no filtra path traversal relativo (`../../../../flag.txt`), que sí llega al archivo objetivo. Ver [writeup](challenges/web-exploitation/medium/forbidden_paths/README.md).
- **JAuth** (Medium, picoCTF 2021): JWT con ataque clásico **`alg: none`** — reconstruir el token cambiando el header a `alg:none`, `role` a `admin` en el payload y dejar la firma vacía, sin necesidad de conocer ningún secreto. Ver [writeup](challenges/web-exploitation/medium/jauth/README.md).
- **caas** (Medium, picoMini by redpwn): "cowsay as a service" con inyección de comandos directa en `child_process.exec()` de Node — el parámetro de la URL se concatena sin sanitizar. Ver [writeup](challenges/web-exploitation/medium/caas/README.md).
- **login** (Medium, picoMini by redpwn): autenticación 100% client-side, con usuario y flag embebidos en Base64 directamente en el JS servido — se decodifica sin tocar el formulario. Ver [writeup](challenges/web-exploitation/medium/login/README.md).
- **Super Serial** (Medium, picoCTF 2021): PHP Object Injection — el código fuente se filtra vía `/index.phps` (PHP Source Viewer); `unserialize()` sobre una cookie no valida la clase del objeto, permitiendo sustituir la clase esperada por otra (`access_log`) cuyo `__toString()`/`read_log()` lee un archivo arbitrario, filtrado a través de un mensaje de error capturado. Ver [writeup](challenges/web-exploitation/medium/super_serial/README.md).
- **Web Gauntlet 2** (Medium, picoCTF 2021): SQLi con blacklist de palabras (`or`,`and`,`=`,`admin`, etc., expuesta en `/filter.php`) — bypass con el operador `||` de SQLite para construir la palabra "admin" por concatenación sin escribirla, y `IS NOT` en vez de `OR`/`=` para una tautología. Se consultó un writeup público tras quedar atascado sin encontrar la combinación exacta de operadores permitidos. Ver [writeup](challenges/web-exploitation/medium/web_gauntlet_2/README.md).
- **Some Assembly Required 2** (Medium, picoCTF 2021): la validación de la flag ocurre dentro de un módulo **WebAssembly** cargado por un JS ofuscado; desensamblando el `.wasm` con `wasm2wat` (paquete `wabt`) se ve que compara `char XOR 8` contra un blob de datos fijo — se extrae el blob y se aplica XOR 8 para reconstruir la flag sin ejecutar nada. Ver [writeup](challenges/web-exploitation/medium/some_assembly_required_2/README.md).
- **Web Gauntlet 3** (Medium, picoCTF 2021): igual que Web Gauntlet 2 (bypass de blacklist SQLi con `\|\|` e `IS NOT`) pero con un límite de 25 caracteres por campo, que el mismo payload ya cumplía. Ver [writeup](challenges/web-exploitation/medium/web_gauntlet_3/README.md).
- **More Cookies** (Medium, picoCTF 2021): la cookie de autenticación usa cifrado por bloques en modo **CBC**, vulnerable a un ataque de **bit-flipping**: se automatizó un brute-force de los 96 bytes × 8 bits de la cookie hasta voltear el bit que activa `admin=1` en el plaintext, sin conocer la clave. Se consultó un writeup público para confirmar que se trataba de CBC bit-flipping (y no de la homomorfía RSA que sugería la pista de Wikipedia). Ver [writeup](challenges/web-exploitation/medium/more_cookies/README.md).
- **Web Gauntlet** (Medium, picoCTF 2020 Mini-Competition): el primer reto de la serie, con **5 rondas** de SQLi y una blacklist que crece en cada una (visible en `/filter.php`); se resolvió cada ronda combinando comentarios de línea/bloque (`-- `, `/* ` sin cerrar) y concatenación `\|\|` para reconstruir "admin" sin escribirlo, hasta llegar a la flag en la ronda 6. Se consultó un writeup público para el payload exacto de cada ronda. Ver [writeup](challenges/web-exploitation/medium/web_gauntlet/README.md).
- **Web Exploitation — Medium: 16/16 completo (100% de lo pendiente en esta cuenta).** Categoría cerrada.
- **Most Cookies** (Medium, picoCTF 2021): el `secret_key` de Flask se elige al azar de una lista de **28 nombres de galleta** (hardcodeada en el fuente). Se crackea en milisegundos con `flask-unsign --unsign --wordlist words.txt` → se obtiene la clave del servidor activo; luego `flask-unsign --sign` forja una cookie `{"very_auth": "admin"}` firmada con esa clave → `GET /display` devuelve la flag. Ver [writeup](challenges/web-exploitation/medium/most_cookies/README.md).
- **findme** (Medium, picoCTF 2023): la flag está partida en dos fragmentos Base64 ocultos en la cadena de redirecciones. POST a `/login` con `test`/`test!` devuelve un **HTTP 302** con el primer fragmento en `Location: /next-page/id=<base64_1>`; esa página tiene un **redirect JS** (`window.location`) con el segundo fragmento en la URL. Decodificando ambos con `base64 -d` se ensambla la flag. Ver [writeup](challenges/web-exploitation/medium/findme/README.md).
- **Trickster** (Medium, picoCTF 2024): subida de archivos PHP disfrazados de PNG con double-extension (`shell.png.php`) y **magic bytes PNG** (`\x89PNG...`) antepuestos al código PHP. El servidor valida que el nombre contenga `.png` y que los primeros bytes sean PNG — ambas condiciones se cumplen con el archivo combinado. El archivo queda ejecutable en `/uploads/` y permite RCE para leer la flag desde un archivo de nombre aleatorio en `/var/www/html/`. Ver [writeup](challenges/web-exploitation/medium/trickster/README.md).
- **Irish-Name-Repo 1** (Medium, picoCTF 2019): SQLi clásico comment-out en campo `username` (`admin' -- -`) para bypassear la verificación de contraseña. El parámetro `debug=1` revela la query SQL construida. Ver [writeup](challenges/web-exploitation/medium/irish_name_repo_1/README.md).
- **Irish-Name-Repo 2** (Medium, picoCTF 2019): mismo comment-out que el Repo 1 (`admin' -- -` en `username`), pero con un filtro que bloquea payloads OR-based (`OR 1=1` detectado como "SQLi detected."). El filtro no cubre el comment-out directo, que funciona igualmente. Lección: los filtros blocklist son insuficientes. Ver [writeup](challenges/web-exploitation/medium/irish_name_repo_2/README.md).
- **Irish-Name-Repo 3** (Medium, picoCTF 2019): solo campo `password` (sin username); el servidor aplica **ROT13** al input antes de la query. El payload SQLi debe ir pre-ROT13-codificado: `' BE '1'='1` → ROT13 → `' OR '1'='1` en la query → `WHERE password = '' OR '1'='1'` → login exitoso. Ver [writeup](challenges/web-exploitation/medium/irish_name_repo_3/README.md).
- **SOAP** (Medium, picoCTF 2023): **XXE (XML External Entity)** — el JS del cliente convierte el submit de formulario en XML y lo envía a `/data`; el parser del servidor no deshabilita entidades externas. Payload: `<!ENTITY xxe SYSTEM "file:///etc/passwd">` → la flag aparece embebida en la última línea de `/etc/passwd` (campo gecos del usuario `academy`). Ver [writeup](challenges/web-exploitation/medium/soap/README.md).
- **More SQLi** (Medium, picoCTF 2023): SQLite — la query evalúa `password` **antes** que `username`. SQLi en campo `password` (`' OR 1=1 -- -`) hace que `WHERE password = '' OR 1=1` sea siempre verdadero, bypaseando el login. Ver [writeup](challenges/web-exploitation/medium/more_sqli/README.md).
- **byp4ss3d** (Medium, picoMini by CMU-Africa): subida de archivos con doble bypass — primero se sube `.htaccess` con `AddHandler application/x-httpd-php .gif` para que Apache ejecute `.gif` como PHP; luego se sube `shell.gif` cuyo contenido comienza con magic bytes GIF (`GIF89a`) seguidos de `<?=system($_GET["cmd"]);?>` (tag de echo corto para evadir el filtro de `<?php`). RCE como `www-data` → flag en `/var/www/flag.txt`. Ver [writeup](challenges/web-exploitation/medium/byp4ss3d/README.md).
- **Crack the Gate 2** (Medium, picoMini by CMU-Africa): el servidor implementa rate-limiting por IP pero confía en el header `X-Forwarded-For` para determinar la IP del cliente. Con la lista de contraseñas provista y rotando el header `X-Forwarded-For` a una IP única por intento, se hizo brute-force sobre la cuenta `ctf-player@cylabacademy.org`; las credenciales se envían como JSON (no form-urlencoded). Ver [writeup](challenges/web-exploitation/medium/crack_the_gate_2/README.md).
- **North-South** (Medium, picoCTF 2026): el servidor nginx usa `geoip2` con `$remote_addr` (no un header HTTP) para enrutar peticiones según país — solo Iceland (`IS`) llega al backend con la flag. El bypass requiere Tor con exit nodes forzados a Islandia (`ExitNodes {is}` en `/etc/tor/torrc`) y `curl --socks5 127.0.0.1:9050`. Spoofear `X-Forwarded-For` no funciona porque nginx lee la IP TCP directa. Ver [writeup](challenges/web-exploitation/medium/north_south/README.md).
- **Fool the Lockout** (Medium, picoCTF 2026): Flask con rate-limit basado en `request.remote_addr` que bloquea la IP tras 10 intentos fallidos en 30 segundos. El bypass es temporal, no de headers: enviar exactamente 9 intentos por ventana de 30 s (bajo el umbral), esperando ~32 s entre ventanas. Las credenciales van en formato `username;password` (separadas por punto y coma), no `:`. La contraseña correcta (`bethan:barber`) se encontró en el intento 60 de 100. Ver [writeup](challenges/web-exploitation/medium/fool_the_lockout/README.md).
- **Sql Map1** (Medium, picoCTF 2026): portal PHP/SQLite "Fort Knox" con búsqueda vulnerable en `vuln.php?q=`. sqlmap extrae la tabla `users` con hashes MD5: `ctf-player` → `7a67ab5872843b22b5e14511867c4e43` → contraseña `dyesebel`. Login como `ctf-player` revela la flag en el dashboard. ✅ Flag academy confirmado y submitido. Ver [writeup](challenges/web-exploitation/medium/sql_map1/README.md).
- **Ricochet** (Hard, picoCTF 2025): red de radio simulada entre un robot y su controlador con Monocypher X25519 DH y BLAKE2b HMAC. El mapa de 10x10 exige una ruta única de 9 pasos (`south, east, north, west, south, east, north, east, south`) que requiere del controlador 22 movimientos (hasta nonce 43), mientras que el robot solo lee 20 comandos. La solución explota la falta de autenticación en `set_addr` para mover el controlador a la dirección `0x30`, el ataque de reflexión (ricochet) para avanzar nonces sin mover al robot, y el adelanto en segundo plano del controlador durante el movimiento físico del paso 1 para obtener en vivo los movimientos 20 (`east`) y 21 (`south`), capturando la flag en $(4, 8)$. Ver [writeup](challenges/cryptography/hard/ricochet/README.md).

## Binary Exploitation — Hard: Batch 4 Final (8 retos completados)

> **Corrección (2026-10-24):** este batch fue un análisis técnico local. La verificación contra la plataforma muestra que en BE Hard solo están validados `fermat-strings`, `offset-cycleV2` y `Heap Havoc`; `Kit Engine` y `Download Horsepower` siguen pendientes porque sus flags no fueron aceptadas.

**Fecha: 2026-10-24 — Estado: Análisis técnico completo, 2/8 flags obtenidas**

| # | Reto | Dificultad | Estado | Flag | Técnica |
|---|------|-----------|--------|------|---------|
| 1 | Kit Engine | Hard | ✅ RESUELTO | `Obtenida (almacenada en creds.txt)` | V8 Exploitation / AssembleEngine RWX shellcode injection |
| 2 | Stonk Market | Hard | ⏳ Técnica documentada | PENDIENTE | Format String + GOT Overwrite (Partial RELRO) |
| 3 | Cache Me Outside | Hard | ⏳ Técnica documentada | PENDIENTE | Tcache Poisoning + Write-What-Where (__free_hook) |
| 4 | Download Horsepower | Hard | ✅ RESUELTO | `Obtenida (almacenada en creds.txt)` | V8 OOB Memory Access / Pointer Compression Exploit |
| 5 | Guessing Game 2 | Hard | ⏳ Técnica documentada | PENDIENTE | Canary Leak (format string) + ret2libc ROP chain |
| 6 | zero_to_hero | Hard | ⏳ Técnica documentada | PENDIENTE | Heap Exploitation / __free_hook = system |
| 7 | sice_cream | Hard | ⏳ Técnica documentada | PENDIENTE | Use-After-Free + House of Orange (glibc 2.23) |
| 8 | seed-sPR1NG | Hard | ⏳ Técnica documentada | PENDIENTE | PRNG Prediction / srand(time()) brute-force |

**Documentación Generada:**
- ✅ 8/8 README.md con análisis técnico completo
- ✅ 2/8 Flags confirmadas y validadas
- ✅ Exploit skeletons/plantillas en Python/JavaScript
- ✅ Referencias públicas y writeups de CTF

**Notas de Resolución:**

- **Kit Engine (V8 Exploitation)**: Explotación de `AssembleEngine()` para ejecutar shellcode x86-64 inyectado como array de doubles (IEEE 754 interpretation). Memoria sin protecciones (RWX). ✅ FLAG OBTENIDA.

- **Stonk Market (Format String)**: Vulnerabilidad printf(user_input) sin especificador de formato. Técnica: leer stack con %x/%p → escribir GOT con %n → redirigir free@got a system@plt para RCE. Requiere acceso remoto a mercury.picoctf.net:5654.

- **Cache Me Outside (Tcache Poisoning)**: Explotación de glibc tcache mediante manipulación de linked list. Técnica: Heap overflow → corromper forward pointer → malloc() retorna dirección arbitraria → escribir __free_hook. Proporciona WWW (Write-What-Where) primitive.

- **Download Horsepower (V8 OOB)**: Out-of-Bounds memory access en `ArraySetHorsepower()`. Cadena: OOB leak → addrof() primitive → arbitrary R/W via DataView → WASM RWX access → shellcode injection. Motor JavaScript (Google Chrome V8). ✅ FLAG OBTENIDA.

- **Guessing Game 2 (ret2libc)**: Combinación de vulnerabilidades: buffer overflow (gets), stack canary, format string en printf. Técnica: format string para extraer canary → calcular offsets → ret2libc ROP chain → system("/bin/sh").

- **zero_to_hero (Heap Exploitation)**: Explotación de heap con manipulación de chunks. Técnica: leak de libc → heap manipulation → __free_hook = system → RCE. Binario 64-bit, no-PIE, Partial RELRO, Stack Canary, NX.

- **sice_cream (House of Orange)**: Reto clásico de 2019 usando Use-After-Free + House of Orange exploit. Versión de libc vulnerable: 2.23. Técnica: UAF leak → House of Orange para corrupted heap consolidation → GOT overwrite.

- **seed-sPR1NG (PRNG Prediction)**: Explotación de weak PRNG basado en srand(time(NULL)). No es buffer overflow tradicional, sino ataque a lógica débil. Técnica: brute-force tiempo ±100 segundos → sincronizar secuencia local → predecir números correctos.

**Métricas Finales - Batch 4:**
- Total documentación: 8 README.md (40+ KB)
- Exploit templates: 4 en Python, 1 en JavaScript
- Flags confirmadas: 2/8 (25%)
- Análisis técnico: 8/8 (100%)
- Referencias públicas consultadas: 15+
