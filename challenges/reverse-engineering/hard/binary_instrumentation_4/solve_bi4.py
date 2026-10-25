#!/usr/bin/env python3
"""
Binary Instrumentation 4 - Solver Script
Challenge: Extract flag from interactive binary using Frida instrumentation
Author: Security Analysis
Date: 2026-10-24

Prerequisites:
- Python 3.7+
- frida and frida-tools: pip install frida frida-tools
- Wine (Linux/macOS) or native Windows environment
- Binary: bin-ins.exe (extract from bin-ins4.zip with password 'academy')

Usage:
    python3 solve_bi4.py [--wine] [--frida] [--static]
"""

import subprocess
import sys
import time
import json
import re
from pathlib import Path

class BinaryInstrumentation4:
    """Solver for Binary Instrumentation 4 challenge"""

    def __init__(self, binary_path="bin-ins.exe", hook_script="hook_compare.js"):
        self.binary = Path(binary_path)
        self.hook_script = Path(hook_script)
        self.flag = None
        self.all_comparisons = []
        self.test_inputs = [
            "Darkraicg492",  # Author name
            "darkraicg492",  # Lowercase
            "academy",
            "picoctf",
            "student",
            "user",
            "admin",
            "test",
            "flag",
        ]

    def check_prerequisites(self):
        """Verify required tools are installed"""
        tools = {
            "Frida": ["frida", "--version"],
            "Wine (optional)": ["wine", "--version"],
        }

        print("[*] Checking prerequisites...")
        for tool_name, cmd in tools.items():
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=5)
                if result.returncode == 0:
                    print(f"[+] {tool_name}: OK")
                    return True
            except FileNotFoundError:
                if "optional" not in tool_name:
                    print(f"[-] {tool_name}: NOT FOUND")
                    return False
            except Exception as e:
                print(f"[-] {tool_name}: {e}")

        return True

    def run_with_wine(self, test_input=None):
        """Run binary with Wine and test input"""
        if not self.binary.exists():
            print(f"[-] Binary not found: {self.binary}")
            return None

        print(f"\n[*] Running with Wine: input='{test_input}'")

        try:
            proc = subprocess.Popen(
                ["wine", str(self.binary)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = proc.communicate(
                input=(test_input + "\n") if test_input else None,
                timeout=5
            )

            print("[+] Output:")
            print(stdout)

            if stderr and not "WINE" in stderr:
                print("[!] Stderr:", stderr)

            # Check for flag
            if "academy{" in stdout or "picoCTF{" in stdout:
                print("[+] FLAG FOUND!")
                return stdout

            return stdout

        except subprocess.TimeoutExpired:
            proc.kill()
            print("[-] Timeout (process took too long)")
            return None
        except FileNotFoundError:
            print("[-] Wine not found. Install with: brew install wine")
            return None
        except Exception as e:
            print(f"[-] Error: {e}")
            return None

    def run_with_frida(self):
        """Run binary with Frida instrumentation"""
        if not self.hook_script.exists():
            print(f"[-] Hook script not found: {self.hook_script}")
            return False

        print(f"\n[*] Setting up Frida instrumentation...")
        print(f"[*] Using hook script: {self.hook_script}")
        print(f"[*] Binary: {self.binary}")

        try:
            # Command to attach Frida to process
            cmd = [
                "frida",
                "-n", str(self.binary),
                "-l", str(self.hook_script)
            ]

            print(f"[*] Command: {' '.join(cmd)}")
            print("[*] Waiting for binary to run (will timeout in 30 seconds)...")
            print("[*] Provide input when prompted by the binary\n")

            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Wait and capture output
            try:
                stdout, stderr = proc.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                print("[!] Timeout reached (expected for interactive binary)")
                proc.kill()
                stdout, _ = proc.communicate()

            print("[+] Frida output:")
            print(stdout)

            if stderr:
                print("[!] Stderr:", stderr)

            # Parse output for comparisons
            self.parse_frida_output(stdout)

            return True

        except FileNotFoundError:
            print("[-] Frida not found. Install with: pip install frida frida-tools")
            return False
        except Exception as e:
            print(f"[-] Error: {e}")
            return False

    def parse_frida_output(self, output):
        """Extract comparisons from Frida output"""
        print("\n[*] Parsing Frida output...")

        # Look for comparison patterns
        pattern = r"\[(strcmp|lstrcmp[AW]?|strcmpi)\].*?(?:Left|'.*?'.*?Right|'.*?')"

        matches = re.findall(pattern, output)
        if matches:
            print(f"[+] Found {len(matches)} comparisons")

        # Look for MATCH patterns
        matches = re.findall(r"\[\+\] MATCH FOUND!", output)
        if matches:
            print(f"[+++] Found {len(matches)} MATCH results!")

        # Look for flag patterns
        flag_pattern = r"(academy\{[^}]*\}|picoCTF\{[^}]*\}|flag\{[^}]*\})"
        flags = re.findall(flag_pattern, output)
        if flags:
            print(f"\n[+++] POTENTIAL FLAGS FOUND:")
            for flag in set(flags):
                print(f"      {flag}")
                self.flag = flag

    def run_static_analysis(self):
        """Perform static analysis with radare2"""
        print("\n[*] Running static analysis with radare2...")

        try:
            result = subprocess.run(
                ["radare2", "-q", "-c", "aaa;izz~academy", str(self.binary)],
                capture_output=True,
                text=True,
                timeout=10
            )

            print("[+] String analysis:")
            print(result.stdout)

        except FileNotFoundError:
            print("[-] radare2 not found (optional tool)")
        except Exception as e:
            print(f"[-] Error in static analysis: {e}")

    def solve(self, method="wine"):
        """Main solver logic"""
        print("=" * 60)
        print("Binary Instrumentation 4 - Solver")
        print("=" * 60)

        if not self.check_prerequisites():
            print("\n[-] Missing required tools")
            return False

        if method == "frida":
            return self.run_with_frida()

        elif method == "wine":
            print("\n[*] Method: Wine + Test Inputs")
            print(f"[*] Will test {len(self.test_inputs)} different inputs\n")

            for test_input in self.test_inputs:
                output = self.run_with_wine(test_input)

                if output and ("academy{" in output or "picoCTF{" in output):
                    self.flag = output
                    return True

                time.sleep(0.5)  # Brief pause between attempts

            return False

        elif method == "static":
            self.run_static_analysis()
            return False

        return False

    def export_results(self):
        """Export results to file"""
        results = {
            "binary": str(self.binary),
            "method": "Frida instrumentation / Wine testing",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "flag": self.flag,
            "all_comparisons": self.all_comparisons
        }

        output_file = "bi4_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n[+] Results exported to: {output_file}")

    def main(self):
        """Main execution"""
        import argparse

        parser = argparse.ArgumentParser(
            description="Binary Instrumentation 4 Solver",
            epilog="Examples:\n"
                   "  python3 solve_bi4.py --wine\n"
                   "  python3 solve_bi4.py --frida\n"
                   "  python3 solve_bi4.py --static"
        )

        parser.add_argument(
            "--wine", action="store_true",
            help="Run with Wine + test inputs (Linux/macOS)"
        )
        parser.add_argument(
            "--frida", action="store_true",
            help="Run with Frida instrumentation (recommended)"
        )
        parser.add_argument(
            "--static", action="store_true",
            help="Run static analysis only"
        )
        parser.add_argument(
            "--binary", default="bin-ins.exe",
            help="Path to binary (default: bin-ins.exe)"
        )

        args = parser.parse_args()

        # Update binary path
        self.binary = Path(args.binary)

        # Determine method
        method = "wine"  # Default
        if args.frida:
            method = "frida"
        elif args.static:
            method = "static"

        # Run solver
        success = self.solve(method)

        print("\n" + "=" * 60)
        if self.flag:
            print(f"[+] SUCCESS! Flag found:")
            print(f"    {self.flag}")
        else:
            print("[-] Flag not found")
            print("[*] Try:")
            print("    - Run manually with: wine bin-ins.exe")
            print("    - Try input: Darkraicg492 (author name)")
            print("    - Use Frida for detailed instrumentation")
        print("=" * 60)

        self.export_results()

        return success


if __name__ == "__main__":
    solver = BinaryInstrumentation4()
    sys.exit(0 if solver.main() else 1)
