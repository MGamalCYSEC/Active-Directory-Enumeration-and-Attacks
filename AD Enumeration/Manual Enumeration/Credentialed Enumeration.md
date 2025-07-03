# Credentialed Enumeration - from Linux
## Using CrackMapExec (now NetExec)
### Domain User Enumeration
```powershell
sudo crackmapexec smb <Target-IP> -u <username> -p <password> --users
sudo netexec smb <Target-IP> -u <username> -p <password> --users

```
### Domain Group Enumeration
```shell
sudo crackmapexec smb <Target-IP> -u <username> -p <password> --groups
sudo netexec smb <Target-IP> -u <username> -p <password> --groups
```
### Logged On Users
```shell
sudo crackmapexec smb <Target-IP> -u <username> -p <password> --loggedon-users
sudo netexec smb <Target-IP> -u <username> -p <password> --loggedon-users
```
### Share Searching
```shell
sudo crackmapexec smb <Target-IP> -u <username> -p <password> --shares
sudo netexec smb <Target-IP> -u <username> -p <password> --shares
```
#### Spider_plus
The module spider_plus will dig through each readable share on the host and list all readable files.
```shell
sudo crackmapexec smb <Target-IP> -u <username> -p <password> -M spider_plus --share 'Department Shares'
sudo netexec smb <Target-IP> -u <username> -p <password> -M spider_plus --share 'Department Shares'
```
---

## Using SMBMap
SMBMap is great for enumerating SMB shares from a Linux attack host.
### SMBMap To Check Access
```shell
smbmap -u <username> -p <password> -d Domain.LOCAL -H <Target-IP>
```
### Recursive List Of All Directories
```shell
smbmap -u <username> -p <password> -d Domain.LOCAL -H <Target-IP> -R 'Department Shares' --dir-only
```
---

## Using rpcclient
### unauthenticated enumeration
```shell
rpcclient -U "" -N <Target-IP>
```
### Authenticated enumeration
```shell
rpcclient -U 'DOMAIN\Administrator%password' <Target-IP>
```
In rpc **rid**: beside each user. A [Relative Identifier](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/security-identifiers) (RID) is a unique identifier (represented in hexadecimal format) utilized by Windows to track and identify objects.
### User Enumeration
```shell
> enumdomusers
```
![image](https://github.com/user-attachments/assets/82b57b31-845f-4620-8b38-65395a61bd14)
**Enumeration By RID**
`queryuser RID`
```shell
queryuser 0x1f4
```
Extract Users Descriptions/Comments for extra informations with rpc
[Script.sh](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Automation/Users_Description_Comment_RPC.sh)

### Group Enumeration
```shell
> enumdomgroups
```
![image](https://github.com/user-attachments/assets/e9d41d37-26da-4533-a438-05e8591858ed)
**Get group members**
`querygroupmem RID`
```shell
querygroupmem 0xff0
```

---

## Impacket Toolkit
### psexec.py
```shell
psexec.py Domain.local/User:'Password'@<Target-IP>
impacket-psexec Domain.local/User:'Password'@<Target-IP>
```
### wmiexec.py
utilizes a semi-interactive shell where commands are executed through [Windows Management Instrumentation](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmi-start-page). It does not drop any files or executables on the target host and generates fewer logs than other modules.
```shell
wmiexec.py Domain.local/User:'Password'@<Target-IP>
impacket-wmiexec Domain.local/User:'Password'@<Target-IP>
```
---

## Using [Windapsearch](https://github.com/ropnop/windapsearch) that utilizing **LDAP** queries
Python script we can use to enumerate users, groups, and computers from a Windows domain by utilizing **LDAP** queries.
### Windapsearch - Domain Admins
``` shell
python3 windapsearch.py --dc-ip <Target-IP> -u User@Domain.local -p <Password> --da
```
### Windapsearch - Privileged Users
``` shell
python3 windapsearch.py --dc-ip <Target-IP> -u User@Domain.local -p <Password> -PU
```

