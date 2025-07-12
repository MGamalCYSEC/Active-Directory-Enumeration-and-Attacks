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
