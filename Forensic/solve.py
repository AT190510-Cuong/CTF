#!/usr/bin/python3.7
from scapy.all import *

filename = "./EBE.pcap"
print(f"[+] đang đọc file {filename}")
packets = rdpcap(filename)

print("flag là: ", end="")
for packet in packets:
    if not "evil" in packet[IP].flags:
        print(packet[Raw].load.decode('utf-8'), end="")



