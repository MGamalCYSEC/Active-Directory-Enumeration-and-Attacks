# Attacking Domain Trusts - Cross-Forest Trust Abuse 🖥️ - From Windows
Kerberos-based attacks—such as **Kerberoasting** and ASREPRoasting—can be executed across domain or forest trusts, depending on the trust direction.
If you're operating within a domain that has an inbound or **bidirectional** trust with another domain or forest, you may be able to leverage that trust to launch attacks in the trusted domain.
In some cases, privilege escalation within your current domain may not be possible. However, you might still be able to request a **Kerberos service ticket (TGS)** for an administrative account in the trusted domain. Once obtained, the ticket hash can be cracked offline, potentially giving you credentials for a user with Domain Admin or Enterprise Admin privileges across both domains—thus giving you a powerful foothold.
#### Consider You are a user of domain CORP.LOCAL and found a trust Bidirection to domain DOM.LOCAL like the following examole from BLOODHOUND
<img width="1867" height="388" alt="image" src="https://github.com/user-attachments/assets/e00a4627-2f77-497f-882d-e5307d8f45bd" />

### Enumerating accounts in a target domain that have SPNs associated with them Using PowerView:
```powershell
Get-DomainUser -SPN -Domain <TargetDomain> | select SamAccountName
```
<img width="1504" height="250" alt="image" src="https://github.com/user-attachments/assets/2b1e92aa-f4e3-4616-8dfb-30e06c4dcead" />

### Enumerating the mssqlsvc Account
<img width="1657" height="214" alt="image" src="https://github.com/user-attachments/assets/245a75ee-1096-45f8-ac13-d30a16462bc1" />

### Perform a Kerberoasting attack across the trust using Rubeus
```powershell
.\Rubeus.exe kerberoast /domain:DOM.LOCAL /user:mssqlsvc /nowrap
```
<img width="1632" height="370" alt="image" src="https://github.com/user-attachments/assets/64e77fda-8e07-4293-9f20-9edf86448206" />
Copy the Hash on Kali-Machine

### Crack the hashes
```shell
sudo hashcat -m 13100 hash.hash /usr/share/wordlists/rockyou.txt
```

---

## **Admin Password Reuse & Cross-Forest Group Membership**

#### 🔁 **Password Reuse Between Trusted Domains**

* In environments with **bidirectional forest trusts**, both forests might be managed by the same company and admins.
* If you compromise **Domain A** and obtain the **NT hash or cleartext password** of:

  * The **built-in Administrator**, or
  * A user in **Domain Admins** or **Enterprise Admins**,
    …check if **Domain B** has a similarly named account with **the same password**.

✅ **Why?** Because admins sometimes reuse passwords across domains.

**Example:**

* Domain A has `adm_bob.smith` in Domain Admins.
* Domain B has `bsmith_admin`.
* If both accounts share the same password, taking over Domain A could give **full admin access to Domain B**.


#### 👥 **Cross-Forest Group Membership**

* In **bidirectional forest trusts**, admins from one domain can be members of groups in another.
* **Domain Local Groups** (in Domain B) can include **users from Domain A**.
* If a **Domain A admin** is added to the **Administrators group in Domain B**, and you compromise that admin in Domain A—you now have **admin access in Domain B**.


#### 🔍 **Real Example:**

* Use PowerView’s `Get-DomainForeignGroupMember` to find **foreign users** in groups.

```powershell
Get-DomainForeignGroupMember -Domain DOM.LOCAL
Convert-SidToName <SID>
```
<img width="2023" height="556" alt="image" src="https://github.com/user-attachments/assets/399423dc-a805-447a-baea-20624d48f7cc" />
Output shows that the built-in Administrators group in DOM.LOCAL has the built-in Administrator account for the CORP.LOCAL domain as a member. We can verify this access using the Enter-PSSession cmdlet to connect over WinRM.

* Accessing DC03 Using Enter-PSSession

```powershell
Enter-PSSession -ComputerName DC03.DOM.LOCAL -Credential CORP\administrator
```
---

## SID History Abuse - Cross Forest

Here’s a simplified and organized version of the explanation about **SID History abuse across forest trusts**:

---

### 🆔 **SID History Abuse Across Forest Trusts**

#### 🧠 What is SID History?

* When a user is **migrated from one domain or forest to another**, their old **SID (Security Identifier)** can be stored in the `SIDHistory` attribute of the new account.
* This allows the user to **retain access** to resources that rely on their **old permissions**.


#### 🚨 **Abuse Scenario (Cross-Forest)**

* In a **forest trust** setup, if **SID filtering** is **not enabled**, attackers can **manually insert SIDs** into the `SIDHistory` attribute.
* This means you can **add the SID of an admin account from Forest A** into the `SIDHistory` of a user in Forest B.
* When the user authenticates across the trust, their token includes that **admin SID**, granting them **privileges in the other forest**.

#### 🔍 **Example Scenario:**

* A user `jjones` is migrated from `DOM.LOCAL` (Forest A) to `CORP.LOCAL` (Forest B).
* If:

  * `SID filtering` is **disabled**, and
  * `jjones` had **admin rights** (or useful access) in Forest A,
* Then:

  * The `jjones` account in `CORP.LOCAL` can still **access and control** resources in `DOM.LOCAL` using their **old SID**.

#### 🔒 **Mitigation:**

* **Enable SID Filtering** on forest trusts to block foreign SIDs in access tokens.
* This helps prevent privilege escalation via `SIDHistory`.
