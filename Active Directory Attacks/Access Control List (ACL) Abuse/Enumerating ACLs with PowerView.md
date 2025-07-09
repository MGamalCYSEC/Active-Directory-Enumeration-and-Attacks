# Enumerating ACLs with PowerView
## Performing targeted enumeration starting with a user that we have control over.
Example: We will foucs on owned user 
1. Get SID from Username

```powershell
$username = "DOMAIN\Username"
(New-Object System.Security.Principal.NTAccount($username)).Translate([System.Security.Principal.SecurityIdentifier]).Value
```
**Using PowerView**
```powershell
Convert-NameToSID -Name "username"
```
2. Using the `Get-DomainObjectACL` function to perform our targeted search
```powershell
$sid = Convert-NameToSid <user>
Get-DomainObjectACL -Identity * | ? {$_.SecurityIdentifier -eq $sid}
```
![image](https://github.com/user-attachments/assets/31c04d84-2c2e-4225-9f59-6bd452867427)

This picture shows that user wley with SID ****-1181 has an Extended rights with ACE `00299570-246d-11d0-a768-00aa006e0529` on user ObjectDN Dana Amundsen with sid `S-1-5-21-3842939050-3880317879-2865463114-1176`

- To get the ACE type google it ACE `00299570-246d-11d0-a768-00aa006e0529` we will found it a **User-Force-Change-Password extended right**
- To get username from SID use PowerView
```powershell
Convert-SIDToName -SID "S-1-5-21-XXXXXXX-XXXXXXX-XXXXXXX-XXXX"
```

3. **PowerView** has the `ResolveGUIDs` flag, which does this very thing for us but will take much time.
```powershell
Get-DomainObjectACL -ResolveGUIDs -Identity * | ? {$_.SecurityIdentifier -eq $sid} 
```
### Performing a Reverse Search & Mapping to a GUID Value
**NOTE**: Shell must run with admin priv.
Example: Preform search on GUID value `00299570-246d-11d0-a768-00aa006e0529`  which is a **User-Force-Change-Password extended right**
```powershell
$guid= "00299570-246d-11d0-a768-00aa006e0529"
Get-ADObject -SearchBase "CN=Extended-Rights,$((Get-ADRootDSE).ConfigurationNamingContext)" -Filter {ObjectClass -like 'ControlAccessRight'} -Properties * |Select Name,DisplayName,DistinguishedName,rightsGuid| ?{$_.rightsGuid -eq $guid} | fl
```

## Check what controls we have over UsersList with our user 
1. Creating a List of Domain Users with PowerView
```powershell
Get-ADUser -Filter * | Select-Object -ExpandProperty SamAccountName > ad_users.txt
```
2. Check what controls we have over UsersList with our <user>
```powershell
foreach($line in [System.IO.File]::ReadLines("C:\temp\ad_users.txt")) {get-acl  "AD:\$(Get-ADUser $line)" | Select-Object Path -ExpandProperty Access | Where-Object {$_.IdentityReference -match 'INLANEFREIGHT\\<User>'}}
```

### Get member of group that we found user has controls over it
```powershell
Get-DomainGroup -Identity "Group Name" | select memberof
```

