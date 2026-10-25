#!/usr/bin/env python3
"""
Script para extraer manualmente la lista de retos de Binary Exploitation Hard desde CyLab.

Como CyLab está protegido por Cloudflare y requiere autenticación, este script proporciona
instrucciones para extraer los datos manualmente usando las herramientas del navegador.
"""

import json
from pathlib import Path
import sys

# Instrucciones de extracción manual
INSTRUCTIONS = """
==============================================================================
EXTRACCIÓN MANUAL DE RETOS DE BINARY EXPLOITATION HARD DESDE CYLAB
==============================================================================

PASO 1: Acceder a CyLab
  1. Abre https://learn.cylabacademy.org en tu navegador
  2. Inicia sesión con:
     - Usuario: hackadvisermx
     - Contraseña: [proporciona la contraseña]

PASO 2: Navegar a Binary Exploitation Hard
  1. Ve a "Challenge Library"
  2. Filtra por categoría: "Binary Exploitation"
  3. Filtra por dificultad: "Hard"

PASO 3: Extraer los datos usando la consola del navegador
  1. Abre Developer Tools (F12 o Ctrl+Shift+I)
  2. Ve a la pestaña "Console"
  3. Copia y ejecuta el siguiente código:

================== CÓDIGO A EJECUTAR EN CONSOLA ==================

const challenges = [];
const rows = document.querySelectorAll('table tbody tr, [role="row"]');

rows.forEach((row) => {
    const cells = row.querySelectorAll('td, [role="gridcell"]');
    if (cells.length > 0) {
        const name = cells[0]?.textContent?.trim() || '';
        let points = '';
        let id = '';

        for (const cell of cells) {
            const text = cell.textContent?.trim() || '';
            if (text.match(/^\\d+$/) && parseInt(text) > 0 && parseInt(text) < 1000) {
                points = text;
            }
        }

        if (name && name.length > 0) {
            challenges.push({
                nombre: name,
                puntos: points || 'Unknown',
                id: cells[1]?.textContent?.trim() || '',
                categoria: 'binary-exploitation',
                dificultad: 'hard'
            });
        }
    }
});

// Copiar al portapapeles
const json_str = JSON.stringify(challenges, null, 2);
console.log(json_str);
console.log('Copiar el JSON anterior y guardarlo en tmp/be_hard_challenges.json');
copy(json_str);

=================== FIN DEL CÓDIGO =======================

PASO 4: Guardar los datos
  1. El código anterior copia los datos al portapapeles
  2. Crea un archivo: tmp/be_hard_challenges.json
  3. Pega el contenido del portapapeles

PASO 5: Ejecutar este script de verificación
  python3 scripts/manual_cylab_extraction.py tmp/be_hard_challenges.json

==============================================================================
"""

def verify_challenges_file(filepath):
    """Verifica y procesa el archivo de retos extraído."""
    filepath = Path(filepath)

    if not filepath.exists():
        print(f"[-] Archivo no encontrado: {filepath}")
        return None

    try:
        with open(filepath, 'r') as f:
            challenges = json.load(f)

        print(f"\n[+] Archivo cargado: {filepath}")
        print(f"[+] Total de retos encontrados: {len(challenges)}\n")

        # Mostrar tabla de retos
        print("=" * 80)
        print(f"{'#':<3} {'Nombre':<40} {'Puntos':<10} {'ID':<10}")
        print("=" * 80)

        for i, ch in enumerate(challenges, 1):
            nombre = ch.get('nombre', ch.get('name', 'Unknown'))[:38]
            puntos = ch.get('puntos', ch.get('points', 'Unknown'))
            id_val = ch.get('id', '')[:8]
            print(f"{i:<3} {nombre:<40} {puntos:<10} {id_val:<10}")

        print("=" * 80)
        print(f"\nTOTAL: {len(challenges)} retos de Binary Exploitation Hard\n")

        return challenges

    except json.JSONDecodeError as e:
        print(f"[-] Error al parsear JSON: {e}")
        return None
    except Exception as e:
        print(f"[-] Error: {e}")
        return None

def main():
    """Función principal."""
    print(INSTRUCTIONS)

    # Si se proporciona un archivo, verificarlo
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        challenges = verify_challenges_file(filepath)
        if challenges:
            print("[+] ¡Listo para proceder con la resolución de retos!")
    else:
        print("\nPara usar este script con un archivo existente:")
        print("  python3 scripts/manual_cylab_extraction.py tmp/be_hard_challenges.json")

if __name__ == "__main__":
    main()
