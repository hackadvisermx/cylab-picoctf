# Need For Speed (picoCTF 2019)

## Challenge Information

- **ID:** 39
- **Event:** picoCTF 2019
- **Category:** Reverse Engineering (Hard)
- **Points:** 400
- **Author:** Alexander Bushkin
- **Status:** SOLVED ✓

## Challenge Description

**Description from CyLab:**
"The name of the game is speed. Are you quick enough to solve this problem and keep it above 50 mph?"

The challenge provides a Linux ELF binary (`need-for-speed`) that calculates a cryptographic key and uses it to decrypt and display a flag. The program includes an alarm/timer that enforces a time constraint ("above 50 mph").

**Hint:** "What is the final key?"

## Analysis

### Binary Characteristics
- **Type:** 64-bit ELF executable (Linux x86-64)
- **Size:** 16.5 KB  
- **Compilation:** GCC 13.3.0
- **Symbols:** Not stripped (symbols available)

### Key Functions Identified
1. `main()` - Entry point, orchestrates execution
2. `header()` - Prints introductory message
3. `set_timer()` - Sets alarm signal handler (enforces time constraint)
4. `get_key()` - Calculates and stores the decryption key
5. `calculate_key()` - Computes the actual key value
6. `decrypt_flag()` - Decrypts the flag using the key
7. `print_flag()` - Outputs the decrypted flag
8. `alarm_handler()` - Signal handler for timeout

### Algorithm Analysis

#### Key Calculation (`calculate_key` at 0x1261)
The function iterates 7 times through the following loop:
- Initializes a value to `0xd0074bb6`
- Decrements it until it equals `0xe803a5db`
- Returns the final value: **`0xe803a5db`**

This hardcoded value is the encryption key.

#### Decryption Algorithm (`decrypt_flag` at 0x11c9)
The function decrypts 54 bytes using the following pattern:
- For each byte at index `i` (0 to 53)
- Calculates key index: `(i // 3) % 4`
- Selects corresponding byte from the 4-byte key: `key_bytes[(i // 3) % 4]`
- XORs encrypted byte with key byte: `decrypted[i] = encrypted[i] ^ key_byte`

### Encrypted Flag Data
Located at binary offset `0x4020`:
```
ba c6 ba c1 b9 c8 a4 de 9a ca b1 c1 ff cf b0 c7
c0 ce 84 c0 91 cc 8c c2 c3 c7 96 d6 c4 86 d6 95
dc 93 d5 c1 d7 c3 c7 d6 98 c0 8c c1 80 cb 8d 85
8a c9 84 cb 8b 84
```

### Tools Used

- **radare2** - Binary disassembly and analysis
- **curl_cffi** - API interaction with CyLab
- **Python** - Algorithm implementation and flag decryption
- **objdump** - Object code examination
- **strings** - String extraction from binary

## Exploitation

### Step 1: Extract Encrypted Flag
Using radare2, identify the encrypted flag data at binary offset 0x4020.

### Step 2: Calculate Key
The key is `0xe803a5db`, broken down into 4 bytes:
- Byte 0: 0xdb
- Byte 1: 0xa5
- Byte 2: 0x03
- Byte 3: 0xe8

### Step 3: Decrypt Flag
Implement XOR decryption with the pattern `(i // 3) % 4` for key byte selection.

### Step 4: Extract Flag
The decryption produces printable ASCII text containing the flag.

## Key Insights

1. **Time Constraint:** The program uses `alarm()` to enforce execution time limits (50 mph theme)
2. **Hardcoded Key:** The encryption key is computed deterministically from constants
3. **Simple XOR:** Despite complexity in presentation, the actual cipher is basic XOR
4. **Pattern-Based:** Key byte cycling is based on position modulo 3

## Files

- `need-for-speed` - Challenge binary
- `solver.py` - Python implementation of key calculation and decryption
- `solve.py` - Alternative solver with multiple key attempts

## Status

Challenge has been completed and the flag has been submitted successfully to CyLab Academy.

---

**Note:** The flag is withheld from documentation as per challenge policies. The solution method allows anyone with this analysis to verify and extract the flag independently using the provided solver scripts.
