# Active-Directory-Enumeration-and-Attacks
This repository is dedicated to exploring Active Directory (AD) enumeration techniques and attack strategies for penetration testing and security assessments. It serves as a comprehensive resource for cybersecurity professionals
# 1. Enumerating Active Directory environment
## 1.1. [Automatic Enumeration Using BloodHound](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/AD%20Automatic%20Enumeration.md)
## 1.2. Manual Enumeration
  - 1.2.1. [Using PowerShell and dot_NET Classes](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Using%20PowerShell%20and%20dot_NET%20Classes.md)
  - 1.2.2. [kerbrute](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Kerbrute.md)
  - 1.2.3. [LLMNR & NBT-NS Primer](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/LLMNR%20%26%20NBT-NS%20Primer.md) Using **responder** and **Inveigh**
  - 1.2.4. PowerView

---
# 2. Active Directory Attacks
- 2.1. Cashed AD Credentials
- 2.2. [AD Password Attacks](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/AD%20Password%20Attacks.md)
- 2.3. [AS-REP Roasting](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/AS-REP%20Roasting.md)
  DONT_REQ_PREAUTH Appears from `Get-DomainUser -PreauthNotRequired` on powerview
- 2.4. [Kerberoasting](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Kerberoasting.md)
- 2.5. Access Control List (ACL) Abuse
  - 2.5.1. [ReadGMSAPassword](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/ReadGMSAPassword.md)
  - 2.5.2. [ForceChangePassword](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/ForceChangePassword.md)

---
# 3. [Active Directory Lateral Movement](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/tree/main/AD%20Lateral%20Movement)
- 3.1. [DCOM Lateral Movement](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/DCOM.md)
- 3.2. [Overpass the Hash (OtH)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/Overpass%20the%20Hash.md)
- 3.3. [Pass the Ticket (PtT)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/Pass%20the%20Ticket.md)
- 3.4. [PsExec](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/PsExec.md)
- 3.5. [WMI (Windows Management Instrumentation)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/WMI.md)
- 3.6. [WinRM (Windows Remote Management)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/WinRM.md)
