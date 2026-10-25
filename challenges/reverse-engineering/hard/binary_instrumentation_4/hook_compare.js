// Binary Instrumentation 4 - Frida Hook Script
// Hookea funciones de comparación de strings para extraer la flag
// Autor: Security Analysis
// Fecha: 2026-10-24

var Module = require("frida").Module;

console.log("[+] Binary Instrumentation 4 - Frida Hook Script");
console.log("[*] Target: Hook compare functions to extract flag");

// Almacenar strings para análisis posterior
var allComparisons = [];
var flagCandidates = [];

// === HOOK STRCMP ===
try {
    var strcmpAddr = Module.findExportByName("msvcrt", "strcmp");
    if (strcmpAddr) {
        Interceptor.attach(strcmpAddr, {
            onEnter: function(args) {
                try {
                    var str1 = Memory.readUtf8String(args[0]);
                    var str2 = Memory.readUtf8String(args[1]);

                    console.log("\n[strcmp]");
                    console.log("  Left:  '" + str1 + "'");
                    console.log("  Right: '" + str2 + "'");

                    allComparisons.push({
                        func: "strcmp",
                        left: str1,
                        right: str2
                    });
                } catch(e) {
                    console.log("[strcmp] Error reading strings: " + e.message);
                }
            },
            onLeave: function(retval) {
                if (retval == 0) {
                    console.log("  [+] MATCH FOUND!");
                }
            }
        });
        console.log("[+] strcmp hooked");
    }
} catch(e) {
    console.log("[-] strcmp hook failed: " + e.message);
}

// === HOOK lstrcmpA (ANSI) ===
try {
    var lstrcmpA_Addr = Module.findExportByName("kernel32.dll", "lstrcmpA");
    if (lstrcmpA_Addr) {
        Interceptor.attach(lstrcmpA_Addr, {
            onEnter: function(args) {
                try {
                    var str1 = Memory.readUtf8String(args[0]);
                    var str2 = Memory.readUtf8String(args[1]);

                    console.log("\n[lstrcmpA]");
                    console.log("  Left:  '" + str1 + "'");
                    console.log("  Right: '" + str2 + "'");

                    allComparisons.push({
                        func: "lstrcmpA",
                        left: str1,
                        right: str2
                    });

                    // Capture potential inputs
                    if (str1.length > 3) {
                        flagCandidates.push(str1);
                    }
                    if (str2.length > 3) {
                        flagCandidates.push(str2);
                    }
                } catch(e) {}
            },
            onLeave: function(retval) {
                if (retval == 0) {
                    console.log("  [+] MATCH FOUND!");
                }
            }
        });
        console.log("[+] lstrcmpA hooked");
    }
} catch(e) {
    console.log("[-] lstrcmpA hook failed: " + e.message);
}

// === HOOK lstrcmpW (UNICODE) ===
try {
    var lstrcmpW_Addr = Module.findExportByName("kernel32.dll", "lstrcmpW");
    if (lstrcmpW_Addr) {
        Interceptor.attach(lstrcmpW_Addr, {
            onEnter: function(args) {
                try {
                    var str1 = Memory.readUtf16String(args[0]);
                    var str2 = Memory.readUtf16String(args[1]);

                    console.log("\n[lstrcmpW]");
                    console.log("  Left:  '" + str1 + "'");
                    console.log("  Right: '" + str2 + "'");

                    allComparisons.push({
                        func: "lstrcmpW",
                        left: str1,
                        right: str2
                    });

                    if (str1.length > 3) {
                        flagCandidates.push(str1);
                    }
                    if (str2.length > 3) {
                        flagCandidates.push(str2);
                    }
                } catch(e) {}
            },
            onLeave: function(retval) {
                if (retval == 0) {
                    console.log("  [+] MATCH FOUND!");
                }
            }
        });
        console.log("[+] lstrcmpW hooked");
    }
} catch(e) {
    console.log("[-] lstrcmpW hook failed: " + e.message);
}

// === HOOK strcmpi (CASE-INSENSITIVE) ===
try {
    var strcmpi_Addr = Module.findExportByName("msvcrt", "strcmpi");
    if (strcmpi_Addr) {
        Interceptor.attach(strcmpi_Addr, {
            onEnter: function(args) {
                try {
                    var str1 = Memory.readUtf8String(args[0]);
                    var str2 = Memory.readUtf8String(args[1]);

                    console.log("\n[strcmpi]");
                    console.log("  Left:  '" + str1 + "'");
                    console.log("  Right: '" + str2 + "'");

                    allComparisons.push({
                        func: "strcmpi",
                        left: str1,
                        right: str2
                    });
                } catch(e) {}
            },
            onLeave: function(retval) {
                if (retval == 0) {
                    console.log("  [+] MATCH FOUND!");
                }
            }
        });
        console.log("[+] strcmpi hooked");
    }
} catch(e) {
    console.log("[-] strcmpi hook failed: " + e.message);
}

// === HOOK MessageBoxA (Possible flag display) ===
try {
    var msgBoxA_Addr = Module.findExportByName("user32.dll", "MessageBoxA");
    if (msgBoxA_Addr) {
        Interceptor.attach(msgBoxA_Addr, {
            onEnter: function(args) {
                try {
                    // args[1] is LPCSTR lpText
                    var text = Memory.readUtf8String(args[1]);
                    console.log("\n[MessageBoxA]");
                    console.log("  Text: '" + text + "'");

                    // Check if contains flag
                    if (text.indexOf("academy{") !== -1 ||
                        text.indexOf("picoCTF{") !== -1 ||
                        text.indexOf("flag{") !== -1) {
                        console.log("  [+++] POTENTIAL FLAG FOUND!");
                        flagCandidates.push(text);
                    }
                } catch(e) {}
            }
        });
        console.log("[+] MessageBoxA hooked");
    }
} catch(e) {
    console.log("[-] MessageBoxA hook failed: " + e.message);
}

// === HOOK MessageBoxW (Unicode version) ===
try {
    var msgBoxW_Addr = Module.findExportByName("user32.dll", "MessageBoxW");
    if (msgBoxW_Addr) {
        Interceptor.attach(msgBoxW_Addr, {
            onEnter: function(args) {
                try {
                    // args[1] is LPCWSTR lpText
                    var text = Memory.readUtf16String(args[1]);
                    console.log("\n[MessageBoxW]");
                    console.log("  Text: '" + text + "'");

                    if (text.indexOf("academy{") !== -1 ||
                        text.indexOf("picoCTF{") !== -1 ||
                        text.indexOf("flag{") !== -1) {
                        console.log("  [+++] POTENTIAL FLAG FOUND!");
                        flagCandidates.push(text);
                    }
                } catch(e) {}
            }
        });
        console.log("[+] MessageBoxW hooked");
    }
} catch(e) {
    console.log("[-] MessageBoxW hook failed: " + e.message);
}

// === EXPORT DATA ===
rpc.exports = {
    getAllComparisons: function() {
        return allComparisons;
    },
    getFlagCandidates: function() {
        return flagCandidates;
    },
    getStats: function() {
        return {
            totalComparisons: allComparisons.length,
            candidateStrings: flagCandidates.length,
            potentialFlags: flagCandidates.filter(function(s) {
                return s.indexOf("{") !== -1;
            })
        };
    }
};

console.log("[*] All hooks installed successfully");
console.log("[*] Run the binary and provide input when prompted");
console.log("[*] Watch for [+] MATCH FOUND! messages");
console.log("[*] All comparisons are being logged above");
console.log("[+] Hook installation complete\n");
