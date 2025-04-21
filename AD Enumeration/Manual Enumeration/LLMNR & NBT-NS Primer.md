# LLMNR & NBT-NS Primer
[Link-Local Multicast Name Resolution](https://datatracker.ietf.org/doc/html/rfc4795) (LLMNR) and [NetBIOS Name Service](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-2000-server/cc940063(v=technet.10)?redirectedfrom=MSDN) (NBT-NS) are Microsoft Windows components that serve as alternate methods of host identification that can be used when DNS fails.
LLMNR uses port `5355` over UDP natively. If LLMNR fails, the NBT-NS will be used. NBT-NS identifies systems on a local network by their NetBIOS name. NBT-NS utilizes port `137` over UDP.
LLMNR/NBT-NS are used for name resolution, ANY host on the network can reply.
LLMNR/NBT-NS allow any host on the network to respond to name resolution requests, enabling attackers to use tools like `Responder` for poisoning. By spoofing an authoritative name resolution source in the broadcast domain, attackers trick victims into communicating with their rogue system. This captures NetNTLM hashes for offline brute-force attacks or relaying to exploit protocols like `LDAP`. Combined with disabled SMB signing, this method can escalate to administrative domain access. SMB Relay will be detailed in lateral movement discussions.
## LLMNR/NBT-NS Poisoning - from Linux
### Responder
``` shell
sudo responder -I <interface>
```
Responder will print it out on screen and write it to a log file per host located in the `/usr/share/responder/logs` directory. Hashes are saved in the format `(MODULE_NAME)-(HASH_TYPE)-(CLIENT_IP).txt`

### Cracking an NTLMv2 Hash With Hashcat
``` shell
hashcat -m 5600 hash_ntlmv2 /usr/share/wordlists/rockyou.txt -r rules/best64.rule
```

## LLMNR/NBT-NS Poisoning - from Windows

By using tool [Inveigh](https://github.com/Kevin-Robertson/Inveigh) and attempt to capture another set of credentials. [Inveigh](https://github.com/Kevin-Robertson/Inveigh) works similar to Responder, but is written in PowerShell and C#. Inveigh can listen to IPv4 and IPv6 and several other protocols, including `LLMNR`, DNS, `mDNS`, NBNS, `DHCPv6`, ICMPv6, `HTTP`, HTTPS, `SMB`, LDAP, `WebDAV`, and Proxy Auth.

On powershell (Open as admin)
``` powershell
Import-Module .\Inveigh.ps1
(Get-Command Invoke-Inveigh).Parameters
Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y
```

