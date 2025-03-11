# Active Directory Persistence
Active Directory environments are often targeted by adversaries looking to maintain long-term persistence within a network. Two prominent techniques for achieving this are Golden Ticket attacks and abuse of the Shadow Copy Service (VSS). This repository provide a Step-by-Step Exploitation for each.
## 1. Golden Ticket Attack
The core of the Golden Ticket attack lies in the manipulation of the Ticket Granting Ticket (TGT)—a credential encrypted using a secret key associated with the krbtgt account. By compromising this account, attackers can forge their own TGTs, known as Golden Tickets. This allows them to impersonate any user, including Domain Administrators, effectively granting unfettered access to all domain resources.

#### Prerequisites:
- **krbtgt Hash**: Extraction of the NTLM hash for the krbtgt account is essential. This step typically requires Domain Admin privileges or an outright compromise of a Domain Controller.
- **Domain SID**: The unique Security Identifier of the domain (e.g., S-1-5-21-1987370270-658905905-1781884369) must be obtained.
- **Mimikatz Access**: Tools like Mimikatz are used on domain-joined systems to generate and inject the forged tickets without needing elevated privileges for ticket injection.
## 2. Shadow Copy (VSS) Abuse
Shadow Copy Service (VSS) is a built-in Microsoft feature designed to create point-in-time snapshots of files or volumes—even while they are in use—to facilitate backups and data recovery. However, attackers can exploit VSS to access sensitive files, such as the NTDS.dit (Active Directory database), and the SYSTEM hive, which holds the boot key necessary for decrypting the NTDS.dit.

#### Prerequisites:
- **Domain Admin Access**: Executing these commands on a Domain Controller generally requires Domain Admin privileges, given the elevated access necessary to interact with these critical files.
- **Volume Shadow Copy Utilities**: Tools such as vssadmin or diskshadow are used to create and manipulate shadow copies, enabling the extraction of these sensitive files.
