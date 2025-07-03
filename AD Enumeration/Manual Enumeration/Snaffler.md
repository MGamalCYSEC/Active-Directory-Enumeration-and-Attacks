# Using Snaffler - enumerating Shares
To execute Snaffler, we can use the command below:
``` powershell
.\Snaffler.exe -s -d Domain.local -o snaffler.log -v data
```
#### Command Breakdown:

- **`-s`**: Prints results to the console for real-time viewing.
- **`-d`**: Specifies the domain to search within (e.g., `inlanefreight.local`).
- **`-o`**: Writes the results to a logfile (e.g., `snaffler.log`).
- **`-v`**: Sets verbosity level.
- `data` is typically the best setting for initial runs as it limits console output, making it easier to analyze results in real-time.
We may find passwords, SSH keys, configuration files, or other data that can be used to further our access. Snaffler color codes the output for us and provides us with a rundown of the file types found in the shares.
