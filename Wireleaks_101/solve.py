from scapy.all import *

pcap = rdpcap('chall.pcap')

flag = ''

for pkt in pcap:
    if pkt.haslayer(TCP) and pkt.getlayer(TCP).dport == 443:
        if 'U' in str(pkt['TCP'].flags):
            flag += '1'
        else:
            flag += '0'

while(len(flag)>8):
    print(chr(int(flag[0:8], 2)), end='')
    flag = flag[8:]
