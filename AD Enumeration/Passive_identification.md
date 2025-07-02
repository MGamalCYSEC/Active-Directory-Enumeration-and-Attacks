# Passive identification of any hosts in the network
## Identifying Hosts
### Wireshark
```shell
sudo -E wireshark
```
Take some time to listen to the network and see what's going on "put our ear to the wire".
We notice some ARP requests and replies, MDNS, and other basic layer two packets (since we are on a switched network, we are limited to the current broadcast domain) some of which we can see below.
### Tcpdump 
```shell
sudo tcpdump -i tun0 -nn -v
sudo tcpdump -i tun0 arp
```
Our first look at network traffic pointed us to a couple of hosts via MDNS and ARP.
### Responder
```shell
sudo responder -I tun0 -A
```
