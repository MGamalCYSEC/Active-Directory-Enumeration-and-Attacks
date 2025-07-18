# Exchange Related Group Membership
- The Exchange group Organization Management is another extremely powerful group (effectively the "Domain Admins" of Exchange) and can access the mailboxes of all domain users. It is not uncommon for sysadmins to be members of this group. This group also has full control of the OU called Microsoft Exchange Security Groups, which contains the group Exchange Windows Permissions.
- If we can compromise an Exchange server, this will often lead to Domain Admin privileges. Additionally, dumping credentials in memory from an Exchange server will produce 10s if not 100s of cleartext credentials or NTLM hashes.

# PrivExchange
The PrivExchange attack results from a flaw in the Exchange Server PushSubscription feature, which allows any domain user with a mailbox to force the Exchange server to authenticate to any host provided by the client over HTTP.

The PrivExchange attack exploits a flaw in the Exchange PushSubscription feature, allowing any domain user with a mailbox to trick Exchange into authenticating to an attacker-controlled host. Since Exchange runs as SYSTEM and often has excessive privileges (like WriteDacl on the domain), this authentication can be relayed to LDAP to gain DCSync rights and dump the NTDS database—resulting in full domain compromise. Even if LDAP relay fails, the attack can still be used for lateral movement within the domain.
