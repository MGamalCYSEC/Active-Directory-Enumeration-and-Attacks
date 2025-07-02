 we can pull the domain password policy in several ways, depending on how the domain is configured and whether or not we have valid domain credentials.
 **NOTE**: The default password policy when a new domain is created is as follows, and there have been plenty of organizations that never changed this policy:
Minimum password length:	7
- Password must meet complexity requirements:	Enabled
- Account lockout duration:	Not set
- Maximum password age:	42 days

 # Enumerating the Password Policy - from Linux - Credentialed
 ```shell
crackmapexec smb <target_IP> -u <UserName> -p <Password> --pass-pol
netexec smb <target_IP> -u <UserName> -p <Password> --pass-pol
```
# Enumerating the Password Policy - from Linux - SMB NULL Sessions
```shell
rpcclient -U "" -N <target_IP>
rpcclient $> getdompwinfo
```
![image](https://github.com/user-attachments/assets/e2004298-1093-4322-80fc-c823e86ac78e)
Explanation:
**min_password_length**: 8
This means the minimum password length required in the domain is 8 characters.
**password_properties**: 0x00000001
This value is a bitmask that represents which password policies are enforced. In this case:
00000001, meaning only the first bit is set.
**The first bit corresponds to: DOMAIN_PASSWORD_COMPLEX**
This flag means that the domain enforces **password complexity rules**:
According to Microsoft, **complex passwords** must meet the following:
- Must not contain the user's account name or parts of the user's full name
- Must be at least 6 characters (but overridden by your `min_password_length: 8`)
- Must contain characters from **three of the following four categories**:
    - Uppercase letters (A–Z)
    - Lowercase letters (a–z)
    - Numbers (0–9)
    - Special characters (e.g., `!@#$%^&*`)
[Generated GUIDs using just capital letters and numbers (`A-Z and 0-9`)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Automation/Generated_GUIDs.sh)
# Enumerating the Password Policy - from Windows
### Using net.exe
```cmd
net accounts
```
![image](https://github.com/user-attachments/assets/5c5f59b1-d85b-41ab-9892-05749a197c69)
- Passwords never expire (Maximum password age set to Unlimited)
- The minimum password length is 8 so weak passwords are likely in use
- The lockout threshold is 5 wrong passwords
- Accounts remained locked out for 30 minutes
### Using PowerView
```powershell
import-module .\PowerView.ps1
Get-DomainPolicy
```
### Establish a null session from windows
```cmd
C:\> net use \\DC01\ipc$ "" /u:""
The command completed successfully.
```
Error: Account is Disabled
```cmd
C:\> net use \\DC01\ipc$ "" /u:guest
System error 1331 has occurred.

This user can't sign in because this account is currently disabled.
```
Error: Password is Incorrect
```cmd
C:\htb> net use \\DC01\ipc$ "password" /u:guest
System error 1326 has occurred.

The user name or password is incorrect.
```
Error: Account is locked out (Password Policy)
```cmd
C:\htb> net use \\DC01\ipc$ "password" /u:guest
System error 1909 has occurred.

The referenced account is currently locked out and may not be logged on to.
```
This way we can know an important NOTE that Policy
