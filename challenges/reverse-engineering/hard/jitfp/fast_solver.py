#!/usr/bin/env python3
"""Fast JITFP solver using observed behavior"""

import subprocess
import sys

def test_flag(host, port, username, password, flag):
    """Test a flag against the remote binary"""
    try:
        cmd = [
            "sshpass", "-p", password, "ssh", "-p", str(port),
            f"{username}@{host}", "-o", "StrictHostKeyChecking=no",
            f"timeout 3 ./ad7e550b '{flag}' 2>&1"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        output = (result.stdout + result.stderr).strip()
        return output
    except:
        return ""

def count_asterisks(output):
    """Count asterisks in output"""
    for line in output.split('\n'):
        if line.startswith('*'):
            return len(line)
    return 0

def solve():
    HOST = "chatelaine.cylabacademy.net"
    PORT = 46499
    USERNAME = "ctf-player"
    PASSWORD = "d137d16e"

    current = "academy{"
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-}"

    print(f"[*] Starting solver...")
    print(f"[*] Current: {current}")

    for pos in range(1, 50):
        print(f"\n[*] Position {pos}: Finding character for '{current}?'")

        best_char = None
        best_score = -1

        for char in charset:
            test_str = current + char
            output = test_flag(HOST, PORT, USERNAME, PASSWORD, test_str)

            if "Correct" in output:
                print(f"[+] FOUND CORRECT: {test_str}")
                return test_str

            score = count_asterisks(output)

            if score > best_score:
                best_score = score
                best_char = char
                print(f"  {char}: {score} stars (BEST)")
            elif score > 0:
                print(f"  {char}: {score} stars")

        if best_char:
            current += best_char
            print(f"[+] Selected '{best_char}' -> {current}")

            # Verify it's still getting progress
            output = test_flag(HOST, PORT, USERNAME, PASSWORD, current)
            if "Correct" in output:
                print(f"[+] COMPLETE: {current}")
                return current
        else:
            print(f"[-] No progress found")
            break

    return None

if __name__ == "__main__":
    flag = solve()
    if flag:
        print(f"\n[+] SOLUTION: {flag}")
    else:
        print(f"\n[-] Failed to solve")
