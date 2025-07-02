 we can pull the domain password policy in several ways, depending on how the domain is configured and whether or not we have valid domain credentials.
 # Enumerating the Password Policy - from Linux - Credentialed
 ```shell
crackmapexec smb <target_IP> -u <UserName> -p <Password> --pass-pol
netexec smb <target_IP> -u <UserName> -p <Password> --pass-pol
```
# Enumerating the Password Policy - from Linux - SMB NULL Sessions
```shell
rpcclient -U "" -N <target_IP>
```
