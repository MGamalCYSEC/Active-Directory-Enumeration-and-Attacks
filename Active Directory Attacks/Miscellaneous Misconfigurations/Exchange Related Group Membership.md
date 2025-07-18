# Exchange Related Group Membership
- The Exchange group Organization Management is another extremely powerful group (effectively the "Domain Admins" of Exchange) and can access the mailboxes of all domain users. It is not uncommon for sysadmins to be members of this group. This group also has full control of the OU called Microsoft Exchange Security Groups, which contains the group Exchange Windows Permissions.
- If we can compromise an Exchange server, this will often lead to Domain Admin privileges. Additionally, dumping credentials in memory from an Exchange server will produce 10s if not 100s of cleartext credentials or NTLM hashes.

# PrivExchange
The PrivExchange attack results from a flaw in the Exchange Server PushSubscription feature, which allows any domain user with a mailbox to force the Exchange server to authenticate to any host provided by the client over HTTP.

The PrivExchange attack exploits a flaw in the Exchange PushSubscription feature, allowing any domain user with a mailbox to trick Exchange into authenticating to an attacker-controlled host. Since Exchange runs as SYSTEM and often has excessive privileges (like WriteDacl on the domain), this authentication can be relayed to LDAP to gain DCSync rights and dump the NTDS database—resulting in full domain compromise. Even if LDAP relay fails, the attack can still be used for lateral movement within the domain.

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

# MS14-068
Vulnerability in Kerberos Could allow an attacker to elevate unprivileged domain user account privileges to those of the domain administrator account. A Kerberos ticket contains information about a user, including the account name, ID, and group membership in the Privilege Attribute Certificate (PAC). The PAC is signed by the KDC using secret keys to validate that the PAC has not been tampered with after creation.
The vulnerability allowed a forged PAC to be accepted by the KDC as legitimate. This can be leveraged to create a fake PAC, presenting a user as a member of the Domain Administrators or other privileged group.
The only defense against this attack is patching.
Knock and Pass: Kerberos Exploitation follow the steps [HERE](https://wizard32.net/blog/knock-and-pass-kerberos-exploitation.html)
python script in order to impersonate the Kerberos ticket [HERE](https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS14-068/pykek)
Sample HTB Machine [Mantis](https://app.hackthebox.com/machines/98)

# Sniffing LDAP Credentials
Many applications and printers store LDAP credentials in their web admin console to connect to the domain. Sometimes, these credentials can be viewed in cleartext. Other times, the application has a test connection function that we can use to gather credentials by changing the LDAP IP address to that of our attack host and setting up a netcat listener on LDAP port 389. Accounts used for LDAP connections are often privileged, but if not, this could serve as an initial foothold in the domain. Other times, a full LDAP server is required to pull off this attack Check [ME](https://grimhacker.com/2018/03/09/just-a-printer/)

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

# Password in Description Field
Sensitive information such as account passwords are sometimes found in the user account Description or Notes fields and can be quickly enumerated using PowerView.
```powershell
Import-Module .\Import-Module
Get-DomainUser * | Select-Object samaccountname,description |Where-Object {$_.Description -ne $null}
```

We can use the this [shell script](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Automation/Users_Description_Comment_RPC.sh) to get all description data for users using valid RPC credits (Change IP, User, Password) in the script.
NOTE: It will take time in compare to PowerView but that is depend on your access type.

# PASSWD_NOTREQD Field
- If passwd_notreqd field set, the user is not subject to the current password policy length, meaning they could have a shorter password or no password at all (if empty passwords are allowed in the domain). A password may be set as blank intentionally or accidentally hitting enter before entering a password when changing it via the command line.
- Just because this flag is set on an account, it doesn't mean that no password is set, just that one may not be required.
## Checking for PASSWD_NOTREQD Setting using PowerView
```powershell
Import-Module .\Import-Module
Get-DomainUser -UACFilter PASSWD_NOTREQD | Select-Object samaccountname,useraccountcontrol
```
## Checking for PASSWD_NOTREQD Setting using rpc 
we can utilize This following [Bash Script](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Automation/Check_PASSWD_NOTREQD.sh): Check for PASSWD_NOTREQD Flag (0x0020) using valid RPC credits

# Credentials in SMB Shares and SYSVOL Scripts

