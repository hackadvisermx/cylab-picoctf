#!/usr/bin/env python3
"""Simple JITFP solver - test one character at a time"""

import subprocess
import time

def test_flag(host, port, username, password, flag):
    """Test a single flag"""
    cmd = f"sshpass -p '{password}' ssh -p {port} -o ConnectTimeout=2 -o StrictHostKeyChecking=no {username}@{host} './ad7e550b \"{flag}\" 2>&1' 2>/dev/null"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=6)
        return result.stdout + result.stderr
    except:
        return ""

HOST = "chatelaine.cylabacademy.net"
PORT = 46499
USERNAME = "ctf-player"
PASSWORD = "d137d16e"

current = "academy{"
charset = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-}@#$%^&*!")

print(f"[*] Start: {current}")

for pos in range(1, 50):
    print(f"\n[Position {pos}]")
    best_char = None
    best_output = ""
    best_score = -1

    for i, char in enumerate(charset):
        test_str = current + char
        output = test_flag(HOST, PORT, USERNAME, PASSWORD, test_str)

        # Check for success
        if "Correct" in output:
            print(f"SUCCESS: {test_str}")
            print(output)
            exit(0)

        # Count asterisks
        stars = output.count('*')
        lines = output.count('\n')

        if stars > best_score:
            best_score = stars
            best_char = char
            best_output = output
            status = "BEST"
        else:
            status = ""

        print(f"  [{i+1:2d}] '{char}': {stars:2d} stars, {lines:2d} lines {status}")

        # Small delay to avoid overwhelming SSH
        time.sleep(0.1)

    if best_char:
        current += best_char
        print(f"\n[+] Selected '{best_char}' -> {current}")
    else:
        print(f"[-] No character advanced the flag")
        break

print(f"\n[Final] {current}")
