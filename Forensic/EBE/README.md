# LACTF_misc-EBE

## Đề bài

```
I was trying to send a flag to my friend over UDP, one character at a time, but it got corrupted! I think someone else was messing around with me and sent extra bytes, though it seems like they actually abided by RFC 3514 for once. Can you get the flag?
```

## Khai thác

- follow UDP stream được một chuỗi ký tự

![image](https://hackmd.io/_uploads/BJ1EvFZA6.png)

in ra từng gói tin để phân tích với Scapy payload

```python
#!/usr/bin/python3.7
from scapy.all import *

filename = "./EBE.pcap"
print(f"[+] đang đọc file {filename}")
packets = rdpcap(filename)

for packet in packets:
    print(packet.show())
    input()
```

![image](https://hackmd.io/_uploads/ryOlSYWA6.png)

![image](https://hackmd.io/_uploads/H1WzSKWA6.png)

thấy các ký tự của flag xuất hiện khi trường flags trong lớp IP không phải evil

- vậy chúng ta dùng script sau

```python
#!/usr/bin/python3.7
from scapy.all import *

filename = "./EBE.pcap"
print(f"[+] đang đọc file {filename}")
packets = rdpcap(filename)

print("flag là: ", end="")
for packet in packets:
    if not "evil" in packet[IP].flags:
        print(packet[Raw].load.decode('utf-8'), end="")

```

![image](https://hackmd.io/_uploads/r13lIFWAp.png)

được flag là **lactf{3V1L_817_3xf1l7R4710N_4_7H3_W1N_51D43c8000034d0c}**
