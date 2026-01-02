
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

#### #### A specific fetching Using PowerShell to view the Permissions `UserX` has over `TAREGT-USER`
```powershell
$parsedSecurityDescriptor.Access | Where-Object {$_.IdentityReference -like '<UserX>'}
```

## Using `PowerView`
##### Using PowerView to Identify UserX's Rights over `TAREGT-USER`
```powershell
Set-ExecutionPolicy Bypass -Scope CurrentUser -Force
Import-Module .\PowerView.ps1
$userSID = (Get-DomainUser -Identity <UserX>).objectsid
Get-DomainObjectAcl -Identity <TAREGT-USER> -ResolveGUIDs | ?{$_.SecurityIdentifier -eq $userSID}
```

##### Querying UserX's DACL **over the Domain**
```powershell
$userSID = ConvertTo-SID <UserX>
Get-DomainSID | Get-DomainObjectAcl -ResolveGUIDs | ?{$_.SecurityIdentifier -eq $userSID}
```
**Examples**:
![[Pasted image 20251226194907.png]]
##### `Pedro`, has **Self-Membership** over the target group `Backup Operators`
![[Pasted image 20251226233946.png]]
##### `luna`, has **WriteDACL** over the target group `Finance`
![[Pasted image 20251230130204.png]]
##### Pedro's Access Rights over Yolanda **User-Force-Change-Password**
![[Pasted image 20251229164705.png]]
Search `AceType` _00299570-246d-11d0-a768-00aa006e0529_
![[Pasted image 20251229164826.png]]
![[Pasted image 20251229170052.png]]
![[Pasted image 20251230121729.png]]
##### Pedro's **WriteOwner** over the User `GPOAdmin`:
![[Pasted image 20251230154040.png]]


## Executing `GMSAPasswordReader`
```cmd
GMSAPasswordReader.exe --accountname apache-dev
```
![[Pasted image 20251229191757.png]]
##### Enumerate all gMSA accounts first, then loop over them:
```powershell
Get-ADServiceAccount -Filter * | ForEach-Object {
    .\GMSAPasswordReader.exe --accountname $_.Name
}
```
