# Using PowerView
`PowerView.ps1` is a powerful PowerShell script included in the PowerSploit framework, designed for Active Directory enumeration and exploitation. Below is an overview of commonly used commands and examples for `PowerView.ps1`.
**Importing PowerView**
```powershell
powershell -ep bypass
Import-Module .\PowerView.ps1
```
## Enumerating Domain Information
**Get-NetDomain**
```powershell
Get-NetDomain
```
**Get-NetForest**
```powershell
Get-NetForest
```
**Get-NetDomainController**
```powershell
Get-NetDomainController
```
**Get-NetUser**
List **all users** in the domain:
```powershell
Get-NetUser
```
- **To filter by a specific user:**
```powershell
Get-NetUser | Where-Object { $_.SamAccountName -eq "gamal" }
```
- **Querying users using select statement**
``` powershell
Get-NetUser | select cn
```
- **Querying users displaying pwdlastset and lastlogon**
``` powershell
Get-NetUser | select cn,pwdlastset,lastlogon
```
- Example 
``` powershell
Get-DomainUser -Identity gamal -Domain domain.local | Select-Object -Property name,samaccountname,description,memberof,whencreated,pwdlastset,lastlogontimestamp,accountexpires,admincount,userprincipalname,serviceprincipalname,useraccountcontrol
```
**Get-NetGroup**
**Retrieve all groups in the domain**
```powershell
Get-NetGroup
```
- **Find users in a specific group**
```powershell
Get-NetGroup | Where-Object { $_.Name -eq "Development Department" }
```
- **Enumerate a specific group member**
``` powershell
Get-NetGroup "Management Department" | select member
```
- **Recursive Group Membership**
``` powershell
Get-DomainGroupMember -Identity "Domain Admins" -Recurse
```
- **enumerate domain trust mappings**
``` powershell
Get-DomainTrustMapping
```
