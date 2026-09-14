import "pe"

rule YaraRules0x100_Suspicious
{
    meta:
        author = "solver"
        description = "Detects self-debugging anti-analysis malware sample (packed or unpacked)"

    condition:
        uint16(0) == 0x5A4D and
        (
            (
                pe.imports("KERNEL32.DLL", "DebugActiveProcess") and
                pe.imports("KERNEL32.DLL", "DebugActiveProcessStop") and
                pe.imports("KERNEL32.DLL", "IsDebuggerPresent") and
                pe.imports("KERNEL32.DLL", "CreateToolhelp32Snapshot") and
                pe.imports("KERNEL32.DLL", "Process32NextW") and
                pe.imports("KERNEL32.DLL", "CreateMutexW") and
                pe.imports("ADVAPI32.dll", "AdjustTokenPrivileges") and
                pe.imports("ADVAPI32.dll", "LookupPrivilegeValueW")
            )
            or
            (
                pe.section_index("UPX0") >= 0 and
                pe.section_index("UPX1") >= 0
            )
        )
}
