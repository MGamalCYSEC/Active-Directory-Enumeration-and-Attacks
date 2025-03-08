Here’s a structured, organized document outlining **Lateral Movement Techniques** and their **Conditions for Success**:

---

# **Lateral Movement Methods**  
*Organized by technique, conditions, and practical use cases*  

---

## **1. Overview**  
**Lateral Movement** refers to techniques attackers use to expand access within a network after initial compromise. These methods often exploit valid accounts, stolen credentials (hashes, Kerberos tickets), or system vulnerabilities.  
- **MITRE Framework**: Mapped under [TA0008 - Lateral Movement](https://attack.mitre.org/tactics/TA0008/).  
- **Key Goal**: Move from a compromised system to other systems/services to escalate privileges or access sensitive data.  

---

## **2. Method-Specific Prerequisites**  

---

### **2.1 [WMI (Windows Management Instrumentation)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks-/blob/main/AD%20Lateral%20Movement/WMI.md)**  
**Use Case**: Remote process execution, system management.  

#### **Conditions for Success**:  
1. **Local Admin Privileges**:  
   - User must be in the target’s **Local Administrators group** (or Domain Admin).  
2. **ADMIN$ Share**:  
   - Must be accessible (enabled by default on Windows).  
3. **File and Printer Sharing**:  
   - Enabled (default on modern Windows).  
4. **Session 0 Execution**:  
   - Processes spawn in non-interactive sessions. Use `-RunAs` for GUI access.  

---

### **2.2 [WinRM (Windows Remote Management)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks-/blob/main/AD%20Lateral%20Movement/WinRM.md)**  
**Use Case**: PowerShell remoting, command execution.  

#### **Conditions for Success**:  
1. **WinRM Enabled**:  
   - Enabled via `Enable-PSRemoting` on the target.  
2. **User Permissions**:  
   - User must be in **Remote Management Users** (basic) or **Administrators** (full).  
3. **Port Access**:  
   - **5985/TCP (HTTP)** or **5986/TCP (HTTPS)** open.  

---

### **2.3 [PsExec](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks-/blob/main/AD%20Lateral%20Movement/PsExec.md)**  
**Use Case**: Remote command execution via SMB.  

#### **Conditions for Success**:  
1. **Local Admin Rights**:  
   - User must be a member of the target’s **Local Administrators group**.  
2. **Network Access**:  
   - **445/TCP (SMB)** open.  
3. **ADMIN$ Share**:  
   - Accessible (default enabled).  

---

### **2.4 [Pass the Hash (PtH)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks-/blob/main/AD%20Lateral%20Movement/Pass%20the%20Hash%20(PtH).md)**  
**Use Case**: Authenticate using NTLM hashes instead of plaintext passwords.  

#### **Conditions for Success**:  
1. **Local Admin Rights**:  
   - Required for non-built-in accounts (post-2014 security updates).  
2. **SMB Access**:  
   - **445/TCP** open and **File/Printer Sharing** enabled.  
3. **ADMIN$ Share**:  
   - Accessible.  

---

### **2.5 [Overpass the Hash (OtH)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks-/blob/main/AD%20Lateral%20Movement/Overpass%20the%20Hash.md)**  
**Use Case**: Convert NTLM hash to Kerberos TGT for stealthy access.  

#### **Conditions for Success**:  
1. **Cached Credentials**:  
   - Target user’s NTLM hash must be cached (e.g., via `sekurlsa::logonpasswords`).  
2. **Kerberos Availability**:  
   - Domain must use Kerberos authentication.  
3. **Local Admin Rights**:  
   - Required to dump LSASS memory for hashes.  

---

### **2.6 [Pass the Ticket (PtT)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks-/blob/main/AD%20Lateral%20Movement/Pass%20the%20Ticket.md)**  
**Use Case**: Steal/reuse Kerberos TGS tickets.  

#### **Conditions for Success**:  
1. **Valid TGS Ticket**:  
   - Service ticket (e.g., `cifs/web04`) must exist in memory.  
2. **LSASS Access**:  
   - Requires admin rights to dump tickets from another user’s session.  
1. **No Admin for Injection (Self-Injection Exception)** :  
   - Tickets can be injected into your own session without privileges.  

---

### **2.7 [DCOM (Distributed Component Object Model)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks-/blob/main/AD%20Lateral%20Movement/DCOM.md)**  
**Use Case**: Remote code execution via COM objects.  

#### **Conditions for Success**:  
1. **Local Admin Rights**:  
   - Required to interact with DCOM Service Control Manager.  
2. **DCOM Enabled**:  
   - Enabled by default on Windows.  
3. **Port Access**:  
   - **135/TCP (RPC)** open.  

---

## **3. Quick Reference Table**  

| **Method**            | **Key Prerequisites**                      | **Tools**              |
| --------------------- | ------------------------------------------ | ---------------------- |
| **WMI**               | Local admin, ADMIN$ share, SMB access      | `wmic`, Impacket       |
| **WinRM**             | WinRM enabled, port 5985/5986              | Evil-WinRM, PowerShell |
| **PsExec**            | Local admin, SMB port 445, ADMIN$ share    | Sysinternals PsExec    |
| **Pass the Hash**     | SMB access, local admin (for non-built-in) | Mimikatz, CrackMapExec |
| **Overpass the Hash** | Cached NTLM hash, Kerberos enabled         | Mimikatz, Rubeus       |
| **Pass the Ticket**   | Valid TGS ticket, LSASS access (optional)  | Mimikatz, Rubeus       |
| **DCOM**              | Local admin, RPC port 135, DCOM enabled    | PowerShell, Impacket   |

---

## **4. Common Themes**  
1. **Local Admin Rights**: Required for most methods (except PtT self-injection).  
2. **Default Shares**: `ADMIN$` and `C$` are critical for SMB-based techniques.  
3. **Network Access**: Ports 135 (RPC), 445 (SMB), 5985/5986 (WinRM) are common targets.  
