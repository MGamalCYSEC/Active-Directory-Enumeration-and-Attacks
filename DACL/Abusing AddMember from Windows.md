**PowerShell** or **CMD**
#### Query the Backup Operators Group Membership
```cmd
net localgroup "<TARGET-GROUP>"
```
#### Adding a User to a Group using PowerView
```powershell
Add-DomainGroupMember -Identity "<TARGET-GROUP>" -Members <USSER-TO-BE-ADDED> -Verbose
```
![[Pasted image 20251227222345.png]]
