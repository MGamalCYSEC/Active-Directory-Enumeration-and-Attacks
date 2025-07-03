# Enumerating Security Controls
## Windows Defender
Checking the Status of Defender with Get-MpComputerStatus
```powershell
Get-MpComputerStatus
```
## AppLocker
It is common for organizations to block `cmd.exe` and `PowerShell.exe` and write access to certain directories, but this can all be bypassed. Organizations also often focus on blocking the PowerShell.exe executable, but forget about the other PowerShell executable locations such as `%SystemRoot%\SysWOW64\WindowsPowerShell\v1.0\powershell.exe` or `PowerShell_ISE.exe`. 

```powershell
Get-AppLockerPolicy -Effective | select -ExpandProperty RuleCollections
```
**The default paths to the executables for PowerShell and PowerShell ISE on relevant _64-bit_ Windows operating systems:**

| 32-bit (x86) PowerShell executable     | `%SystemRoot%\SysWOW64\WindowsPowerShell\v1.0\powershell.exe`     |
| -------------------------------------- | ----------------------------------------------------------------- |
| 64-bit (x64) Powershell executable     | `%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe`     |
| 32-bit (x86) Powershell ISE executable | `%SystemRoot%\SysWOW64\WindowsPowerShell\v1.0\powershell_ise.exe` |
| 64-bit (x64) Powershell ISE executable | `%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell_ise.exe` |

**Windows PowerShell Executables File System Locations on 32-bit Windows**

The default paths to the executables for PowerShell and PowerShell ISE on relevant **32-bit** Windows operating systems:

| 32-bit (x86) PowerShell executable     | `%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe`    |
| -------------------------------------- | ---------------------------------------------------------------- |
| 32-bit (x86) Powershell ISE executable | `SystemRoot%\system32\WindowsPowerShell\v1.0\powershell_ise.exe` |


## PowerShell Constrained Language Mode
Constrained Language Mode is a PowerShell language mode designed to restrict script execution in environments with low trust (like when running as a non-admin, or in AppLocker/Device Guard-constrained systems).
```powershell
$ExecutionContext.SessionState.LanguageMode
```
