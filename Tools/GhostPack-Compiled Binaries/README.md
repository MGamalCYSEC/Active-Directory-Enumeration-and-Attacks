Compiled binaries for [GhostPack](https://github.com/GhostPack) 
To check the .NET Framework version installed on a Windows machine using PowerShell, you can query the registry where .NET Framework versions are stored.
``` powershell
Get-ChildItem "HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP" -Recurse |
Get-ItemProperty -Name Version -ErrorAction SilentlyContinue |
Where-Object { $_.Version -match "^\d" } |
Select-Object -Property PSChildName, Version
```
