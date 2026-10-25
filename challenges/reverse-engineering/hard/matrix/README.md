# Challenge: MATRIX (ID 221, 500 pts)

**Category:** Reverse Engineering (Hard)  
**Author:** asphyxia  
**Event:** picoMini by redpwn

## Challenge Description

```
Enter the M A T R I X
```

The challenge provides a binary that implements an esoteric stack-based language interpreter. The program reads a program written in this custom language and executes it.

## Binary Analysis

### File Information
- **Type:** ELF 64-bit LSB pie executable, x86-64
- **Size:** 14,480 bytes
- **Stripped:** Yes (no symbols)
- **Compiler:** GCC 10.2.0

### Program Flow

1. Allocates two 0x800-byte (2048 bytes) buffers on the heap (r13 and r12)
2. Sets up input/output processing structures
3. Enters a main loop that:
   - Reads bytes from input
   - Interprets them as commands in the custom language
   - Processes stack operations
4. On successful verification, reads and outputs the flag from `flag.txt`
5. On failure, outputs "Have a flag!"

### Stack-Based Language

The interpreter implements a stack-based esoteric language with the following operations:

#### Jump Table (bytes 0x00-0x34 / 0-52)

Valid operations (others cause failure):

| Byte | ASCII | Hex  | Operation |
|------|-------|------|-----------|
| 0x00 | NUL   | 0x00 | Pop value from input stack → rbx->0x08 |
| 0x01 |       | 0x01 | Clear output (xor eax, eax) |
| 0x10 |       | 0x10 | Duplicate top value |
| 0x11 |       | 0x11 | Decrement pointer (subq $0x2) |
| 0x12 |       | 0x12 | Add: top[-2] += top[-4] |
| 0x13 |       | 0x13 | Subtract: top[-4] -= top[-2] |
| 0x14 |       | 0x14 | Swap top[-4] and top[-2] |
| 0x20 | ' '   | 0x20 | Pop from input, push to output |
| 0x21 | '!'   | 0x21 | Pop from output, push to input |
| 0x30 | '0'   | 0x30 | Pop from input stack, set counter |
| 0x31 | '1'   | 0x31 | Check condition: fail if top[-4] != 0 |
| 0x32 | '2'   | 0x32 | Check condition: fail if top[-4] == 0 |
| 0x33 | '3'   | 0x33 | Check condition: fail if top[-4] >= 0 |
| 0x34 | '4'   | 0x34 | Check condition: fail if top[-4] <= 0 |

#### Special High-Byte Operations (0xC0+)

- 0xC0 (-64): Call function pointer at rbx->0x20
- 0xBF (-65): Complex multi-byte instruction parsing
- 0x80 (-128): Call function pointer at rbx->0x20 with argument
- 0x81 (-127): Signed byte instruction

The language appears to manipulate two stacks (input at rbx->0x10, output at rbx->0x18) and performs arithmetic/logical operations on 16-bit values stored on these stacks.

### Key Observations

1. **Two-stack model:** Input stack (rax from rbx->0x10) and output stack (rax from rbx->0x18)
2. **16-bit operations:** Uses word (16-bit) values for stack elements
3. **Conditional verification:** Multiple condition checks ensure the program meets specific requirements
4. **Function callbacks:** Uses function pointers at rbx->0x20 and rbx->0x28 for dynamic behavior
5. **Error handling:** Sets error flag if conditions fail; returns "Have a flag!" on error

### Verification Logic

The program checks:
1. Stack values must meet specific conditions at various points
2. Operations must not underflow or overflow the stacks
3. The exact sequence of operations matters for verification

## Solution Approach

The challenge requires finding the correct sequence of operations in this custom language that:
1. Passes all stack condition checks
2. Produces the expected output
3. Allows the program to read and output the flag

### Program Verification Logic

Key findings from dynamic testing:
- The program reads commands from stdin in a loop (0x1178)
- Each command is interpreted via jump table at 0x201c
- Invalid commands set error flag at 0x13e7
- Program exits when counter at offset 0xe(rsp) reaches 0
- Success condition: byte at 0xc(rsp) must be 0 and word at 0xe(rsp) must be 0

### Stack Operations

The interpreter uses two stacks:
- **Input stack** (pointer at rbx->0x10): receives values from commands
- **Output stack** (pointer at rbx->0x18): stores results
- All values are 16-bit (word-sized)
- Stack grows downward in memory

### Solution Strategy

This requires:
1. **Reverse engineering** of the condition tree (commands 1,2,3,4 form decision points)
2. **Constraint solving** to find a sequence that satisfies all conditions
3. **Stack analysis** to understand the expected state transitions
4. Possible **automated search** or manual trace through the decision tree

Test results show:
- Commands '0' and '1' together (sequence "01") pass initial checks
- Pattern suggests a binary decision tree structure
- Flag is read from `flag.txt` upon successful verification

## Files

- `matrix` - The main binary (ELF executable)
- `matrix_disasm.txt` - Full disassembly (reference)
- `README.md` - This file

## Tools Used

- `objdump` - Binary disassembly and analysis
- `strings` - String extraction
- `file` - File type identification
- Python - Data analysis and offset calculation

## References

- **CyLab Challenge:** https://learn.cylabacademy.org/library/221/
- **Challenge Command:** `nc mars.cylabacademy.net 31259`
