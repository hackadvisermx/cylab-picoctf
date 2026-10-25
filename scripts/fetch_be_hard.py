#!/usr/bin/env python3
"""
Script para obtener la lista de retos de Binary Exploitation Hard desde CyLab.
Requiere credenciales de login en un archivo .env o como argumentos de línea de comandos.
"""

import requests
import json
import sys
from pathlib import Path

# Configuración
CYLAB_URL = "https://learn.cylabacademy.org"
LOGIN_ENDPOINT = f"{CYLAB_URL}/api/auth/login"
CHALLENGES_ENDPOINT = f"{CYLAB_URL}/api/challenges"

def login(username, password):
    """Autentica con CyLab y devuelve la sesión."""
    session = requests.Session()

    # Intentar login
    login_data = {
        "username": username,
        "password": password
    }

    print(f"[*] Intentando login como {username}...")
    try:
        response = session.post(LOGIN_ENDPOINT, json=login_data, timeout=10)
        print(f"[*] Respuesta de login: {response.status_code}")

        if response.status_code == 200:
            print("[+] Login exitoso")
            return session
        else:
            print(f"[-] Login fallido: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"[-] Error al conectar: {e}")
        return None

def fetch_challenges(session, category="binary-exploitation", difficulty="hard"):
    """Obtiene la lista de retos de una categoría y dificultad específica."""
    print(f"\n[*] Obteniendo retos de {category}/{difficulty}...")

    try:
        # Intentar diferentes endpoints posibles
        endpoints = [
            f"{CHALLENGES_ENDPOINT}?category={category}&difficulty={difficulty}",
            f"{CYLAB_URL}/api/challenges/category/{category}/{difficulty}",
            f"{CYLAB_URL}/challenges/library?category={category}&difficulty={difficulty}",
        ]

        for endpoint in endpoints:
            print(f"[*] Probando: {endpoint}")
            response = session.get(endpoint, timeout=10)
            print(f"    Respuesta: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    return data
                except:
                    print(f"    No es JSON válido")
                    continue

        print("[-] No se pudo obtener la lista de retos")
        return None

    except Exception as e:
        print(f"[-] Error: {e}")
        return None

def main():
    """Función principal."""
    print("=== CyLab Challenge Fetcher ===\n")

    # Leer credenciales
    username = input("Usuario CyLab (o dejar en blanco para 'hackadvisermx'): ").strip() or "hackadvisermx"
    password = input("Contraseña: ").strip()

    if not password:
        print("[-] Contraseña requerida")
        sys.exit(1)

    # Login
    session = login(username, password)
    if not session:
        print("[-] No se pudo autenticar")
        sys.exit(1)

    # Obtener retos de BE Hard
    challenges = fetch_challenges(session)

    if challenges:
        print("\n[+] Retos obtenidos:")
        print(json.dumps(challenges, indent=2))

        # Guardar en archivo
        output_file = Path(__file__).parent.parent / "tmp" / "be_hard_challenges.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(challenges, f, indent=2)
        print(f"\n[+] Lista guardada en: {output_file}")
    else:
        print("[-] No se obtuvieron retos")
        sys.exit(1)

if __name__ == "__main__":
    main()
