Suportive Usernames Lists [jsmith.txt](https://github.com/insidetrust/statistically-likely-usernames/blob/master/jsmith.txt) or [jsmith2.txt](https://github.com/insidetrust/statistically-likely-usernames/blob/master/jsmith2.txt)
# NULL Sessions to Pull User List
### Using **enum4linux-ng** or **enum4linux**: 
```shell SMB NULL Sessions
enum4linux-ng -P <target_IP> -oA <Out>
enum4linux -U <target_IP>  | grep "user:" | cut -f2 -d"[" | cut -f1 -d"]"
```
### Using **netexec** or **crackmapexec**:
``` shell
netexec smb <target_IP> --shares -u '' -p ''
netexec smb <target_IP> -u guest -p "" --rid-brute
netexec smb <target_IP> -u '' -p "" --rid-brute
```
### Using **rpcclient**
```shell
rpcclient -U "" -N <target_IP>
rpcclient $> enumdomusers
```
Extract Users Descriptions/Comments for extra informations with rpc
[Script.sh](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Automation/Users_Description_Comment_RPC.sh)
### Users with **LDAP** Anonymous
```shell
ldapsearch -h <target_IP> -x -b "DC=<Domain>,DC=<com>" -s sub "(&(objectclass=user))"  | grep sAMAccountName: | cut -f2 -d" "
```
### Using [windapsearch](https://github.com/ropnop/windapsearch)
```shell
./windapsearch.py --dc-ip <target_IP> -u "" -U
```
### Enumerating Users with **Kerbrute**
```shell
kerbrute userenum -d <domain.local> --dc <target_IP> /path/to/users/list/jsmith.txt
```
