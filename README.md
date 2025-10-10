# 🗂️🌐🛡️ Active-Directory-Enumeration-and-Attacks
This repository is dedicated to exploring Active Directory (AD) enumeration techniques and attack strategies for penetration testing and security assessments. It serves as a comprehensive resource for cybersecurity professionals
# 💡 0. Have No access to any domain user
## 0.1. [Initial Enumeration of the Domain](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Initial%20Enumeration%20of%20the%20Domain.md)
  - 0.1.1. [Passive identification of any hosts in the network](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Passive_identification.md)
  - 0.1.2. [Active identification of any hosts in the network](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Active_identification.md)
## 0.2. [Password Spraying](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Password%20Spraying.md)
  - 0.2.1. [NULL Sessions to Pull User List](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/NULL%20Sessions.md#null-sessions-to-pull-user-list)
  - 0.2.2. [Generated GUIDs From Password Policy](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Password%20Policy%20Enum.md)
  - 0.2.3. **Internal Password Spraying** (At this stage  we have created a wordlist)
     - 0.2.3.1. [Internal Password Spraying From Linux](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Password%20Spraying%20from%20Linux.md) 🐧
     - 0.2.3.2. [Internal Password Spraying From Windows](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Password%20Spraying%20from%20Windows.md) 🖥️ (Foothold on machine joint domain)
# 🔍 1. Enumerating Active Directory environment (Foothold) 
## 1.1. [Automatic Enumeration Using BloodHound](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/AD%20Automatic%20Enumeration.md)
## 1.2. Manual Enumeration
  - 1.2.1. [Enumerating Security Controls](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Enumerating%20Security%20Controls.md) 🖥️ - From **Windows**
  - 1.2.2. [Credentialed less Domain Users Enumeration](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/DomainUsers.md) 🐧 -From Linux
  - 1.2.3. [Credentialed Enumeration](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Credentialed%20Enumeration%20from%20linux.md) 🐧 - From **Linux**
      - 1.2.3.1. [Using CrackMapExec](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Credentialed%20Enumeration%20from%20linux.md#using-crackmapexec-now-netexec)
      - 1.2.3.2. [Using SMBMap](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Credentialed%20Enumeration%20from%20linux.md#using-smbmap)
      - 1.2.3.3. [Using rpcclient](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Credentialed%20Enumeration%20from%20linux.md#using-rpcclient)
      - 1.2.3.4. [Impacket Toolkit](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Credentialed%20Enumeration%20from%20linux.md#impacket-toolkit)
      - 1.2.3.5. [Using Windapsearch](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Credentialed%20Enumeration%20from%20linux.md#using-windapsearch-that-utilizing-ldap-queries)
      - 1.2.3.6. [Get Weak Credentials](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Get_Weak_Credentials.md)
  - 1.2.4. [Credentialed Enumeration](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Credentialed%20Enumeration%20-%20from%20Windows.md) 🖥️ - From **Windows**
      - 1.2.4.1. [Using PowerShell and dot_NET Classes](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Using%20PowerShell%20and%20dot_NET%20Classes.md)
      - 1.2.4.2. [ActiveDirectory PowerShell Module](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/ActiveDirectory%20PowerShell.md)
      - 1.2.4.3. [Using PowerView](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/PowerView.md)
      - 1.2.4.4. [Using SharpView](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/SharpView.md)
      - 1.2.4.5. [Using Snaffler - enumerating Shares](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Snaffler.md)
      - 1.2.4.6. [LLMNR/NBT-NS Poisoning](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/LLMNR/NBT-NS%20Poisoning.md)
  - 1.2.5. [Living Off the Land](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Living%20Off%20the%20Land.md)
      - 1.2.3.1. [Basic Enumeration Commands](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Living%20Off%20the%20Land.md#basic-enumeration-commands)
      - 1.2.3.2. [Using built-in modules in PowerShell](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Living%20Off%20the%20Land.md#using-built-in-modules-in-powershell)
      - 1.2.3.3. [Examining the PowerShell Event Log](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Living%20Off%20the%20Land.md#examining-the-powershell-event-log)
      - 1.2.3.4. [Checking Defenses](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Living%20Off%20the%20Land.md#checking-defenses)
      - 1.2.3.5. [Network Information](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Living%20Off%20the%20Land.md#network-information)
      - 1.2.3.6. [Windows Management Instrumentation (WMI)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Living%20Off%20the%20Land.md#windows-management-instrumentation-wmi)
      - 1.2.3.7. [Net Commands](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Living%20Off%20the%20Land.md#net-commands)
      - 1.2.3.8. [Dsquery](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Living%20Off%20the%20Land.md#dsquery)
  - 1.2.6. [kerbrute](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Manual%20Enumeration/Kerbrute.md)

---
# 2. ⚔️ Active Directory Attacks
- 2.1. Cashed AD Credentials
- 2.2. [AD Password Attacks](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/AD%20Password%20Attacks.md) **If You Got User Password Try It's Password For all List of Users May Be its a default Password**
- 2.3. [AS-REP Roasting](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/AS-REP%20Roasting.md) 
  DONT_REQ_PREAUTH Appears from `Get-DomainUser -PreauthNotRequired` on powerview
- 2.4. [Kerberoasting](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Kerberoasting.md) 
  - 2.4.1. [Overview](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Kerberoasting.md#kerberoasting)
  - 2.4.2. [Using Kali](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Kerberoasting.md#perform-kerberoasting-using-kali) 🐧
  - 2.4.3. [Using Windows (joined domain)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Kerberoasting.md#perform-kerberoasting-on-windows-joined-domain) 🖥️
  - 2.4.3. [Replay Tickets with Impacket](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Kerberoasting.md#replay-tickets-with-impacket)
  - 2.4.4. [Kerberos Double Hop Problem](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Kerberos%20Double%20Hop%20Problem.md)
- 2.5. [AD Certificate Authority (pfx)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/AD%20Certificate%20Authority.md) 
- 2.6. [Access Control List (ACL) Abuse](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/tree/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse)
  - 2.6.1. [Get Remote Access Users](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/Remote%20Access%20Users.md)
  - 2.6.2. [ReadGMSAPassword](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/ReadGMSAPassword.md)
  - 2.6.3. [ForceChangePassword](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/ForceChangePassword.md)
  - 2.6.4. [DS-Replication GetChanges+GetChangesAll -> DCSync attack](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/DS-Replication-Get-Changes_and_all.md)
  - 2.6.5. [AS-REP Roasting attack (PreauthNotRequired / dontreqpreauth)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/AS-REP%20Roasting.md)
  - 2.6.6. [SPN Jacking](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/SPN%20Jacking.md)
  - 2.6.7. [GenericWrite AddMember in target group](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/GenericWrite.md)
  - 2.6.8. [ReadLAPSPassword](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/ReadLAPSPassword.md)
  - 2.6.9. [Abusing **WriteOwner** permissions](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteOwner.md)
  - 2.6.10.[SeBackupPrivilege](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/SeBackupPrivilege.md) _whoami /priv_
  - 2.6.11. WriteDacl
     - 2.6.11.1. [WriteDacl On User](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteDacl%20On%20User.md)
     - 2.6.11.2. [WriteDacl On Groups](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteDacl%20On%20Groups.md)
     - 2.6.11.3. [WriteDacl On Computers](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteDacl%20On%20Computers.md)
     - 2.6.11.4. [WriteDacl On Domains](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteDacl%20On%20Domains.md)
     - 2.6.11.5. [WriteDacl on Default Domain Policy](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/WriteDacl%20on%20Default%20Domain%20Policy.md)
  - 2.6.121. [GenericAll](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/GenericAll.md)
     - 2.6.12.1. [On a User A](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/ForceChangePassword.md)
     - 2.6.12.2. [On a User Create fake SPN](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/SPN%20Jacking.md)
     - 2.6.12.3. [On a Computer](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Access%20Control%20List%20(ACL)%20Abuse/GenericAll%20permissions%20to%20the%20computer%20(RBCD).md)
- 2.7. Bleeding Edge Vulnerabilities
  - 2.7.1. [NoPac (**SamAccountName** Spoofing)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/NoPac%20(SamAccountName%20Spoofing).md) ([2021-42278](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42278) and [2021-42287](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42287))
  - 2.7.1. [PrintNightmare](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/PrintNightmare.md) ([CVE-2021-34527](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527) and [CVE-2021-1675](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-1675))
  - 2.7.2. [PetitPotam (MS-EFSRPC)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/PetitPotam%20(MS-EFSRPC).md) ([CVE-2021-36942](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-36942))
- 2.8. Domain Trusts
  - 2.8.1. [Enumerating Trust Relationships](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Domain%20Trusts/Domain%20Trusts%20Enum.md)
  - 2.8.2. [Attacking Domain Trusts - Child -> Parent Trusts](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Domain%20Trusts/Attacking%20Domain%20Trusts%20From%20Windows.md) 🖥️ - From Windows
  - 2.8.3. [Attacking Domain Trusts - Child -> Parent Trusts](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Domain%20Trusts/Attacking%20Domain%20Trusts%20From%20Linux.md) 🐧 - From Linux
  - 2.8.4. [Attacking Domain Trusts - Cross-Forest Trust Abuse](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Domain%20Trusts/Attacking%20Domain%20Trusts%20-%20Cross-Forest%20-%20Windows.md) 🖥️ - From Windows
  - 2.8.5. [Attacking Domain Trusts - Cross-Forest Trust Abuse](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Domain%20Trusts/Attacking%20Domain%20Trusts%20-%20Cross-Forest%20-%20Linux.md) 🐧 - From Linux
- 2.9. Miscellaneous Misconfigurations
  - 2.9.1. [Exchange Related Group Membership](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/tree/main/Active%20Directory%20Attacks/Miscellaneous%20Misconfigurations)
---
# 3. 🔀 [Active Directory Lateral Movement](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/tree/main/AD%20Lateral%20Movement)
- 3.1. [DCOM Lateral Movement](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/DCOM.md)
- 3.2. [Overpass the Hash (OtH)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/Overpass%20the%20Hash.md)
- 3.3. [Pass the Ticket (PtT)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/Pass%20the%20Ticket.md)
- 3.4. [Pass the Certificate (PFX)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/Pass%20the%20Certificate(PFX).md)
- 3.5. [PsExec](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/PsExec.md)
- 3.6. [WMI (Windows Management Instrumentation)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/WMI.md) 🖥️
- 3.7. [WinRM (Windows Remote Management)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Lateral%20Movement/WinRM.md) 🖥️
- 3.8. [Remote Desktop Service (RDP)]() 🖥️🐧
---
# 4. Miscellaneous
- 4.1. [RunAs (Run specific processes with different permissions than the user's current logon )](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Active%20Directory%20Attacks/Miscellaneous/RunAs.md)
- 5.1. [Connect to the MSSQL database Server](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Miscellaneous/MSSQLClient.md)
