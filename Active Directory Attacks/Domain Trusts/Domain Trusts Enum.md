# Introduction
- Large organizations often create **domain trust relationships** to simplify access when acquiring other companies or integrating with external partners like Managed Service Providers (MSPs) or remote business units. This avoids the need to migrate users and resources, making integration faster. However, if not properly secured, these trusts can become a **security risk**—a vulnerable subdomain or trusted partner can provide attackers with a path into the main domain. Understanding and assessing these trust relationships is crucial, as they can be **abused through built-in mechanisms** during security testing.
# Overview
- A [trust](https://learn.microsoft.com/en-us/archive/technet-wiki/50969.active-directory-forest-trust-attention-points) is used to establish forest-forest or domain-domain (intra-domain) authentication, which allows users to access resources in (or perform administrative tasks) another domain, outside of the main domain where their account resides. 
- A trust creates a link between the authentication systems of two domains and may allow either one-way or two-way (bidirectional) communication.
## Types of trusts:
* **Parent-child**: Domains in the same forest with two-way trust—users can access resources between parent and child domains media.domain.local could authenticate into the parent domain domain.local, and vice-versa.
* **Cross-link**: Trust between child domains to make authentication faster.
* **External**: One-way or two-way trust between separate forests, not transitive—uses SID filtering to control access.
* **Tree-root**: Automatic two-way trust between the main forest root and a new tree root domain.
* **Forest**: Trust between two different forest roots—fully transitive.
* **[ESAE](https://learn.microsoft.com/en-us/security/privileged-access-workstations/esae-retirement)**: A separate, secure forest (also called a bastion forest) used to manage Active Directory securely.
### **NOTES**: 
- A **transitive** trust means that trust is extended to objects that the child domain trusts, Example: if Domain A has a trust with Domain B, and Domain B has a transitive trust with Domain C, then Domain A will automatically trust Domain C.
- **Non-transitive** trust, the child domain itself is the only one trusted.
- **One-way trust** Users in a trusted domain can access resources in a trusting domain, not vice-versa.
- **Bidirectional trust** Users from both trusting domains can access resources in the other domain.
# Enumerating Trust Relationships
## Using Get-ADTrust
```powershell
Import-Module activedirectory
Get-ADTrust -Filter *
```
Ouput Example:
<img width="1485" height="831" alt="image" src="https://github.com/user-attachments/assets/096e98be-0717-4249-a2c2-ae6dd9b8732b" />

The output indicates that our current domain, **Corp.com**, has two domain trusts. The first is with **LOGISTICS.Corp.com**, identified as a child domain due to the *IntraForest* (the trust is internal to the forest ) property—confirming we are in the forest root domain. The second trust is with **Dom.com**, and the *ForestTransitive* property being *True* suggests it's either a forest or external trust. Both trusts are **bidirectional**, allowing users to authenticate in both directions. This is a key detail during assessments—if cross-trust authentication isn't possible, we won’t be able to enumerate or launch attacks across the trusted domain.
## Using PowerView

```powershell
Get-DomainTrust
```
perform a domain trust mapping and provide information such as the type of trust (parent/child, external, forest) and the direction of the trust (one-way or bidirectional).
```powershell
Get-DomainTrustMapping
```
## Checking Users in the Child Domain using Get-DomainUser
```powershell
Get-DomainUser -Domain LOGISTICS.CORP.LOCAL | select SamAccountName
```
## Using netdom 
The netdom query sub-command of the netdom command-line tool in Windows can retrieve information about the domain, including a list of workstations, servers, and domain trusts.
### To query domain trust
```powershell
netdom query /domain:CORP.local trust
```
### To query domain controllers
```powershell
netdom query /domain:CORP.local dc
```
### To query workstations and servers
```powershell
netdom query /domain:CORP.local workstation
```
## Visualizing Trust Relationships in BloodHound
<img width="1912" height="583" alt="image" src="https://github.com/user-attachments/assets/b2f6b9f0-48b5-4f0a-911f-0b26ce5cd6c5" />
