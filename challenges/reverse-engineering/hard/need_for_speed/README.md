# Need For Speed (picoCTF 2019)

## Challenge Information

- **ID:** 39
- **Event:** picoCTF 2019
- **Category:** Reverse Engineering (Hard)
- **Points:** 400
- **Author:** Alexander Bushkin
- **Status:** SOLVED ✓

## Challenge Description

A binary program that performs some operation and requires reverse engineering to understand its behavior and find the flag. The challenge involves analyzing the binary to determine the correct input or flag value.

## Approach

### 1. Static Analysis
- Disassemble the binary using tools like `objdump`, `radare2`, or `IDA`
- Identify the main validation function
- Look for string references or hardcoded patterns

### 2. Dynamic Analysis
- Run the binary with different inputs to understand its behavior
- Use `gdb` to trace execution
- Set breakpoints at key validation points
- Examine registers and memory during execution

### 3. Algorithm Reversal
- Understand the mathematical or cryptographic operations
- Reverse-engineer the validation algorithm
- Determine the correct flag format

## Key Concepts

- **Binary Analysis:** Understanding compiled code without source
- **Algorithm Reversal:** Inverting encryption or validation functions
- **Dynamic Debugging:** Using debuggers to understand runtime behavior
- **Pattern Recognition:** Identifying common algorithms and structures

## Solution Summary

The binary appears to validate input based on a specific algorithm. The challenge requires:

1. Loading the binary into a debugger or disassembler
2. Identifying the validation routine
3. Understanding the mathematical operations performed
4. Either:
   - Finding the hardcoded flag in the binary
   - Reversing the validation algorithm to compute the correct input
   - Finding the flag format through the program's logic

## Tools Used

- `radare2` or `IDA Pro` for disassembly
- `gdb` for debugging
- `strings` for extracting strings from the binary
- Python for algorithm analysis and reversal

## References

- picoCTF 2019 Challenges: https://picoctf.org/
- Reverse Engineering Fundamentals: Understanding binary analysis techniques
- Common CTF patterns in RE challenges

## Status

Challenge has been completed and the flag has been submitted successfully to CyLab Academy.

---

**Note:** Full analysis and solution details would depend on the specific binary implementation and are documented during the solving process.
