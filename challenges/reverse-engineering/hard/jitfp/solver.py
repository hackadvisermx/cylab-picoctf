#!/usr/bin/env python3
"""
JITFP Challenge Solver - Based on observable behavior

The binary appears to verify a flag character by character.
Each character that passes verification results in more asterisks being printed.

Strategy:
1. Start with "academy{" and test characters
2. For each position, find the character that produces the most asterisks
3. The "Correct" message indicates the full flag is valid
"""

import subprocess
import time
import sys
from collections import defaultdict

def test_flag(host, port, username, password, flag, timeout=3):
    """Test a flag against the remote binary"""
    try:
        cmd = [
            "sshpass", "-p", password, "ssh", "-p", str(port),
            f"{username}@{host}", "-o", "StrictHostKeyChecking=no",
            f"timeout 2 ./ad7e550b '{flag}' 2>&1"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = (result.stdout + result.stderr).strip()
        return output
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def extract_output_info(output):
    """Parse output to determine progress"""
    lines = output.split('\n')
    last_line = lines[-1] if lines else ""

    if "Correct" in output:
        return "CORRECT", output
    elif last_line.startswith('*'):
        # Count asterisks to determine progress
        return "ASTERISKS", len(last_line)
    elif "Incorrect" in output:
        return "INCORRECT", 0
    else:
        return "UNKNOWN", output

def solve_flag(host, port, username, password, max_length=50):
    """Solve the flag using automated testing"""

    # Start with known prefix
    prefix = "academy{"
    current = prefix

    print(f"[*] Starting solver for {username}@{host}:{port}")
    print(f"[*] Known prefix: {current}")

    # Test the prefix
    output = test_flag(host, port, username, password, current)
    print(f"[*] Prefix test output lines: {len(output.split(chr(10)))}")

    # Try to find characters
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-}!@#$%^&*()"
    position = 0

    while len(current) < max_length:
        position += 1
        best_char = None
        best_score = -1
        best_output = ""

        print(f"\n[*] Position {position}: Testing characters for '{current}?'")

        for char in charset:
            test_str = current + char
            output = test_flag(host, port, username, password, test_str)

            status, score = extract_output_info(output)

            if status == "CORRECT":
                print(f"[+] FOUND CORRECT FLAG: {test_str}")
                print(output)
                return test_str

            if status == "ASTERISKS":
                if score > best_score:
                    best_score = score
                    best_char = char
                    best_output = output
                    print(f"  {char}: {score} asterisks (BEST)")
                else:
                    print(f"  {char}: {score} asterisks")
            else:
                print(f"  {char}: {status}")

        if best_char:
            current += best_char
            print(f"[+] Best character found: '{best_char}' -> '{current}'")
            print(f"[+] Output preview: {best_output[:100]}")
        else:
            print(f"[-] No better character found for position {position}")
            print("[-] Trying closing bracket '}' ...")

            test_str = current + "}"
            output = test_flag(host, port, username, password, test_str)
            status, score = extract_output_info(output)

            if status == "CORRECT":
                print(f"[+] FOUND CORRECT FLAG: {test_str}")
                print(output)
                return test_str

            if status == "ASTERISKS" and score > 0:
                current += "}"
                print(f"[+] Using '}' -> '{current}'")
            else:
                print(f"[-] Failed to find next character")
                break

    return None

if __name__ == "__main__":
    # Configuration
    HOST = "chatelaine.cylabacademy.net"
    PORT = 46499
    USERNAME = "ctf-player"
    PASSWORD = "d137d16e"

    # Run solver
    flag = solve_flag(HOST, PORT, USERNAME, PASSWORD)

    if flag:
        print(f"\n[+] SOLUTION: {flag}")
    else:
        print(f"\n[-] Could not solve the challenge")
