I have no access on Any machine on domain
**Key Points**
- **AD Users** :We are trying to enumerate valid user accounts we can target for password spraying.
- **AD Joined Computers** Key Computers include Domain Controllers, file servers, SQL servers, web servers, Exchange mail servers, database servers, etc.
- **Key Services** Kerberos, NetBIOS, LDAP, DNS
- **Vulnerable Hosts and Services** 	Anything that can be a quick win. ( a.k.a an easy host to exploit and gain a foothold)

**Focus on**:
- _ARP Requests/Replies_: Identify active devices and their MAC addresses.
- _MDNS (Multicast DNS)_: Look for device names and network services.
- _Broadcast Domain Traffic_: Understand the network’s broadcast domain since switched networks limit visibility.

1. [Passive identification of any hosts in the network](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Passive_identification.md)
2. [Active identification of any hosts in the network](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Active_identification.md)
