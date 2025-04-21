# Active Directory Enumeration (Non-Joined Domain)

## 1. Nmap Port Scan: Identifying Key Services

When scanning your target Domain Controller, focus on these ports to detect services related to AD:
### Core Authentication & Directory Services

|Port|Protocol|Service|Description|
|---|---|---|---|
|**53**|TCP/UDP|DNS|Domain Name System resolution for AD domains.|
|**88**|TCP/UDP|Kerberos|Authentication protocol for AD (supports both TCP and UDP).|
|**389**|TCP/UDP|LDAP|Unencrypted directory queries via Lightweight Directory Access Protocol.|
|**636**|TCP|LDAPS|Secure LDAP over SSL/TLS (encrypted directory queries).|
|**3268**|TCP|Global Catalog|LDAP for forest-wide directory data searches.|
|**3269**|TCP|Global Catalog|Secure Global Catalog over SSL/TLS.|

### File Sharing & Group Policy

|Port|Protocol|Service|Description|
|---|---|---|---|
|**135**|TCP|RPC Endpoint|RPC endpoint mapper for AD services.|
|**445**|TCP|SMB|File sharing, Group Policy, and AD replication via Server Message Block.|

### Replication & Management

|Port|Protocol|Service|Description|
|---|---|---|---|
|**5722**|TCP|DFSR|AD database replication using Distributed File System Replication.|
|**9389**|TCP|AD Web Services|SOAP-based management used by PowerShell and AD admin tools.|

### Legacy & Optional Services

|Port|Protocol|Service|Description|
|---|---|---|---|
|**137-139**|TCP/UDP|NetBIOS|Legacy NetBIOS for name resolution and file sharing (mostly replaced by SMB).|
|**123**|UDP|NTP|Network Time Protocol for time synchronization (important for Kerberos).|
|**464**|TCP/UDP|kpasswd|Kerberos password change protocol.|

---

## 2. Passive Network Analysis: Responder

**Responder** is used to passively listen to LLMNR, NBT-NS, and mDNS traffic.
- **Command**:
    ```bash
    sudo responder -I <interface> -A
    ```
- **Purpose**: Analyze network requests to identify additional domain hosts without actively poisoning traffic.

---

## 3. User Enumeration with [Kerbrute](https://github.com/ropnop/kerbrute/releases)

**Kerbrute** helps identify valid AD usernames and exposes misconfigurations.

- **Command**:
``` shell
kerbrute userenum -d INLANEFREIGHT.LOCAL --dc 172.16.5.5 /usr/share/wordlists/rockyou.txt -o valid_ad_users
```
- **Note**: Look for outputs that indicate “No Pre-Authentication Required.”
    - **AS-REP Hash**: If found (e.g., `$krb5asrep$23$...`), this hash can be cracked offline to recover the plaintext password.
    - that's mean the user has **Kerberos pre-authentication disabled** (`DONT_REQ_PREAUTH` flag set in Active Directory). This misconfiguration allows attackers to request a Kerberos Ticket Granting Ticket (TGT) for the user **without knowing their password**.
---

## 4. SMB NULL Sessions & Enumeration

### What is a NULL Session?
- An unauthenticated SMB connection that provides limited access to resources like domain shares and RPC services.
- Often enabled for legacy compatibility, exposing information about the domain.
### Using CrackMapExec (CME)

- **Purpose**: Enumerate domain users and check account states.
- **Command**:
``` shell
crackmapexec smb <IP> --users
```
- **Output**: Displays user accounts along with `badpwdcount` and `baddpwdtime` to assess the risk of lockouts.
### Using rpcclient for Enumeration
- **Establish a NULL Session**:
``` shell
rpcclient -U "" -N <target_IP>
```
- **Common rpcclient Commands**:
``` shell
# Query domain info
querydominfo
# Retrieve domain password policies
getdompwinfo
# Enumerate domain users
enumdomusers
# Enumerate domain groups
enumdomgroups
```
**Example Output Analysis**
- **Domain Info**:
```plaintext
Domain:         INLANEFREIGHT
Total Users:    3650
Total Groups:   0
Total Aliases:  37
Server Role:    ROLE_DOMAIN_PDC
```
- _Key Details_: The number of users, groups, aliases, and the server role (Primary Domain Controller in this case).
- **Password Policy**:
```plaintext
min_password_length: 8
password_properties: 0x00000001
DOMAIN_PASSWORD_COMPLEX
```
- _Weakness_: A minimum password length of 8 may be insufficient, depending on the password complexity enforced.

---

## 5. Enumeration with enum4linux & enum4linux-ng
### enum4linux (Classic)
- **Command**:
``` shell
enum4linux -P 172.16.5.5
```
### enum4linux-ng (Enhanced Version)
- **Command**:
``` shell
enum4linux-ng -P 172.16.5.5 -oA ilfreight
```
- **Advantages**: Outputs data in YAML/JSON for further processing and adds more enumeration features.

---

## 6. Windows-Based NULL Session Enumeration

### Establishing a NULL Session from Windows:
- **Successful NULL Session**:
```cmd
net use \\DC01\ipc$ "" /u:""
```
- _Message_: “The command completed successfully.”
### Handling Common Errors:
- **Account Disabled**:
```cmd
net use \\DC01\ipc$ "" /u:guest
```
  - _Error_: System error 1331 – “This user can't sign in because this account is currently disabled.”
- **Incorrect Password**:
```cmd
net use \\DC01\ipc$ "password" /u:guest
```
- _Error_: System error 1326 – “The user name or password is incorrect.”
- **Account Locked Out**:
```cmd
net use \\DC01\ipc$ "password" /u:guest
```
- _Error_: System error 1909 – “The referenced account is currently locked out and may not be logged on to.”

---
## 7. LDAP Anonymous Bind & Policy Enumeration
### LDAP Anonymous Binds
- **Overview**: In legacy configurations, anonymous LDAP binds can allow unauthenticated attackers to retrieve detailed domain data (users, groups, computers, and password policies).
    - _Note_: Modern Windows Server versions restrict LDAP binds to authenticated users.
### Enumerating via LDAP Tools
- **Using ldapsearch**:
- Basic enumeration on null session
``` shell
ldapsearch -x -H ldap://<LDAP_SERVER_IP> -D '' -w '' -b "DC=hutch,DC=LOCAL"
```
- password policy
```bash
ldapsearch -H <LDAP_SERVER_IP> -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "*" | grep -m 1 -B 10 pwdHistoryLength
```
- **Expected Output**: Domain password policy details (e.g., minimum password length, lockout threshold, and complexity requirements).

- **List Users**:
    ```bash
    ldapsearch -x -H ldap://<LDAP_SERVER_IP> -D '' -w '' -b "<BASE_DN>" "(objectClass=user)"
    ```
- **List Groups**:
    ```bash
    ldapsearch -x -H ldap://<LDAP_SERVER_IP> -D '' -w '' -b "<BASE_DN>" "(objectClass=group)"
    ```
- **List Computers**:
    ```bash
    ldapsearch -x -H ldap://<LDAP_SERVER_IP> -D '' -w '' -b "<BASE_DN>" "(objectClass=computer)"
    ```
- Replace `<LDAP_SERVER_IP>` with the LDAP server's IP or hostname.
- Replace `<BASE_DN>` with the Base DN, e.g., `DC=example,DC=com`.
    
