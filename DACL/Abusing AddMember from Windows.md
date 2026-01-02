**PowerShell** or **CMD**
#### Query the Backup Operators Group Membership
```cmd
net localgroup "<TARGET-GROUP>"
```
#### Adding a User to a Group using PowerView
```powershell
Add-DomainGroupMember -Identity "<TARGET-GROUP>" -Members <USSER-TO-BE-ADDED> -Verbose
```
<img width="1655" height="60" alt="Pasted image 20251227222345" src="https://github.com/user-attachments/assets/078eb509-4214-4b4c-a45a-800646b5717e" />

