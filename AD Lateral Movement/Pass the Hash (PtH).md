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

#### **Example: Impacket’s `wmiexec`**  
```bash
# Syntax:
impacket-wmiexec -hashes <LM_HASH:NT_HASH> <USER>@<TARGET_IP>

# Example (local admin):
impacket-wmiexec -hashes :2892D26CDF84D7A70E2EB3B9F05C425E Administrator@192.168.50.73
```  
- **Output**: Semi-interactive shell with SYSTEM/local admin privileges.  
- **Use Case**: Execute commands, dump credentials, or pivot to other hosts.  

---

### **Key Notes**  
1. **Limitations**:  
   - Doesn’t work for Kerberos-authenticated services.  
   - Blocked for non-built-in local admin accounts (post-2014 patches).  

2. **Stealth**:  
   - Triggers **Event ID 4624** (Logon Type 3) and **Event ID 4688** (Process Creation).  
   - Use proxying/pivoting to avoid direct exposure.  

---

### **Detection & Mitigation**  
**Detection**:  
- Monitor for **NTLM authentication** (Event ID 4776) from unexpected users.  
- Alert on SMB connections to ADMIN$ share from non-admin workstations.  

**Mitigation**:  
- Disable NTLM (enforce **Kerberos**).  
- Use **Local Administrator Password Solution (LAPS)** for unique local admin passwords.  
- Restrict SMB (port 445) and disable File/Printer Sharing if unused.  
- Enable **Protected Users** group to block NTLM caching.  
