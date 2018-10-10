#!/usr/bin/python
import ifcfg
from scapy.all import srp, Ether, ARP

print('Content-Type: text/html\n')

ifcard='wlp4s0'
macs=[
   '0c:72:2c:4e:26:f8',
   '54:ee:75:86:6a:8b',
   'e4:a4:71:62:d5:54' 
]
subnet='192.168.1.1/24'
map2ip={}

for name, interface in ifcfg.interfaces().items():
    if interface['device'] == ifcard:
        ip=interface['inet'].split('.')
        subnet='%s.%s.%s.%s/24'%(ip[0],ip[1],ip[2],1)
       
ans,unans = srp(Ether(dst='FF:FF:FF:FF:FF:FF')/ARP(pdst=subnet), timeout=2)
for send, rcv in ans:
   map2ip[rcv.src]=rcv.psrc
print('<html>hejie</html>')
print(map2ip)
