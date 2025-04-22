# AD Password Attacks
##  Enumerating the Password Policy
- PowerShell
``` powershell
net account
```
Note: **Lockout threshold** which indicates a limit of _numbers_ login attempts before lockout.
- [PowerView](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Tools/PowerView.ps1)
``` powershell
import-module .\PowerView.ps1
Get-DomainPolicy
```
## Making a Target User List
