# JITFP Challenge - picoCTF 2026

## Challenge Description
If we can crack the password checker on this remote host, we will be able to infiltrate deeper into this criminal organization. The catch is it only functions properly on the host on which we found it.

**Points:** 500  
**Difficulty:** Hard (3/3)  
**Category:** Reverse Engineering  

## Challenge Analysis

### Binary Information
- **Binary:** `ad7e550b` (14KB)
- **Format:** ELF 64-bit LSB PIE executable
- **Compiler:** GCC (Alpine 13.2.1)
- **Libc:** musl-x86_64
- **Status:** Stripped (no symbols)

### Key Observations

1. **Behavior Pattern:**
   - The binary takes a flag as command-line argument
   - It prints visual output (asterisks and lines) based on flag correctness
   - The flag format appears to be `academy{...}`

2. **Visual Output Analysis:**
   - Input with characters a-k after opening brace: Produces `================================` line
   - Input with characters l-z or 0-9 after opening brace: Produces `================================v` + `*` line
   - "Incorrect" message when the flag is wrong
   - "Correct" message indicates success (not yet observed)

3. **Timing Behavior:**
   - SSH commands often timeout when testing
   - The binary may have significant delays
   - Hints mention "If your timing isn't optimal, you can get a partially correct flag sometimes"
   - This suggests a timing-attack vulnerability

4. **System Constraints:**
   - Binary only works properly on the specific host it's deployed on
   - This is the key hint: the solution may depend on host-specific factors

### Challenge Hints
1. "You can exfiltrate files using `scp`" - Files can be copied from the system
2. "If your timing isn't optimal, you can get a partially correct flag sometimes" - Timing is critical
3. "Your extracted flag will be in standard academy{} flag format"

## Approach

### What We Know
- This is a JIT (Just In Time) flag printer/checker
- The verification process appears to check characters sequentially
- Visual output changes based on character correctness
- The binary is stripped and contains compiled code

### What We Need to Discover
1. The exact correct flag by finding which characters produce different outputs
2. The timing requirements for correct submission
3. Whether there's a timing-based vulnerability we can exploit

## Files
- `ad7e550b` - The target binary (exfiltrated from remote host)
- `solver.py` - Initial solver attempt using character enumeration
- `fast_solver.py` - Optimized solver using observed patterns

## Solving Strategy
1. Binary analysis suggests character-by-character verification
2. Use timing analysis to determine correct characters
3. Build flag one character at a time based on output patterns
4. Submit when complete flag is found

## Current Status
- Binary exfiltrated successfully to `tmp_files/ad7e550b`
- Basic behavior patterns identified
- Multiple solver implementations created and executed:
  - `solver.py` - Initial sequential solver
  - `fast_solver.py` - Optimized character detection [EXECUTED - Partial Success]
  - `parallel_solver.py` - Parallel testing for faster convergence
  - `simple_solver.py` - Character-by-character manual solver

### Solver Execution Results
**fast_solver.py Output:**
- Position 1: 'a' (12 asterisks) ✓
- Position 2: '8' (12 asterisks) ✓
- Position 3: 'r'/'x'/'u' (13 asterisks max) → 'r' selected ✓
- Position 4+: All characters: 0 asterisks → No progress detected ✗

**Partial Flag Found:** `academy{a8r`

**Analysis:** The asterisk-based detection reaches maximum around position 3-4, suggesting either:
1. The asterisk counter has a limit
2. Different detection method needed after position 3
3. The initial guess (a8r) may be incorrect, preventing further progress
4. The verification uses a different metric after initial characters

## Solución Definitiva

### Mecanismo Real (Just-In-Time Function Patching)
1. El binario ejecuta `prctl(PR_SET_PTRACER, -1)` para permitir que un servicio demonio local (`/root/jitfp-service.py`) interactúe con él vía `/proc/[pid]/mem`.
2. El demonio reescribe y reorganiza dinámicamente la tabla de punteros a funciones en `.bss` (`qword_4120`) aproximadamente una vez por segundo, en sincronía con el bucle `sleep(1)` del binario.
3. Para cada iteración $j$, únicamente la entrada permutada `qword_4120[dword_4020[j]]` contiene la función de validación con el byte de comparación real del carácter en la posición $j$; el resto de las entradas son señuelos aleatorios.
4. Muestreando la memoria a intervalos de 0.1s y extrayendo la diagonal sincronizada temporalmente (`correct_flag[j] = snapshot_j[j]`), se recuperan con precisión matemática los 33 caracteres de la bandera.

## Flag

```
academy{pr0cf5_d36ugg3r_6afaca48}
```

## Recursos Técnicos

- Linux `/proc/[pid]/mem` interface
- Double indirection function-pointer tables in C
- Just-In-Time code modification & debugging synchronization

