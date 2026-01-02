
## Using DirectoryServices
#### This PowerShell code **retrieves and parses the DACL of a specific Active Directory user account** (`TAREGT-USER`) to enumerate who has access rights over the object.
###### Steps
- 🎯 Locates the AD object using `sAMAccountName`
- 🔐 Requests **DACL** and **Owner** information
- 📦 Extracts the raw `ntSecurityDescriptor`
- 🧩 Parses the binary descriptor into a readable ACL structure
- 📋 Displays individual **Access Control Entries (ACEs)** for permission analysis
```powershell
$directorySearcher = New-Object System.DirectoryServices.DirectorySearcher('(samaccountname=<TAREGT-USER>)')
$directorySearcher.SecurityMasks = [System.DirectoryServices.SecurityMasks]::Dacl -bor `
                                    [System.DirectoryServices.SecurityMasks]::Owner

$binarySecurityDescriptor = $directorySearcher.FindOne().Properties.ntsecuritydescriptor[0]

$parsedSecurityDescriptor = New-Object System.DirectoryServices.ActiveDirectorySecurity
$parsedSecurityDescriptor.SetSecurityDescriptorBinaryForm($binarySecurityDescriptor)

$parsedSecurityDescriptor.Access
```

##### Sample output:
```css
ActiveDirectoryRights : ReadProperty, WriteProperty
InheritanceType       : All
ObjectType            : 5b47d60f-6090-40b2-9f37-2a4de88f3063
InheritedObjectType   : 00000000-0000-0000-0000-000000000000
ObjectFlags           : ObjectAceTypePresent
AccessControlType     : Allow
IdentityReference     : DOMAIN\Key Admins
IsInherited           : True
InheritanceFlags      : ContainerInherit
PropagationFlags      : None
```
**This means:**
`DOMAIN\Key Admins` has **ReadProperty** and **WriteProperty** permissions over `TAREGT-USER`

#### A specific fetching Using PowerShell to view the Permissions `UserX` has over `TAREGT-USER`

```powershell
$parsedSecurityDescriptor.Access | Where-Object {$_.IdentityReference -like '<UserX>'}
```

## Using `PowerView`

##### ✅ Using PowerView to Identify UserX's Rights over `TAREGT-USER`

```powershell
Set-ExecutionPolicy Bypass -Scope CurrentUser -Force
Import-Module .\PowerView.ps1
$userSID = (Get-DomainUser -Identity <UserX>).objectsid
Get-DomainObjectAcl -Identity <TAREGT-USER> -ResolveGUIDs | ?{$_.SecurityIdentifier -eq $userSID}
```

##### ✅ Querying UserX's DACL **over the Domain**

```powershell
$userSID = ConvertTo-SID <UserX>
Get-DomainSID | Get-DomainObjectAcl -ResolveGUIDs | ?{$_.SecurityIdentifier -eq $userSID}
```
**Examples**:

<img width="1698" height="685" alt="Pasted image 20251226194907" src="https://github.com/user-attachments/assets/a925e7de-2e18-4eb4-a083-f3e149ba7c46" />

##### ✅ `Pedro`, has **Self-Membership** over the target group `Backup Operators`

<img width="1830" height="571" alt="Pasted image 20251226233946" src="https://github.com/user-attachments/assets/3792009c-1b82-4aa0-9605-8cb258d8b102" />

##### ✅ `luna`, has **WriteDACL** over the target group `Finance`

<img width="1893" height="423" alt="Pasted image 20251230130204" src="https://github.com/user-attachments/assets/0e060a23-2dc6-424c-a3ce-d4b6d4daa7c0" />

##### ✅ Pedro's Access Rights over Yolanda **User-Force-Change-Password**

<img width="1508" height="599" alt="Pasted image 20251229164705" src="https://github.com/user-attachments/assets/20a70c9f-2773-464a-ae15-d84a44736462" />

Search `AceType` _00299570-246d-11d0-a768-00aa006e0529_

<img width="1093" height="125" alt="Pasted image 20251229164826" src="https://github.com/user-attachments/assets/6e1aa135-904b-4c38-9bcb-253b843a066a" />

<img width="1227" height="507" alt="Pasted image 20251229170052" src="https://github.com/user-attachments/assets/4e117d0d-d852-406d-bd2b-0a5feb37c387" />

<img width="1617" height="542" alt="Pasted image 20251230121729" src="https://github.com/user-attachments/assets/0f3e1018-a230-4f98-934e-68cad2cfb558" />

##### ✅ Pedro's **WriteOwner** over the User `GPOAdmin`:

<img width="1762" height="541" alt="Pasted image 20251230154040" src="https://github.com/user-attachments/assets/53776218-ce0f-4e9f-9dee-87ed1650497d" />


## Executing `GMSAPasswordReader`
```cmd
GMSAPasswordReader.exe --accountname apache-dev
```

<img width="1609" height="486" alt="Pasted image 20251229191757" src="https://github.com/user-attachments/assets/68db4b6c-a193-4c30-a47a-edce7a040e2a" />

##### ✅ Enumerate all gMSA accounts first, then loop over them:

```powershell
Get-ADServiceAccount -Filter * | ForEach-Object {
    .\GMSAPasswordReader.exe --accountname $_.Name
}
```
