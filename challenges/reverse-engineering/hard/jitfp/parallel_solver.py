#!/usr/bin/env python3
"""Parallel flag solver for JITFP"""

import subprocess
import concurrent.futures
import sys
import time

def quick_test(host, port, username, password, flag):
    """Quick test with very short timeout"""
    try:
        cmd = f"sshpass -p '{password}' ssh -p {port} -o ConnectTimeout=2 -o StrictHostKeyChecking=no {username}@{host} './ad7e550b \"{flag}\" 2>&1' 2>/dev/null"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3)
        output = result.stdout + result.stderr
        return flag, output
    except subprocess.TimeoutExpired:
        return flag, "TIMEOUT"
    except Exception as e:
        return flag, f"ERROR: {e}"

def solve():
    HOST = "chatelaine.cylabacademy.net"
    PORT = 46499
    USERNAME = "ctf-player"
    PASSWORD = "d137d16e"

    current = "academy{"
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-}!@#$%^&*()"

    print(f"[*] Starting parallel solver")
    print(f"[*] Current: {current}")

    for pos in range(1, 30):
        print(f"\n[*] Position {pos}")

        candidates = []
        for char in charset:
            test_flag_str = current + char
            candidates.append((HOST, PORT, USERNAME, PASSWORD, test_flag_str))

        results = {}

        # Test in parallel with limited workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(quick_test, *c): c[4] for c in candidates}

            for future in concurrent.futures.as_completed(futures, timeout=15):
                try:
                    flag_str, output = future.result(timeout=2)
                    results[flag_str] = output

                    if "Correct" in output:
                        print(f"[+] FOUND: {flag_str}")
                        return flag_str

                    # Show progress
                    if output.count('\n') > 1:
                        print(f"  Progress on {flag_str[-1]}: {output.count('*')} asterisks")

                except Exception as e:
                    print(f"  Error in future: {e}")

        # Find best
        best_flag = None
        best_score = -1

        for flag_str, output in results.items():
            if output == "TIMEOUT":
                continue
            score = output.count('*')
            if score > best_score:
                best_score = score
                best_flag = flag_str

        if best_flag and best_score >= 0:
            current = best_flag
            print(f"[+] Best: {current} ({best_score} asterisks)")
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
