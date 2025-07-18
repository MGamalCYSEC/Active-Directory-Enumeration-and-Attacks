# Exchange Related Group Membership
- The Exchange group Organization Management is another extremely powerful group (effectively the "Domain Admins" of Exchange) and can access the mailboxes of all domain users. It is not uncommon for sysadmins to be members of this group. This group also has full control of the OU called Microsoft Exchange Security Groups, which contains the group Exchange Windows Permissions.
- If we can compromise an Exchange server, this will often lead to Domain Admin privileges. Additionally, dumping credentials in memory from an Exchange server will produce 10s if not 100s of cleartext credentials or NTLM hashes.

---

# PrivExchange
The PrivExchange attack results from a flaw in the Exchange Server PushSubscription feature, which allows any domain user with a mailbox to force the Exchange server to authenticate to any host provided by the client over HTTP.

The PrivExchange attack exploits a flaw in the Exchange PushSubscription feature, allowing any domain user with a mailbox to trick Exchange into authenticating to an attacker-controlled host. Since Exchange runs as SYSTEM and often has excessive privileges (like WriteDacl on the domain), this authentication can be relayed to LDAP to gain DCSync rights and dump the NTDS database—resulting in full domain compromise. Even if LDAP relay fails, the attack can still be used for lateral movement within the domain.

---

# Printer Bug
- The Printer Bug is a flaw in the MS-RPRN protocol (Print System Remote Protocol). This protocol defines the communication of print job processing and print system management between a client and a print server. 
- To leverage this flaw, any domain user can connect to the spool's named pipe with the RpcOpenPrinter method and use the RpcRemoteFindFirstPrinterChangeNotificationEx method, and force the server to authenticate to any host provided by the client over SMB.
- The spooler service runs as SYSTEM and is installed by default in Windows servers running Desktop Experience. 
attack can be leveraged to relay to LDAP and grant your attacker account DCSync privileges to retrieve all password hashes from AD.
- The attack can also be used to relay LDAP authentication and grant Resource-Based Constrained Delegation (RBCD) privileges for the victim to a computer account under our control, thus giving the attacker privileges to authenticate as any user on the victim's computer.
- This attack can be leveraged to compromise a Domain Controller in a partner domain/forest, provided you have administrative access to a Domain Controller in the first forest/domain already, and the trust allows TGT delegation, which is not by default anymore.

## Enumerating for MS-PRN Printer Bug
We can use tools such as the Get-SpoolStatus SecurityAssessment.ps1 
- Download SecurityAssessment module
```shell
wget https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Tools/SecurityAssessment.ps1
```
- On target Powershell
```powershell
Import-Module .\SecurityAssessment.ps1
Get-SpoolStatus -ComputerName DC01.domain.LOCAL
```
<img width="1128" height="94" alt="image" src="https://github.com/user-attachments/assets/46297323-944d-4d4e-9a53-55b34cf6a803" />

---

