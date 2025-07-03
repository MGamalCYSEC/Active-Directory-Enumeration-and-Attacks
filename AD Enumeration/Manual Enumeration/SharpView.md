# Using SharpView
SharpView, a .NET port of PowerView. Many of the same functions supported by PowerView can be used with SharpView. We can type a method name with -Help to get an argument list.
```powershell
.\SharpView.exe Get-DomainUser -Help
```
![image](https://github.com/user-attachments/assets/eead44f6-380c-4ce6-9985-f3af9ecc6645)
**Enumerate information about a specific user**
```powershell
.\SharpView.exe Get-DomainUser -Identity <username>
```
