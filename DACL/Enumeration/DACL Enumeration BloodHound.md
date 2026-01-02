Back to [Active Directory - Enumeration (Bloodhound)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/AD%20Automatic%20Enumeration.md) to use `BloodHound` on target machine
## Queries 
#### Search for `USER`, and whether he has **ForceChangePassword**, **GenericAll** or **AllExtendedRights** over any account:
```cypher
MATCH p=((n:User {name:"<USER>@<Domain>.LOCAL"})-[r:ForceChangePassword|GenericAll|AllExtendedRights]->(m)) RETURN p
```
![[Pasted image 20251229135226.png]]
#### Revealing accounts that can read the **LAPS** password attribute. We can use the following cypher query to identify accounts with the **ReadLAPSPassword** access right:
```cypher
MATCH p=((n)-[r:ReadLAPSPassword]->(m)) RETURN p
```
![[Pasted image 20251229172919.png]]
#### Revealing accounts that can read the **ReadGMSAPassword** attribute.
```cypher
MATCH p=((n)-[r:ReadGMSAPassword]->(m)) RETURN p
```
![[Pasted image 20251229191009.png]]
#### Revealing accounts that has a specific permission **WriteDacl** attribute.
```cypher
MATCH p=((n)-[r:WriteDacl]->(m)) RETURN p
```
![[Pasted image 20251229221349.png]]
#### Revealing accounts that has a specific permission **WriteOwner/Owns** attribute.
![[Pasted image 20251230153603.png]]
## Targeted Kerberoasting
**WriteSPN**
![[targeted_kerberoast_bloodhound.png]]
via the **AddMembers** edge:
![[addmember_bloodhound.png]]
