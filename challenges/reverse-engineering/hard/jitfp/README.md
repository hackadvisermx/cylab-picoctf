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
- Multiple solver implementations created:
  - `solver.py` - Initial sequential solver
  - `fast_solver.py` - Optimized character detection
  - `parallel_solver.py` - Parallel testing for faster convergence
- Solving in progress...

## Attack Surface Analysis

### Discovered Pattern
Testing reveals a character-by-character verification:
- Characters 'a' to 'k' produce: `================================` (1 line)
- Characters 'l' to 'z' and '0' to '9' produce: `================================v` + `*` (2 lines, with asterisks)

This suggests:
1. First character discrimination at ASCII boundary (k=107, l=108)
2. Asterisks may represent progress through the flag
3. Different flag positions may have different character sets

### Suspected Vulnerability  
The "timing" hints suggest a timing-based side-channel attack:
- Binary might have different execution times for correct vs. incorrect characters
- Partial correctness detection allowing progressive flag recovery
- The "host-specific" constraint might be related to timing precision

## Exploitation Attempts
1. Direct character enumeration - Successful at detecting character classes
2. Parallel testing - Implemented to reduce total testing time
3. Timing analysis - Limited by network latency and SSH overhead

## Notes
- The "JITFP" name likely means "Just In Time Flag Printer"
- Host-specific execution requirement prevents offline analysis
- Binary is stripped and PIE-compiled, preventing simple static analysis
- Timing vulnerability appears to be the intended attack vector
- This is a live challenge requiring fresh instances from CyLab
