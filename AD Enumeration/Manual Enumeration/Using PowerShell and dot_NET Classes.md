According to Microsoft's documentation, we need a specific LDAP ADsPath in order to communicate with the AD service. The LDAP path's prototype looks like this:
``` 
LDAP://HostName[:PortNumber][/DistinguishedName]
```

#### LDAP Path Parameters Summary

A full LDAP path requires three key parameters:

1. **HostName**:
    - Can be a computer name, IP address, or domain name.
    - Example: For the domain `corp.com`, the HostName could be `corp.com`. However, domains often have multiple Domain Controllers (DCs), and resolving the domain name might point to any DC in the domain.
    - Optimal enumeration requires identifying the [_Primary Domain Controller_](https://learn.microsoft.com/en-GB/troubleshoot/windows-server/identity/fsmo-roles) (PDC), which holds the most updated information.
    - To locate the PDC, find the Domain Controller with the `PdcRoleOwner` property, typically done using PowerShell and specific .NET classes.
2. **PortNumber**:
    
    - Optional for LDAP connections, as the port is chosen automatically based on whether SSL is used.
    - Default ports:
        - Non-SSL: 389
        - SSL: 636
    - For domains with non-default ports, manually specify the PortNumber in scripts.
3. **DistinguishedName (DN)**:
    
    - Uniquely identifies an object in Active Directory (AD).
    - Follows a specific naming standard essential for LDAP functionality.
    - Example: For a user `stephanie` in the `corp.com` domain, the DN might look like:  
        `CN=stephanie,OU=Users,DC=corp,DC=com`.
    - This structure represents:
        - `CN` (Common Name): Specific object (e.g., `stephanie`).
        - `OU` (Organizational Unit): Container within AD (e.g., `Users`).
        - `DC` (Domain Component): Hierarchy of the domain (e.g., `corp.com`).
##### Key Elements in the Distinguished Name (DN)

1. **Common Name (CN)**:
    
    - Identifies an object in the domain.
    - Example: In `CN=Stephanie`, "Stephanie" is the CN representing the user object.
2. **Domain Component (DC)**:
    
    - Refers to components of the domain in the DN, not the Domain Controller in this context.
    - Represents the top of the LDAP tree.
    - Example: `DC=corp,DC=com` signifies the domain `corp.com`.
3. **Reading a DN**:
    
    - Start from the **rightmost** components and move **leftward**.
    - Example: `CN=Stephanie,OU=Users,DC=corp,DC=com`:
        - `DC=corp,DC=com`: The domain (top of the LDAP hierarchy).
        - `OU=Users`: The container where the user is stored.
        - `CN=Stephanie`: The user object.

#### DN Application in LDAP Path

- Focus on `DC=corp,DC=com` for domain-wide enumeration.
- Avoid restricting the search scope by including specific containers like `CN=Users` unless necessary.

#### Preparing to Obtain the PDC

- Use [.NET classes](https://learn.microsoft.com/en-us/dotnet/api/) classes for Active Directory under the `System.DirectoryServices.ActiveDirectory` namespace.
- Key Class: [_Domain Class_](https://learn.microsoft.com/en-us/dotnet/api/system.directoryservices.activedirectory.domain?view=windowsdesktop-7.0)
    - Contains a property `PdcRoleOwner`, which identifies the PDC.
    - Relevant Method: `GetCurrentDomain()`
        - Returns the domain object for the current user (e.g., Stephanie in the example).

#### Next Steps for Scripting

1. Use the `GetCurrentDomain()` method to fetch the domain object.
2. Access the `PdcRoleOwner` property to determine the hostname of the PDC.
3. Incorporate the obtained hostname into the LDAP path for accurate enumeration.

To invoke the _Domain Class_ and the _GetCurrentDomain_ method, we'll run the following command in PowerShell:
``` powershell
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
```
#### Using ADSI to obtain the DN for the domain
``` powershell
([adsi]'').distinguishedName
```

#### Script which will create the full **LDAP path** required for enumeration
``` powershell
$PDC = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().PdcRoleOwner.Name
$DN = ([adsi]'').distinguishedName 
$LDAP = "LDAP://$PDC/$DN"
$LDAP
```
Save it as `enumeration.ps1` The Run it on PowerShell
``` powershell
powershell -ep bypass
.\enumeration.ps1
```
## Adding Search Functionality to our Script
To do this, we will use two .NET classes that are located in the _System.DirectoryServices_ namespace, more specifically the [_DirectoryEntry_](https://learn.microsoft.com/en-us/dotnet/api/system.directoryservices.directoryentry?view=dotnet-plat-ext-6.0) and [_DirectorySearcher_](https://learn.microsoft.com/en-us/dotnet/api/system.directoryservices.directorysearcher?view=dotnet-plat-ext-6.0) classes. Let's discuss these before we implement them.

---
One thing to note with _DirectoryEntry_ is that we can pass it credentials to authenticate to the domain. However, since we are already logged in, there is no need to do that here.

---
When creating an instance of _DirectorySearcher_, we must specify the AD service we want to query in the form of the [_SearchRoot_](https://learn.microsoft.com/en-us/dotnet/api/system.directoryservices.directorysearcher.searchroot?view=dotnet-plat-ext-6.0) property.
The _DirectorySearcher_ documentation lists [_FindAll()_](https://learn.microsoft.com/en-us/dotnet/api/system.directoryservices.directorysearcher.findall?view=dotnet-plat-ext-7.0#system-directoryservices-directorysearcher-findall), which returns a collection of all the entries found in AD.

Let's **implement these two classes into our script**. The code below shows the relevant part of the script:
``` powershell
$PDC = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().PdcRoleOwner.Name
$DN = ([adsi]'').distinguishedName 
$LDAP = "LDAP://$PDC/$DN"

$direntry = New-Object System.DirectoryServices.DirectoryEntry($LDAP)

$dirsearcher = New-Object System.DirectoryServices.DirectorySearcher($direntry)
$dirsearcher.FindAll()
```

### Filter that will sift through the [_samAccountType_](https://learn.microsoft.com/en-us/windows/win32/adschema/a-samaccounttype) attribute
The **`samAccountType`** attribute is a property in Active Directory (AD) that specifies the type of object represented, such as a user, computer, or group. It's part of the **Security Account Manager (SAM)** in AD, which handles object types and their security contexts.

### Understanding `samAccountType`

1. **SAM (Security Account Manager)**:
    
    - SAM is a database that stores information about security principals (e.g., users, computers, groups) in a domain.
    - `samAccountType` is an attribute that categorizes objects in this database.
2. **Purpose of `samAccountType`**:
    
    - It helps distinguish between different types of objects in AD.
    - Each type of object has a specific numeric value assigned to its `samAccountType`.
3. **Common `samAccountType` Values**: These values are hexadecimal constants, often represented in decimal form:
    
    - `0x30000000` (Decimal **805306368**): Represents **user objects**.
    - `0x30000001` (Decimal **805306369**): Represents **computer objects**.
    - `0x30000002` (Decimal **805306370**): Represents **group objects**.
    - `0x10000000` (Decimal **268435456**): Represents a **domain object** (top of the hierarchy).
    - `0x20000000` (Decimal **536870912**): Represents a **built-in group**, such as default administrative or system groups.
4. **Filtering with `samAccountType`**:
    
    - By setting `samAccountType=805306368`, the script filters results to include **only user objects** in the LDAP query.

### Final Script
``` powershell
$PDC = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().PdcRoleOwner.Name
$DN = ([adsi]'').distinguishedName 
$LDAP = "LDAP://$PDC/$DN"

$direntry = New-Object System.DirectoryServices.DirectoryEntry($LDAP)

$dirsearcher = New-Object System.DirectoryServices.DirectorySearcher($direntry)
$dirsearcher.filter="samAccountType=805306368"
$dirsearcher.FindAll()
```
#### Get object, which are stored in the _Properties_ field.
``` powershell
$domainObj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$PDC = $domainObj.PdcRoleOwner.Name
$DN = ([adsi]'').distinguishedName 
$LDAP = "LDAP://$PDC/$DN"

$direntry = New-Object System.DirectoryServices.DirectoryEntry($LDAP)

$dirsearcher = New-Object System.DirectoryServices.DirectorySearcher($direntry)
$dirsearcher.filter="samAccountType=805306368"
$result = $dirsearcher.FindAll()

Foreach($obj in $result)
{
    Foreach($prop in $obj.Properties)
    {
        $prop
    }

    Write-Host "-------------------------------"
}
```
#### Filter based on any property of any object type.
Example filter by name 
Adding the name property to the filter and only print the "memberof" attribute in the nested loop
``` powershell
$dirsearcher = New-Object System.DirectoryServices.DirectorySearcher($direntry)

$dirsearcher.filter="name=jeffadmin"
$result = $dirsearcher.FindAll()

Foreach($obj in $result)
{
    Foreach($prop in $obj.Properties)
    {
        $prop.memberof
    }

    Write-Host "-------------------------------"
}
```


---
## AD Enumeration with **PowerView.ps1

### Get the PowerView.ps1
From kali linux `/usr/share/windows-resources/powersploit/Recon/PowerView.ps1`
From WebSite [Link](https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1)
###  commands and examples  --> **[[PowerView]]**
In order to view the permissions, we'll use the PowerShell [**Get-Acl**](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-acl?view=powershell-7.3) cmdlet. This command will essentially retrieve the permissions for the object we define with the **-Path** flag and print them in our PowerShell prompt.
``` powershell
Get-Acl -Path HKLM:SYSTEM\CurrentControlSet\Services\LanmanServer\DefaultSecurity\ | fl
```
The groups and users that have either _FullControl_ or _ReadKey_, meaning they can all read the **SrvsvcSessionInfo** key itself.

However, the _BUILTIN_ group, _NT AUTHORITY_ group, _CREATOR OWNER_ and _APPLICATION PACKAGE AUTHORITY_ are defined by the system, and do not allow _NetSessionEnum_ to enumerate this registry key from a remote standpoint.

---

# Summary 
## A total Enum Script module:

``` powershell
function LDAPSearch {
    param (
        [string]$LDAPQuery
    )

    $PDC = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().PdcRoleOwner.Name
    $DistinguishedName = ([adsi]'').distinguishedName

    $DirectoryEntry = New-Object System.DirectoryServices.DirectoryEntry("LDAP://$PDC/$DistinguishedName")

    $DirectorySearcher = New-Object System.DirectoryServices.DirectorySearcher($DirectoryEntry, $LDAPQuery)

    return $DirectorySearcher.FindAll()
}

function Get-LDAPObjectProperties {
    param (
        [string]$ObjectName
    )

    $PDC = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().PdcRoleOwner.Name
    $DistinguishedName = ([adsi]'').distinguishedName

    $DirectoryEntry = New-Object System.DirectoryServices.DirectoryEntry("LDAP://$PDC/$DistinguishedName")

    $DirectorySearcher = New-Object System.DirectoryServices.DirectorySearcher($DirectoryEntry)
    $DirectorySearcher.Filter = "name=$ObjectName"

    $Results = $DirectorySearcher.FindAll()

    Foreach ($Result in $Results) {
        Foreach ($Property in $Result.Properties.PropertyNames) {
            Write-Host "$Property : $($Result.Properties[$Property])"
        }
        Write-Host "-------------------------------"
    }
}
```

- Save the script as `function.ps1`
``` powershell
powershell -ep bypass
Import-Module .\function.ps1
```
- Use the `LDAPSearch` function to query objects in the domain. For example:
``` powershell
LDAPSearch -LDAPQuery "(samAccountType=805306368)"
```
-  **Common `samAccountType` Values**: These values are hexadecimal constants, often represented in decimal form:
    - `0x30000000` (Decimal **805306368**): Represents **user objects**.
    - `0x30000001` (Decimal **805306369**): Represents **computer objects**.
    - `0x30000002` (Decimal **805306370**): Represents **group objects**.
    - `0x10000000` (Decimal **268435456**): Represents a **domain object** (top of the hierarchy).
    - `0x20000000` (Decimal **536870912**): Represents a **built-in group**, such as default administrative or system groups.
- Use the `LDAPSearch` function to **query all groups**:
``` powershell
LDAPSearch -LDAPQuery "(objectclass=group)"
```
To enumerate every group available in the domain and also display the user members After importing the module `function.ps1` 
This allows us to select specific attributes we are interested in. For example, let's focus on the _CN_ and _member_ attributes:
``` powershell
foreach ($group in $(LDAPSearch -LDAPQuery "(objectCategory=group)")) {$group.properties | select {$_.cn}, {$_.member}}
```
Get the **group members**:
``` powershell
$group = LDAPSearch -LDAPQuery "(&(objectCategory=group)(cn=Management Department*))"
$group.properties.member
```
