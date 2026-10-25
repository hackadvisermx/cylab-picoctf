#!/usr/bin/env python3
"""
Solver for MATRIX (CyLab ID 221 / picoMini by redpwn)
Extracts the embedded VM bytecode, maps the 16x16 maze,
solves it with BFS (including key farming), and submits the solution.
"""

import socket
import struct
import time
from collections import deque

HOST = "mars.cylabacademy.net"
PORT = 31259

def extract_maze(binary_path="matrix"):
    with open(binary_path, "rb") as f:
        data = f.read()

    # Bytecode is at offset 0x20f0 in .rodata
    bytecode = data[0x20f0:0x26c2]
    table_start = 0x0174

    maze = {}
    for y in range(16):
        for x in range(16):
            idx = y * 16 + x
            pos = table_start + idx * 4
            chunk = bytecode[pos:pos+4]
            if chunk[0] == 0x81 and chunk[3] == 0x30:
                target = struct.unpack("<H", chunk[1:3])[0]
                if target == 0x00fb:
                    maze[(x, y)] = '#'  # Wall / Grue
                elif target == 0x057f:
                    maze[(x, y)] = 'K'  # Key (+1 key)
                elif target == 0x0574:
                    maze[(x, y)] = 'D'  # Door (-1 key, grue if 0)
                elif target == 0x0585:
                    maze[(x, y)] = 'G'  # Goal / Exit
            elif chunk[0] == 0x30:
                maze[(x, y)] = '.'      # Empty passage
    return maze

def solve_maze(maze):
    # State: (x, y, keys)
    # Start at (1, 1) with 0 keys
    queue = deque([(1, 1, 0, "")])
    visited = set([(1, 1, 0)])

    moves = [
        ('u', 0, -1),
        ('d', 0, 1),
        ('l', -1, 0),
        ('r', 1, 0),
    ]

    while queue:
        x, y, k, path = queue.popleft()
        if maze.get((x, y)) == 'G':
            return path

        for move_ch, dx, dy in moves:
            nx, ny = x + dx, y + dy
            cell = maze.get((nx, ny), '#')
            if cell == '#':
                continue
            nk = k
            if cell == 'K':
                nk = k + 1
            elif cell == 'D':
                if k == 0:
                    continue
                nk = k - 1

            if nk > 10:  # Avoid infinite key farming
                continue

            state = (nx, ny, nk)
            if state not in visited:
                visited.add(state)
                queue.append((nx, ny, nk, path + move_ch))
    return None

def main():
    print("[*] Extracting maze from matrix binary...")
    maze = extract_maze("matrix")
    
    print("[*] Finding shortest path via BFS...")
    path = solve_maze(maze)
    print(f"[+] Found solution path ({len(path)} moves): {path}")

    print(f"[*] Connecting to {HOST}:{PORT}...")
    s = socket.create_connection((HOST, PORT), timeout=10)
    time.sleep(0.5)
    banner = s.recv(4096).decode(errors="replace")
    print(banner.strip())

    print("[*] Sending moves...")
    s.sendall(path.encode() + b"\n")
    time.sleep(1)
    response = s.recv(4096).decode(errors="replace")
    print(response.strip())
    s.close()

if __name__ == "__main__":
    main()
