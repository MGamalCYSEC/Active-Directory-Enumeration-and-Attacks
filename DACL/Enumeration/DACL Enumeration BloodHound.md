Back to [Active Directory - Enumeration (Bloodhound)](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/AD%20Automatic%20Enumeration.md) to use `BloodHound` on target machine
## Queries 
#### Search for `USER`, and whether he has **ForceChangePassword**, **GenericAll** or **AllExtendedRights** over any account:
```cypher
MATCH p=((n:User {name:"<USER>@<Domain>.LOCAL"})-[r:ForceChangePassword|GenericAll|AllExtendedRights]->(m)) RETURN p
```
<img width="1413" height="552" alt="Pasted image 20251229135226" src="https://github.com/user-attachments/assets/20365cea-acad-4895-b363-0e09bbbeb183" />

#### Revealing accounts that can read the **LAPS** password attribute. We can use the following cypher query to identify accounts with the **ReadLAPSPassword** access right:
```cypher
MATCH p=((n)-[r:ReadLAPSPassword]->(m)) RETURN p
```
<img width="1381" height="305" alt="Pasted image 20251229172919" src="https://github.com/user-attachments/assets/1c8c1bbc-4502-47e9-9afd-69e6221277ca" />

#### Revealing accounts that can read the **ReadGMSAPassword** attribute.
```cypher
MATCH p=((n)-[r:ReadGMSAPassword]->(m)) RETURN p
```
<img width="1021" height="584" alt="Pasted image 20251229191009" src="https://github.com/user-attachments/assets/1ad480a0-739d-43c4-ad77-f9f9ccdf6cb6" />

#### Revealing accounts that has a specific permission **WriteDacl** attribute.
```cypher
MATCH p=((n)-[r:WriteDacl]->(m)) RETURN p
```
<img width="859" height="235" alt="Pasted image 20251229221349" src="https://github.com/user-attachments/assets/ce16999a-3232-4b27-9e84-68513f511d21" />

#### Revealing accounts that has a specific permission **WriteOwner/Owns** attribute.
<img width="995" height="229" alt="Pasted image 20251230153603" src="https://github.com/user-attachments/assets/5ffc6ebf-040f-4fcc-bc6b-59684d99b3ff" />

## Targeted Kerberoasting
**WriteSPN**
<img width="671" height="227" alt="targeted_kerberoast_bloodhound" src="https://github.com/user-attachments/assets/1d80c14d-243c-477c-9de7-cb2d1c51e303" />

via the **AddMembers** edge:
<img width="680" height="224" alt="addmember_bloodhound" src="https://github.com/user-attachments/assets/ae6d2d59-7dbd-4a85-bbff-472ecd7fefaa" />
