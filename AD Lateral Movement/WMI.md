
### **WMI (Windows Management Instrumentation)**  
**Use Cases**: Remote code execution, lateral movement, data collection.  
**Protocol**: DCOM (TCP ports 135, 49152-65535) or WinRM (HTTP/5985, HTTPS/5986).  
we need the credentials of a member of the _Administrators_ local group, which can also be a domain user.
From PowerShell with `valid member of the Local Administrator group` for the target machines.

 ``` powershell
 wmic /node:192.168.50.73 /user:jen /password:Nexus123! process call create "calc"
```
**Key Commands**:  
- **Legacy WMIC (Deprecated but still useful)**:  
  ```bash
  wmic /node:<IP> /user:<DOMAIN\USER> /password:<PASSWORD> process call create "cmd.exe /c calc.exe"
  ```  
- **/node:** Specifies the target machine’s IP address or hostname.
- **/user:** The username that has the required privileges on the target machine.
- **/password:** The corresponding password for authentication.
- **process call create:** Instructs WMIC to create (execute) a new process on the target.
- **"<COMMAND>":** The command or application to be executed remotely (e.g., `"calc"` for the calculator).
Example:

``` powershell
 wmic /node:192.168.50.73 /user:jen /password:Nexus123! process call create "calc"
```

- A `ReturnValue` of "0", meaning that the process has been created successfully.
- **PowerShell (Modern Approach)**:  
Steps:
1. Create a `PSCredential` Object.
2. Prepare a` CIM` Session: Define session options to use `DCOM` -> Create a new `CIM` session to the target < IP >.
3. Use `Invoke-CimMethod` to run the command on the target machine.

  ```powershell
  # Create PSCredential Object
  $cred = New-Object System.Management.Automation.PSCredential ('<USER>', (ConvertTo-SecureString '<PASSWORD>' -AsPlainText -Force))

  # Create CIM Session (DCOM)
  $opt = New-CimSessionOption -Protocol DCOM
  $session = New-CimSession -ComputerName <IP> -Credential $cred -SessionOption $opt

  # Execute Command
  $Command = 'calc.exe'
  Invoke-CimMethod -CimSession $session -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=$Command}
  ```  

**Key Considerations**:  
- Requires **local admin** privileges on the target.  
- Processes spawn in **Session 0** (non-interactive). Use `-RunAs` or migrate to user sessions for GUI access.  
- UAC bypassed for **domain admins** on domain-joined machines.  
#### We can replace `$Command` with Encoded shell from [PowerShell_RCE](https://github.com/MGamalCYSEC/ReverseShellCrafter/tree/main/PowerShell)
Encoded shell


