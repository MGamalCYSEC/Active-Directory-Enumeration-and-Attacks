# Active-Directory-Enumeration-and-Attacks
This repository is dedicated to exploring Active Directory (AD) enumeration techniques and attack strategies for penetration testing and security assessments. It serves as a comprehensive resource for cybersecurity professionals
# 1. Enumerating Active Directory environment
## 1.1. [Automatic Enumeration Using BloodHound](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/AD%20Automatic%20Enumeration.md)
## 1.2. Manual Enumeration
  - 1.2.1. [Domain Users Enumeration](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/DomainUsers.md)
  - 1.2.2. [Using PowerShell and dot_NET Classes](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Using%20PowerShell%20and%20dot_NET%20Classes.md)
  - 1.2.3. [kerbrute](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Kerbrute.md)
  - 1.2.4. [LLMNR & NBT-NS Primer](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/LLMNR%20%26%20NBT-NS%20Primer.md) Using **responder** and **Inveigh**
  - 1.2.4. PowerView

---
# 2. Active Directory Attacks
- 2.1. Cashed AD Credentials
- 2.2. [AD Password Attacks](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/AD%20Password%20Attacks.md)
- 2.3. [AS-REP Roasting](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/AS-REP%20Roasting.md)
  DONT_REQ_PREAUTH Appears from `Get-DomainUser -PreauthNotRequired` on powerview
- 2.4. [Kerberoasting](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Kerberoasting.md)
- 2.5. [Access Control List (ACL) Abuse](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/tree/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse)
  - 2.5.1. [ReadGMSAPassword](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/ReadGMSAPassword.md)
  - 2.5.2. [ForceChangePassword](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/ForceChangePassword.md)
  - 2.5.3. [AS-REP Roasting attack (PreauthNotRequired / dontreqpreauth)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/AS-REP%20Roasting.md)
  - 2.5.4. [SPN Jacking](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/SPN%20Jacking.md)
  - 2.5.5. [GenericWrite AddMember in target group](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/GenericWrite.md)
  - 2.5.6. [ReadLAPSPassword](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/ReadLAPSPassword.md)
  - 2.5.7. [Abusing **WriteOwner** permissions](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteOwner.md)
  - 2.5.8.[SeBackupPrivilege](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/SeBackupPrivilege.md) _whoami /priv_
  - 2.5.9. WriteDacl
     - 2.5.9.1. [WriteDacl On User](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteDacl%20On%20User.md)
     - 2.5.9.2. [WriteDacl On Groups](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteDacl%20On%20Groups.md)
     - 2.5.9.3. [WriteDacl On Computers](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteDacl%20On%20Computers.md)
     - 2.5.9.4. [WriteDacl On Domains](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteDacl%20On%20Domains.md)
     - 2.5.9.5. [WriteDacl on Default Domain Policy](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteDacl%20on%20Default%20Domain%20Policy.md)
- 2.6. Bleeding Edge Vulnerabilities
  - 2.6.1. [NoPac (**SamAccountName** Spoofing)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/NoPac%20(SamAccountName%20Spoofing).md)
  - 2.6.1. [PrintNightmare](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/PrintNightmare.md)
  - 2.6.2. PetitPotam (MS-EFSRPC)
- 2.7. Miscellaneous Misconfigurations
  - 2.7.1. 
---
# 3. [Active Directory Lateral Movement](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/tree/main/AD%20Lateral%20Movement)
- 3.1. [DCOM Lateral Movement](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/DCOM.md)
- 3.2. [Overpass the Hash (OtH)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/Overpass%20the%20Hash.md)
- 3.3. [Pass the Ticket (PtT)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/Pass%20the%20Ticket.md)
- 3.4. [Pass the Certificate (PFX)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/Pass%20the%20Certificate(PFX).md)
- 3.5. [PsExec](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/PsExec.md)
- 3.6. [WMI (Windows Management Instrumentation)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/WMI.md)
- 3.7. [WinRM (Windows Remote Management)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/WinRM.md)
