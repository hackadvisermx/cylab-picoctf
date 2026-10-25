#!/usr/bin/env python3
"""
Solve "Need For Speed" - picoCTF 2019 Challenge
Reverse engineer the binary to find the key and decrypt the flag
"""

# Encrypted flag bytes from the binary (0x4020)
encrypted_flag = bytes([
    0xba, 0xc6, 0xba, 0xc1, 0xb9, 0xc8, 0xa4, 0xde,
    0x9a, 0xca, 0xb1, 0xc1, 0xff, 0xcf, 0xb0, 0xc7,
    0xc0, 0xce, 0x84, 0xc0, 0x91, 0xcc, 0x8c, 0xc2,
    0xc3, 0xc7, 0x96, 0xd6, 0xc4, 0x86, 0xd6, 0x95,
    0xdc, 0x93, 0xd5, 0xc1, 0xd7, 0xc3, 0xc7, 0xd6,
    0x98, 0xc0, 0x8c, 0xc1, 0x80, 0xcb, 0x8d, 0x85,
    0x8a, 0xc9, 0x84, 0xcb, 0x8b, 0x84
])

def calculate_key():
    """
    Reverse engineered key calculation from sym.calculate_key

    The algorithm:
    1. Initialize value = 0xe803a5db
    2. Initialize counter = 0
    3. Loop:
        - Set value = 0xd0074bb6 (first iteration only, then adjust)
        - Decrement value
        - If value != 0xe803a5db, increment counter
        - Loop until counter reaches 7

    Actually looking at the asm more carefully:
    - Initialize value at [rbp-8] = 0xe803a5db
    - Initialize counter at [rbp-4] = 0
    - Loop:
        - jmp 0x1291 (check counter)
        - At 0x1279: Set value = 0xd0074bb6
        - At 0x1280: Decrement value
        - At 0x1284: Compare value with 0xe803a5db
        - At 0x128b: Jump if not equal back to 0x1280
        - At 0x128d: Increment counter
        - At 0x1291: Compare counter with 7
        - At 0x1295: Jump if <= to 0x1279

    This appears to be doing some kind of hash/computation
    """

    # Let me reverse engineer this step by step
    # Based on the assembly code analysis:
    value = 0xe803a5db
    counter = 0

    while counter < 7:
        # The algorithm loops from 0xd0074bb6 down to 0xe803a5db
        current = 0xd0074bb6
        while current != 0xe803a5db:
            current -= 1
        counter += 1

    # The final value would be in eax, but based on the logic,
    # this seems to be calculating how many iterations it takes
    # to decrement from 0xd0074bb6 to 0xe803a5db

    # Let's calculate the actual difference
    diff = 0xd0074bb6 - 0xe803a5db
    print(f"Difference: {diff} (0x{diff:08x})")

    # Wait, that would be negative because 0xd0074bb6 < 0xe803a5db
    # Let me reconsider...

    # Actually, in the asm, it's comparing with 0xe803a5db
    # Let's look at this as an unsigned comparison

    # The difference is:
    # 0xd0074bb6 to 0xe803a5db (as unsigned 32-bit)
    # 0xd0074bb6 = 3502803382
    # 0xe803a5db = 3896033755
    # So 3502803382 < 3896033755, difference = 393230373

    # But the loop decrements from 0xd0074bb6, so it would go:
    # 0xd0074bb6, 0xd0074bb5, ..., 0x00000000, 0xffffffff, ...
    # wrapping around until it equals 0xe803a5db

    # In unsigned 32-bit arithmetic:
    # We need to count how many decrements to go from 0xd0074bb6 to 0xe803a5db
    # That's: 0xd0074bb6 - 0xe803a5db = 0xfc06fd9d (mod 2^32)
    # As unsigned: 4294967296 - (0xe803a5db - 0xd0074bb6) = 4294967296 - 393230373 = 3901736923

    # Let's compute it directly
    val1 = 0xd0074bb6
    val2 = 0xe803a5db

    # How many times do we decrement val1 until we get val2?
    # In modular arithmetic (mod 2^32):
    steps = (val1 - val2) & 0xffffffff
    print(f"Steps from 0x{val1:08x} to 0x{val2:08x}: {steps} (0x{steps:08x})")

    return steps

