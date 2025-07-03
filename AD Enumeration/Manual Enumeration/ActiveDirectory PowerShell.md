# ActiveDirectory PowerShell Module
The [Get-Module](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-module?view=powershell-7.2) cmdlet, will list all available modules, their version, and potential commands for use.
``` powershell
Get-Module
```
If the module is not loaded, run `Import-Module ActiveDirectory` to load it for use.
``` powershell
Import-Module ActiveDirectory
Get-Module
```
Now we will start enumeration
**Get Domain Info**
``` powershell
Get-ADDomain
```
Use the **Get-ADUser** cmdlet. We will be filtering for accounts with the _ServicePrincipalName_ property populated. This will get us a listing of accounts that may be susceptible to a Kerberoasting attack.
``` powershell
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName
```
**Verify domain trust relationships** using the [Get-ADTrust](https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-adtrust?view=windowsserver2022-ps) cmdlet
``` powershell
Get-ADTrust -Filter *
```
 **Group Enumeration**
 ``` powershell
 Get-ADGroup -Filter * | select name
```
**Detailed Group Info**
``` powershell
Get-ADGroup -Identity "Backup Operators"
```
**Group Membership**
``` powershell
Get-ADGroupMember -Identity "Backup Operators"
```
