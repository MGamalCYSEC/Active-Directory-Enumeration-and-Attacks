#### Using net to Query Group Membership
```shell
net rpc group members '<TARGET-GROUP>' -U domain.com/<USER>%<PASSWORD> -S <TARGET_IP>
```
#### Using net to Add USER to TARGET-GROUP to Query Group Membership
```shell
net rpc group addmem '<TARGET-GROUP>' <USER> -U domain.com/<USER>%<PASSWORD> -S <TARGET_IP>
```

#### Using LDAP for Adding a User to a Group

```shell
wget https://github.com/juliourena/ActiveDirectoryScripts/raw/refs/heads/main/Python/addusertogroup.py
python3 addusertogroup.py -d domain.local -g "<TARGET-GROUP>" -a <USER> -u <USER> -p <PASSWORD>
```
#### Query Group Membership
```shell
net rpc group members '<TARGET-GROUP>' -U domain.com/<USER>%<PASSWORD> -S <TARGET_IP>
```
