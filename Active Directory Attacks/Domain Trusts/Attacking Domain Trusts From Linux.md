To perform this attack from a **Linux attack host**, we  need to gather the following:

* The **KRBTGT hash** of the **child domain**
* The **Security Identifier (SID)** of the **child domain**
* The **Fully Qualified Domain Name (FQDN)** of the **child domain**
* The **SID of the Enterprise Admins group** in the **root domain**
* The **name of a target user** within the child domain (*note: the account does not need to actually exist*)

Once all of this data is collected, the attack can be carried out using the appropriate tools from the Linux environment (e.g., **Impacket**).
