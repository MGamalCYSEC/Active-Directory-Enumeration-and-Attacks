# Enumerating Security Controls
## Windows Defender
Checking the Status of Defender with Get-MpComputerStatus
```powershell
Get-MpComputerStatus
```
---

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

---

## PowerShell Constrained Language Mode
Constrained Language Mode is a PowerShell language mode designed to restrict script execution in environments with low trust (like when running as a non-admin, or in AppLocker/Device Guard-constrained systems).
```powershell
$ExecutionContext.SessionState.LanguageMode
```
**Types of PowerShell Language Modes**

|Language Mode|Description|
|---|---|
|**FullLanguage**|Default for local admins. All PowerShell features are available.|
|**ConstrainedLanguage**|Restricts .NET types, COM objects, reflection, and dynamic code. Used in locked-down environments.|
|**RestrictedLanguage**|Very limited. Used in specific environments like the `Add-Type` compiler. Only allows basic expressions and operators.|
|**NoLanguage**|No script execution allowed. Only predefined cmdlets/functions can be run (e.g., in some constrained environments).|

## 🚫 **What is Blocked in Constrained Language Mode**

|Feature|Allowed?|
|---|---|
|**Add-Type**|❌ Blocked|
|**COM Objects (New-Object -ComObject)**|❌ Blocked|
|**.NET Classes**|✅ Only safe ones; many are blocked|
|**Reflection**|❌ Blocked|
|**ScriptBlock.Invoke()**|❌ Blocked|
|**Dynamic Code (e.g., `Invoke-Expression`)**|❌ Blocked|
|**Custom types or methods**|❌ Blocked|
|**Core Cmdlets and Aliases**|✅ Allowed|
|**Simple arithmetic and logic**|✅ Allowed|

---

# LAPS [Local Administrator Password Solution](https://www.microsoft.com/en-us/download/details.aspx?id=46899)

It used to randomize and rotate local administrator passwords on Windows hosts and prevent lateral movement. We can enumerate what domain users can read the LAPS password set for machines with LAPS installed and what machines do not have LAPS installed.
The [LAPSToolkit](https://github.com/leoloobeek/LAPSToolkit) greatly facilitates this with several functions.
```powershell
. .\LAPSToolkit.ps1
Find-LAPSDelegatedGroups
```
We can use the `Get-LAPSComputers` function to search for computers that have LAPS enabled when passwords expire, and even the randomized passwords in cleartext if our user has access.
```powershell
Get-LAPSComputers
```