# MS14-068
Vulnerability in Kerberos Could allow an attacker to elevate unprivileged domain user account privileges to those of the domain administrator account. A Kerberos ticket contains information about a user, including the account name, ID, and group membership in the Privilege Attribute Certificate (PAC). The PAC is signed by the KDC using secret keys to validate that the PAC has not been tampered with after creation.
The vulnerability allowed a forged PAC to be accepted by the KDC as legitimate. This can be leveraged to create a fake PAC, presenting a user as a member of the Domain Administrators or other privileged group.
The only defense against this attack is patching.
Knock and Pass: Kerberos Exploitation follow the steps [HERE](https://wizard32.net/blog/knock-and-pass-kerberos-exploitation.html)
python script in order to impersonate the Kerberos ticket [HERE](https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS14-068/pykek)
Sample HTB Machine [Mantis](https://app.hackthebox.com/machines/98)

---

# Sniffing LDAP Credentials
Many applications and printers store LDAP credentials in their web admin console to connect to the domain. Sometimes, these credentials can be viewed in cleartext. Other times, the application has a test connection function that we can use to gather credentials by changing the LDAP IP address to that of our attack host and setting up a netcat listener on LDAP port 389. Accounts used for LDAP connections are often privileged, but if not, this could serve as an initial foothold in the domain. Other times, a full LDAP server is required to pull off this attack Check [ME](https://grimhacker.com/2018/03/09/just-a-printer/)

---

# Enumerating DNS Records
- Enumerate all DNS records in a domain using a valid domain user account. 
- If all servers and workstations have a non-descriptive name, it makes it difficult for us to know what exactly to attack. If we can access DNS entries in AD, we can potentially discover interesting DNS records that point to this same server
- The tool works because, by default, all users can list the child objects of a DNS zone in an AD environment.
- By using the [adidnsdump](https://github.com/dirkjanm/adidnsdump) tool, we can resolve all records in the zone and potentially find something useful for our engagement. Check [Post](https://dirkjanm.io/getting-in-the-zone-dumping-active-directory-dns-with-adidnsdump/)
```shell
git clone https://github.com/dirkjanm/adidnsdump
cd adidnsdump
pip3 install . --break-system-packages
adidnsdump -u domain\\user ldap://<DC-IP> 
```
If we run again with the -r flag the tool will attempt to resolve unknown records by performing an A query.

---

# Password in Description Field
Sensitive information such as account passwords are sometimes found in the user account Description or Notes fields and can be quickly enumerated using PowerView.
```powershell
Import-Module .\Import-Module
Get-DomainUser * | Select-Object samaccountname,description |Where-Object {$_.Description -ne $null}
```

We can use the this [shell script](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Automation/Users_Description_Comment_RPC.sh) to get all description data for users using valid RPC credits (Change IP, User, Password) in the script.
NOTE: It will take time in compare to PowerView but that is depend on your access type.

---

# PASSWD_NOTREQD Field
- If passwd_notreqd field set, the user is not subject to the current password policy length, meaning they could have a shorter password or no password at all (if empty passwords are allowed in the domain). A password may be set as blank intentionally or accidentally hitting enter before entering a password when changing it via the command line.
- Just because this flag is set on an account, it doesn't mean that no password is set, just that one may not be required.
## Checking for PASSWD_NOTREQD Setting using PowerView
```powershell
Import-Module .\Import-Module
Get-DomainUser -UACFilter PASSWD_NOTREQD | Select-Object samaccountname,useraccountcontrol
```

---

# Credentials in SMB Shares and SYSVOL Scripts
The SYSVOL share can be a treasure trove of data, especially in large organizations. We may find many different batch, VBScript, and PowerShell scripts within the scripts directory, which is readable by all authenticated users in the domain. It is worth digging around this directory to hunt for passwords stored in scripts. Sometimes we will find very old scripts containing since disabled accounts or old passwords, but from time to time, we will strike gold, so we should always dig through this directory. 
## Discovering an Interesting Script
```powershell
\\<Computer-Name>\SYSVOL\Domain.LOCAL\scripts
```

---

# Group Policy Preferences (GPP) Passwords
When a new Group Policy Preference (GPP) is created, an associated `.xml` configuration file is generated and stored in the `SYSVOL` share on the domain controller. These files are also cached locally on endpoints where the Group Policy applies.

Common GPP XML files include:

* `drives.xml`: Used for mapping network drives
* `groups.xml`: Used for creating or modifying local user accounts
* `printers.xml`: Defines printer configurations
* `services.xml`: Manages service creation and updates
* `scheduledtasks.xml`: Used to create or update scheduled tasks
* Other XMLs: May be used to configure local administrator passwords or other system settings

These XML files can store various configuration parameters, including passwords. The `cpassword` attribute holds passwords encrypted using AES-256. However, Microsoft publicly [disclosed the encryption key on MSDN](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be?redirectedfrom=MSDN), making it possible to decrypt these values. Since `SYSVOL` is world-readable to all authenticated domain users by default, any domain user can access and potentially decrypt these stored passwords.

This security issue was addressed in **Microsoft Security Bulletin MS14-025 (2014)**, which prevented administrators from setting passwords via GPP going forward. However:

* The patch **does not remove** existing `Groups.xml` files containing passwords from `SYSVOL`.
* If a GPP policy is **deleted** rather than **unlinked** from the Organizational Unit (OU), the cached copy **remains on the local machine**, potentially leaving credentials exposed.
If you retrieve the cpassword value more manually, the gpp-decrypt utility can be used to decrypt the password as follows:
```shell
gpp-decrypt VPe/o9YRyz2cksnYRbNeQj35w9KxQ5ttbvtRaAVqxaE
```
<img width="1129" height="64" alt="image" src="https://github.com/user-attachments/assets/008f63ba-c823-49bc-814b-6e8b9d819a2d" />

Locating & Retrieving GPP Passwords with NetExec
```shell
exec smb -L | grep gpp
```
<img width="1808" height="95" alt="image" src="https://github.com/user-attachments/assets/6ce99646-5dfc-4077-876f-c0264cc54a23" />
Using NetExec's gpp_autologin Module
```shell
netexec smb <Target-IP> -u <User> -p <Password> -M gpp_autologin
```

---

# Understanding and Abusing Group Policy Objects (GPOs)
Group Policy is a powerful feature in Active Directory that allows administrators to enforce a wide range of settings on both users and computers across the domain. When used properly, GPOs can significantly strengthen security by applying consistent configurations to systems and applications.

However, the same capabilities that make GPOs valuable to administrators can also be exploited by attackers. If an attacker gains control over a Group Policy Object—often due to misconfigured Access Control Lists (ACLs)—they can use it for:

* **Lateral movement** between systems
* **Privilege escalation** by assigning elevated rights
* **Domain persistence**, making their access harder to detect or remove
* Even **full domain compromise** in some cases

That’s why understanding how to **identify and assess GPO configurations** is critical during security assessments. Misconfigured GPOs can be abused to:

* Grant high-level privileges (e.g., `SeDebugPrivilege`, `SeTakeOwnershipPrivilege`, `SeImpersonatePrivilege`)
* Add local administrator accounts across machines
* Schedule tasks that execute malicious commands immediately

#### Tools for GPO Enumeration and Security Auditing

Several tools can help you enumerate and assess GPO security:

* **PowerView** – Use the `Get-DomainGPO` function to list all GPOs in the domain
* **BloodHound** – Excellent for visualizing GPO relationships and privilege paths
* **Group3r**, **ADRecon**, **PingCastle** – Useful for automated GPO auditing and reporting

By leveraging these tools, you can identify weak GPO configurations that may open the door to privilege abuse or persistence—key opportunities during red teaming or internal penetration tests, especially in tightly locked-down environments.

## Enumerating GPO Names with PowerView
```powershell
Get-DomainGPO |select displayname
```

## Using Built-In Cmdlet
```powershell
Get-GPO -All | Select DisplayName
```
<img width="1232" height="474" alt="image" src="https://github.com/user-attachments/assets/44d4a862-1e55-4e13-9b4c-3f44dde4c93c" />

This can be helpful for us to begin to see what types of security measures are in place (such as denying cmd.exe access and a separate password policy for service accounts). We can see that autologon is in use which may mean there is a readable password in a GPO, and see that Active Directory Certificate Services (AD CS) is present in the domain.

---

# Enumerating Domain User GPO Rights
Using PowerView
```powershell
$sid=Convert-NameToSid "Domain Users"
Get-DomainGPO | Get-ObjectAcl | ?{$_.SecurityIdentifier -eq $sid}
```
Here’s a clearer and more professional rephrasing of your paragraph:

---

In this case, we observe that the **Domain Users** group has excessive permissions over a Group Policy Object (GPO), including rights like **WriteProperty** and **WriteDacl**. These permissions can be exploited to gain **full control over the GPO**, enabling us to modify its settings and launch a variety of attacks. Any changes made would automatically propagate to all users and computers within the **Organizational Units (OUs)** where the GPO is linked—potentially impacting a large portion of the domain.

To identify the GPO by name, we can use its **GUID** along with the `Get-GPO` command (e.g., `Get-GPO -Guid <GPO-GUID>`), which will return the display name and help us better understand its scope and impact.

## Converting GPO GUID to Name
```powershell
Get-GPO -Guid 7CA9C789-14CE-46E3-A722-83F4097AF532
```



