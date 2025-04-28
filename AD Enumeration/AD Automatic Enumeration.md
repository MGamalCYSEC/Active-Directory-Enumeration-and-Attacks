In order to use BloodHound, we need to start the [_Neo4j_](https://neo4j.com/) service, which is installed by default.# [SharpHound](https://support.bloodhoundenterprise.io/hc/en-us/articles/17481151861019-SharpHound-Community-Edition)
Before you Download Sharphound version is so important as newest releases above version v1.1.0 compatible only with bloodhound 5
So for bloodhound on kali dist we use [SharpHound v1.1.0](https://github.com/SpecterOps/SharpHound/releases/tag/v1.1.0) 

``` powershell
powershell -ep bypass
Import-Module .\Sharphound.ps1
```
##### Running SharpHound to collect domain data
``` powershell
Invoke-BloodHound -CollectionMethod All -OutputDirectory C:\temp\ -OutputPrefix "corp audit"
```
#### CollectionMethods
![Pasted image](https://github.com/MGamalCYSEC/Active-Directory-Enumeration-and-Attacks/blob/main/AD%20Enumeration/Pasted%20image%2020241225121647.png)
##### The Session Loop Collection Method
``` powershell
SharpHound.exe --CollectionMethods Session --Loop
```
- As a zip file
``` powershell
.\SharpHound.exe -c All --zipfilename ILFREIGHT
```
## Analysing Data using **BloodHound**
`On kali linux`
In order to use BloodHound, we need to start the [_Neo4j_](https://neo4j.com/) service, which is installed by default.
Neo4j is essentially an open source [graph database](https://en.wikipedia.org/wiki/Graph_database) (NoSQL) that creates nodes, edges, and properties instead of simple rows and columns.
For first run **user**:neo4j and **pwd**:neo4j
if we need to uninstall 
``` shell
sudo apt remove --purge neo4j -y
```

``` shell
sudo apt-get install neo4j
sudo neo4j start
```
##### Starting BloodHound in Kali Linux
``` shell
bloodhound
```
---
on note neo4j:**123**

---
#### Releases Download [V2.5.9](https://github.com/SpecterOps/SharpHound/releases) For sharp hound works on the following
Installing and using Bloodhound 5 with docker on kali or windows 
Repo. [Link](https://github.com/SpecterOps/BloodHound) 
On kali Linux 
#### Before start [Installing Docker](https://www.kali.org/docs/containers/installing-docker-on-kali/)
1. **Uninstall Old Docker Compose (if necessary)**:
``` shell
sudo apt remove docker-compose
```
2. **Install the Docker Compose Plugin**: Download the plugin using the following commands:
``` bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.35.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
3. **Make Docker Compose Executable**:
``` shell
sudo chmod +x /usr/local/bin/docker-compose
```
4. `curl -L https://ghst.ly/getbhce -o docker-compose.yml`
5. Start BloodHound:
``` shell
sudo docker-compose pull
sudo docker-compose up
```
