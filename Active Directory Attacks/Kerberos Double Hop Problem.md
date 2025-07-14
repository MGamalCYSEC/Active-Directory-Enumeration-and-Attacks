# Kerberos "Double Hop" Problem
## Introduction
The **Double Hop problem** happens when a user or service tries to access a **second resource** (like a database) **through another server** (like a web server) using **Kerberos authentication**.

#### Why It Happens:

* **Kerberos tickets** are tied to a specific resource (the **first "hop"**) and **can't be reused** for other resources.
* So when the first server tries to **forward the user's credentials** to the second server (the **second "hop"**), **Kerberos blocks it by default**.

#### Why It's Important:

* This behavior **protects against attackers** using a single ticket to move across systems (lateral movement).
* But it also **breaks workflows** that need to access multiple systems on behalf of a user.
---

The **"Double Hop" problem** happens when you use tools like _WinRM/PowerShell_ to connect to a remote machine (first hop), but then can’t access *another* resource (e.g., a file share or database) from there (second hop). This occurs because WinRM uses **Kerberos tickets** (like a single-use key for one door) instead of storing your password or NTLM hash (a reusable "master key"). Without that stored "master key," the remote machine can’t automatically authenticate you to the next resource—even if you have permission.  

For example:  
- If you hack a server using **WinRM**, you’ll hit a wall trying to access other servers from there (no "master key" saved).  
- But with tools like **PSExec** (which uses SMB/NTLM), your NTLM hash *is* stored in memory, letting you pivot to other systems easily.  

**Why it matters**:  
- **Annoyance**: Admins must configure special permissions ("delegation") for multi-hop access. Attackers hate this because it blocks lateral movement unless they steal a "master key" (NTLM hash) instead.  
In the simplest terms, in this situation, when we try to issue a multi-server command, our credentials will not be sent from the first machine to the second.

---