def decrypt_flag(key):
    """
    Decrypt the flag using the key

    Algorithm from sym.decrypt_flag:
    - For each byte in encrypted_flag (54 bytes)
    - Calculate: (index * 0x55555556) >> 32 - this is essentially index / 3
    - XOR with a transformed version of the key based on index
    - Result is the decrypted character
    """

    decrypted = bytearray()

    for i in range(len(encrypted_flag)):
        # Get encrypted byte
        enc_byte = encrypted_flag[i]

        # The algorithm in decrypt_flag does:
        # 1. Get encrypted[i]
        # 2. Calculate: ((i * 0x55555556) >> 32) is i // 3 (floor division)
        # 3. Use this with the index in some way
        # 4. XOR the encrypted byte with key[computed_index]

        # From the asm, it looks like:
        # - edx = i
        # - Calculate: (i * 0x55555556) >> 32, then subtract i >> 31
        # This is essentially floor(i / 3) in fixed-point arithmetic

        # Then it uses key_index = (i // 3) * 3 - i + something

        # Let me look at the exact operations:
        # sar eax, 0x1f     (sign extend)
        # add edx, eax      (add sign extension)
        # and edx, 1        (mask to get lowest bit of sign)
        # sub edx, eax      (subtract sign extension)
        # This is essentially: (i < 0 ? 2 : 0)  but i is unsigned, so result is 0

        # The key_index calculation is more complex
        # Let me try a simpler approach: iterate through algorithm

        # index_div_3 = (i * 0x55555556) >> 32
        # which is roughly i / 3

        # Then key_index = ((i // 3) * 3 - i + some_value) combined with key

        # Actually looking at line 0x1224: imul rax, rax, 0x55555556
        # This is computing i * 0x55555556, then shifting right by 32 to get i / 3

        # Let me simplify and just implement the XOR pattern
        # Based on the hint and common CTF patterns, it's likely XOR with rotating key

        key_index = i % 4  # Try cycling through 4 bytes of key
        key_byte = (key >> (8 * key_index)) & 0xff

        decrypted_byte = enc_byte ^ key_byte
        decrypted.append(decrypted_byte)

    return bytes(decrypted)

def main():
    print("Need For Speed - picoCTF 2019 Solver")
    print("=" * 50)

    # Calculate the key
    print("\n1. Calculating key...")
    key = calculate_key()
    print(f"   Key: 0x{key:08x} ({key})")

    # Try different key values
    # The key might be used differently
    print("\n2. Attempting decryption with calculated key...")
    result = decrypt_flag(key)
    print(f"   Result: {result}")

    # Try brute force if needed
    print("\n3. Trying alternative approaches...")

    # The key calculation seems complex; let me try to run the actual binary
    # or implement the exact algorithm

    # Looking at calculate_key again:
    # It seems to be counting iterations from 0xd0074bb6 down until wrapping to 0xe803a5db
    # repeated 7 times

    # Let's try a simpler interpretation:
    # Maybe it's counting how many iterations (7) until some condition
    # or it's calculating a specific value based on those constants

    # Let me try: the difference between the two values
    key_attempt2 = 0xe803a5db ^ 0xd0074bb6
    print(f"\n   Trying XOR of constants: 0x{key_attempt2:08x}")
    result2 = decrypt_flag(key_attempt2)
    print(f"   Result: {result2}")

    # Try other operations
    key_attempt3 = (0xe803a5db + 0xd0074bb6) & 0xffffffff
    print(f"\n   Trying SUM of constants: 0x{key_attempt3:08x}")
    result3 = decrypt_flag(key_attempt3)
    print(f"   Result: {result3}")

    # Try running the actual binary to get the key
    import subprocess
    print("\n4. Trying to execute the actual binary...")
    try:
        proc = subprocess.run(["./need-for-speed"],
                            capture_output=True,
                            timeout=1,
                            text=True)
        print(f"   Output: {proc.stdout}")
        print(f"   Stderr: {proc.stderr}")
    except subprocess.TimeoutExpired:
        print("   Binary timed out (alarm triggered)")
    except Exception as e:
        print(f"   Error running binary: {e}")

if __name__ == "__main__":
    main()
