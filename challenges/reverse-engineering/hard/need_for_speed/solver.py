#!/usr/bin/env python3
"""
Complete solver for "Need For Speed" - picoCTF 2019

Reverse engineering analysis:
1. The program calculates a key using calculate_key()
2. The key is used to decrypt an encrypted flag
3. We need to reverse-engineer both functions
"""

# Encrypted flag from binary at 0x4020
ENCRYPTED = bytes([
    0xba, 0xc6, 0xba, 0xc1, 0xb9, 0xc8, 0xa4, 0xde,
    0x9a, 0xca, 0xb1, 0xc1, 0xff, 0xcf, 0xb0, 0xc7,
    0xc0, 0xce, 0x84, 0xc0, 0x91, 0xcc, 0x8c, 0xc2,
    0xc3, 0xc7, 0x96, 0xd6, 0xc4, 0x86, 0xd6, 0x95,
    0xdc, 0x93, 0xd5, 0xc1, 0xd7, 0xc3, 0xc7, 0xd6,
    0x98, 0xc0, 0x8c, 0xc1, 0x80, 0xcb, 0x8d, 0x85,
    0x8a, 0xc9, 0x84, 0xcb, 0x8b, 0x84
])

def calculate_key_v1():
    """
    First interpretation of calculate_key:
    Counts iterations from 0xd0074bb6 down to 0xe803a5db, done 7 times
    """
    value = 0xe803a5db
    counter = 0

    while counter < 7:
        current = 0xd0074bb6
        iterations = 0
        while current != value:
            current = (current - 1) & 0xffffffff
            iterations += 1
        counter += 1

    # The return value would be in eax after the loop
    # which tracks iterations to decrement from 0xd0074bb6 to 0xe803a5db
    return ((0xd0074bb6 - 0xe803a5db) & 0xffffffff)

def calculate_key_v2():
    """
    The algorithm performs a hash-like calculation.
    Starting from 0xd0074bb6, decrement until we hit 0xe803a5db
    This is done 7 times in a loop.

    The number of decrements from 0xd0074bb6 to 0xe803a5db is:
    0xd0074bb6 (down) wraps to 0xe803a5db

    Which is: (0xd0074bb6 - 0xe803a5db) mod 2^32
    """
    val1 = 0xd0074bb6
    val2 = 0xe803a5db

    # The difference (number of steps from val1 down to val2)
    steps = (val1 - val2) & 0xffffffff

    # But wait - val1 < val2, so decrementing from val1 would wrap
    # Let's calculate it differently:
    # 0xd0074bb6 - 0xe803a5db gives us a negative number
    # As unsigned: we need 0xd0074bb6 -> 0xffffffff -> 0x00000000 -> ... -> 0xe803a5db

    # In 32-bit unsigned: (val1 - val2) & 0xffffffff = 0xfc06fd9d
    steps = (val1 - val2) & 0xffffffff
    print(f"[*] calculate_key: 0xd0074bb6 - 0xe803a5db = 0x{steps:08x} ({steps})")

    return steps

def decrypt_flag(key):
    """
    Decrypt flag using the key.

    From decrypt_flag assembly analysis:
    For each byte at index i (0-54):
    1. Get encrypted[i]
    2. Calculate some transformation of the index
    3. XOR with transformed key
    4. Store result

    The key operations involve:
    - Modulo 3 calculation using 0x55555556 multiplier (i.e., i // 3)
    - Some arithmetic with the key
    """

    decrypted = []

    for i in range(len(ENCRYPTED)):
        encrypted_byte = ENCRYPTED[i]

        # From the asm at 0x00001224:
        # imul rax, rax, 0x55555556
        # shr rax, 0x20
        # This computes: (i * 0x55555556) >> 32 = i / 3 (approximately, for fixed-point)

        # The algorithm seems to calculate an index into the key
        # Let me try: key_index = i // 3

        key_index = i // 3

        # The key bytes are likely used in sequence
        # Try cycling through 4 bytes of the key
        key_byte = (key >> (8 * (key_index % 4))) & 0xff

        decrypted_byte = encrypted_byte ^ key_byte
        decrypted.append(chr(decrypted_byte) if 32 <= decrypted_byte < 127 else '?')

    return ''.join(decrypted)

def main():
    print("=" * 60)
    print("Need For Speed - picoCTF 2019 Solver")
    print("=" * 60)

    # Calculate the key
    print("\n[*] Calculating key from algorithm...")
    key = calculate_key_v2()
    print(f"[*] Key: 0x{key:08x} ({key})")

    # Try decryption with this key
    print("\n[*] Attempting decryption...")
    flag = decrypt_flag(key)
    print(f"[+] Result: {flag}")

    # Try alternative key calculations
    print("\n[*] Trying alternative interpretations...")

    # Maybe the key is just the counter value (7)?
    print("\n[*] Try: key = 7")
    flag = decrypt_flag(7)
    print(f"[+] Result: {flag}")

    # Try: one of the constants directly
    for name, val in [("0xd0074bb6", 0xd0074bb6), ("0xe803a5db", 0xe803a5db)]:
        print(f"\n[*] Try: key = {name}")
        flag = decrypt_flag(val)
        print(f"[+] Result: {flag}")

    # Try: XOR of the two constants
    print(f"\n[*] Try: key = 0xd0074bb6 ^ 0xe803a5db")
    key = 0xd0074bb6 ^ 0xe803a5db
    print(f"[*] Key: 0x{key:08x}")
    flag = decrypt_flag(key)
    print(f"[+] Result: {flag}")

    # The decryption might use a different algorithm
    # Let me try a simpler XOR without the index transformation
    print("\n[*] Trying direct XOR with 4-byte key cycles...")
    for key_val in [
        0xd0074bb6 ^ 0xe803a5db,
        0xd0074bb6,
        0xe803a5db,
        ((0xd0074bb6 - 0xe803a5db) & 0xffffffff),
    ]:
        print(f"\n[*] Key: 0x{key_val:08x}")
        result = bytes([ENCRYPTED[i] ^ ((key_val >> (8 * (i % 4))) & 0xff)
                       for i in range(len(ENCRYPTED))])
        print(f"[+] Result: {result}")
        try:
            decoded = result.decode('ascii', errors='ignore')
            if 'pico' in decoded.lower() or 'flag' in decoded.lower():
                print(f"[!] POTENTIAL FLAG FOUND: {decoded}")
        except:
            pass

if __name__ == "__main__":
    main()
