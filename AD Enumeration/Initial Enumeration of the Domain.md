I have no access on Any machine on domain
# Passive identification of any hosts in the network
**Key Points**
- **AD Users** :We are trying to enumerate valid user accounts we can target for password spraying.
- **AD Joined Computers** Key Computers include Domain Controllers, file servers, SQL servers, web servers, Exchange mail servers, database servers, etc.
- **Key Services** Kerberos, NetBIOS, LDAP, DNS
- **Vulnerable Hosts and Services** 	Anything that can be a quick win. ( a.k.a an easy host to exploit and gain a foothold)

**Focus on**:
- _ARP Requests/Replies_: Identify active devices and their MAC addresses.
- _MDNS (Multicast DNS)_: Look for device names and network services.
- _Broadcast Domain Traffic_: Understand the network’s broadcast domain since switched networks limit visibility.
## Identifying Hosts
### Wireshark
```shell
sudo -E wireshark
```
Take some time to listen to the network and see what's going on "put our ear to the wire".
We notice some ARP requests and replies, MDNS, and other basic layer two packets (since we are on a switched network, we are limited to the current broadcast domain) some of which we can see below.
### Tcpdump 
```shell
sudo tcpdump -i tun0 -nn -v
sudo tcpdump -i tun0 arp
```
Our first look at network traffic pointed us to a couple of hosts via MDNS and ARP.
### Responder
```shell
sudo responder -I tun0 -A
```
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
