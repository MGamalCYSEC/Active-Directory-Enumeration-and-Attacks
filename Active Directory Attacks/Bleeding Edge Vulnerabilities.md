# Bleeding Edge Vulnerabilities 
## NoPac (**SamAccountName** Spoofing)
A great example of an emerging threat is the [Sam_The_Admin vulnerability](https://techcommunity.microsoft.com/t5/security-compliance-and-identity/sam-name-impersonation/ba-p/3042699), also called `noPac` or referred to as `SamAccountName Spoofing` released at the end of 2021. This vulnerability encompasses two CVEs [2021-42278](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42278) and [2021-42287](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42287), allowing for intra-domain privilege escalation from any standard domain user to Domain Admin level access in one single command.


| 2021-42278                                                                 | 2021-42287                                                                                    |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `42278` is a bypass vulnerability with the Security Account Manager (SAM). | `42287` is a vulnerability within the Kerberos Privilege Attribute Certificate (PAC) in ADDS. |



