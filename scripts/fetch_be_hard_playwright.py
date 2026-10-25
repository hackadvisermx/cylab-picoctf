#!/usr/bin/env python3
"""
Script para obtener la lista completa de retos de Binary Exploitation Hard desde CyLab.
Usa Playwright para automatizar el navegador.
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
import time

# Configuración
CYLAB_URL = "https://learn.cylabacademy.org"
OUTPUT_DIR = Path(__file__).parent.parent / "tmp"
OUTPUT_FILE = OUTPUT_DIR / "be_hard_challenges.json"

async def fetch_be_hard_challenges(username=None, password=None):
    """
    Obtiene la lista de retos de Binary Exploitation Hard desde CyLab.
    """
    async with async_playwright() as p:
        # Lanzar navegador (con interfaz visible)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("[*] Navegando a CyLab...")
        await page.goto(CYLAB_URL, wait_until="networkidle")

        # Dar tiempo para que cargue
        await page.wait_for_load_state("networkidle")
        time.sleep(2)

        # Verificar si ya estamos autenticados
        url = page.url
        print(f"[*] URL actual: {url}")

        # Si no estamos en la página correcta, intentar login
        if "learn.cylabacademy.org" in url and "/library" not in url:
            print("[*] No autenticado, buscando botón de login...")

            # Buscar botón de login o Sign In
            try:
                # Intentar varios selectores posibles para el botón de login
                selectors = [
                    "button:has-text('Sign In')",
                    "button:has-text('Login')",
                    "a:has-text('Sign In')",
                    "a:has-text('Login')",
                    "[data-testid='sign-in-button']",
                    ".login-button",
                ]

                login_button = None
                for selector in selectors:
                    try:
                        login_button = await page.query_selector(selector)
                        if login_button:
                            print(f"[+] Encontrado botón de login: {selector}")
                            break
                    except:
                        continue

                if login_button:
                    await login_button.click()
                    await page.wait_for_load_state("networkidle")
                    time.sleep(2)
            except Exception as e:
                print(f"[-] Error al buscar botón de login: {e}")

            # Si se proporciona usuario y contraseña, intentar login
            if username and password:
                print(f"[*] Intentando login con {username}...")
                try:
                    # Buscar campo de usuario
                    username_field = await page.query_selector("input[type='email'], input[name='username'], input[id='username']")
                    if username_field:
                        await username_field.fill(username)

                    # Buscar campo de contraseña
                    password_field = await page.query_selector("input[type='password'], input[name='password']")
                    if password_field:
                        await password_field.fill(password)

                    # Buscar botón de submit
                    submit_button = await page.query_selector("button[type='submit'], button:has-text('Sign In'), button:has-text('Login')")
                    if submit_button:
                        await submit_button.click()
                        await page.wait_for_load_state("networkidle")
                        time.sleep(2)
                        print("[+] Login completado (presumiblemente)")
                except Exception as e:
                    print(f"[-] Error durante login: {e}")
            else:
                print("[*] Esperando que el usuario inicie sesión manualmente en el navegador...")
                print("[*] (El script continuará automáticamente cuando se complete el login)")

                # Esperar a que se complete el login (detectando cambio de URL)
                start_time = time.time()
                timeout = 300  # 5 minutos
                while "/library" not in page.url and (time.time() - start_time) < timeout:
                    await page.wait_for_timeout(1000)

                if "/library" not in page.url:
                    print("[-] Timeout esperando login")
                    await browser.close()
                    return None

        # Ahora navegar a la sección de Challenge Library
        print("[*] Navegando a Challenge Library...")
        library_url = f"{CYLAB_URL}/library"
        await page.goto(library_url, wait_until="networkidle")
        await page.wait_for_load_state("networkidle")
        time.sleep(2)

        # Buscar y hacer clic en "Binary Exploitation"
        print("[*] Buscando categoría 'Binary Exploitation'...")
        try:
            # Esperar a que carguen los elementos
            await page.wait_for_selector("button, a, div", timeout=10000)

            # Buscar el botón o enlace de Binary Exploitation
            be_selector = "button:has-text('Binary Exploitation'), a:has-text('Binary Exploitation'), [data-category='binary-exploitation']"
            be_element = await page.query_selector(be_selector)

            if be_element:
                await be_element.click()
                await page.wait_for_timeout(2000)
                print("[+] Clicked Binary Exploitation")
            else:
                print("[-] No se encontró Binary Exploitation, buscando alternativas...")
        except Exception as e:
            print(f"[-] Error buscando Binary Exploitation: {e}")

        # Buscar y hacer clic en "Hard"
        print("[*] Buscando dificultad 'Hard'...")
        try:
            hard_selector = "button:has-text('Hard'), a:has-text('Hard'), [data-difficulty='hard']"
            hard_element = await page.query_selector(hard_selector)

            if hard_element:
                await hard_element.click()
                await page.wait_for_timeout(2000)
                print("[+] Clicked Hard")
            else:
                print("[-] No se encontró Hard")
        except Exception as e:
            print(f"[-] Error buscando Hard: {e}")

        # Esperar a que carguen todos los retos
        await page.wait_for_load_state("networkidle")
        time.sleep(3)

        # Extraer lista de retos
        print("[*] Extrayendo lista de retos...")

        # Script para extraer retos del DOM
        challenges = await page.evaluate("""
        () => {
            const challenges = [];
            const rows = document.querySelectorAll('table tbody tr, [role="row"], .challenge-item, .challenge-card');

            for (const row of rows) {
                // Intentar extraer nombre, ID, puntos
                const cells = row.querySelectorAll('td, [role="gridcell"], .challenge-cell');

                if (cells.length > 0) {
                    let name = cells[0]?.textContent?.trim() || '';
                    let points = '';
                    let id = '';

                    // Buscar puntos (usualmente en una columna que tenga números)
                    for (const cell of cells) {
                        const text = cell.textContent?.trim() || '';
                        if (text.match(/^\\d+$/) && parseInt(text) > 0) {
                            points = text;
                            break;
                        }
                    }

                    if (name && name.length > 0) {
                        challenges.push({
                            name: name,
                            points: points || 'Unknown',
                            id: cells[1]?.textContent?.trim() || '',
                            category: 'binary-exploitation',
                            difficulty: 'hard'
                        });
                    }
                }
            }

            return challenges;
        }
        """)

        print(f"[+] Se encontraron {len(challenges)} retos")

        # Si no se encontraron retos con el script anterior, intentar alternativa
        if len(challenges) == 0:
            print("[*] Intentando método alternativo de extracción...")
            all_text = await page.content()

            # Buscar en el HTML directamente
            import re
            # Patrón para buscar nombres de reto (simplificado)
            pattern = r'<(?:h\d|div|span|p|button)[^>]*>([^<]*(?:Heap|Overflow|Stack|ROP|PIE|ASLR|Format|Buffer|NX)[^<]*)</(?:h\d|div|span|p|button)>'
            matches = re.findall(pattern, all_text, re.IGNORECASE)

            for match in matches[:20]:  # Limitar a 20 resultados
                clean_name = match.strip()
                if len(clean_name) > 2 and len(clean_name) < 100:
                    challenges.append({
                        "name": clean_name,
                        "points": "Unknown",
                        "id": "",
                        "category": "binary-exploitation",
                        "difficulty": "hard"
                    })

        # Guardar en archivo
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(challenges, f, indent=2, ensure_ascii=False)

        print(f"[+] Lista guardada en: {OUTPUT_FILE}")
        print(f"[+] Total de retos: {len(challenges)}")

        # Mostrar primeros 10 retos
        print("\n[+] Primeros 10 retos:")
        for i, ch in enumerate(challenges[:10], 1):
            print(f"   {i}. {ch['name']} ({ch['points']} pts)")

        await browser.close()
        return challenges

async def main():
    """Función principal."""
    print("=== CyLab Binary Exploitation Hard Fetcher ===\n")

    # Intentar con credenciales vacías primero (para OAuth/Sign-In automático)
    print("[*] Iniciando Playwright...")
    challenges = await fetch_be_hard_challenges()

    if challenges and len(challenges) > 0:
        print("\n[SUCCESS] Lista de retos obtenida exitosamente")
        return challenges
    else:
        print("\n[-] No se pudieron obtener los retos")
        return None

if __name__ == "__main__":
    asyncio.run(main())
