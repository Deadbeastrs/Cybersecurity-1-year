How to run the S-AES implementation:

To encrypt the ./encrypt "key1" "key2" , can be used, if key2 is not provided, it will encrypt with normal AES

To decrypt the ./decrypt "key1" "key2" , can be used, if key2 is not provided, it will decrypt with normal AES

Command example for encrypt and decrypt: 

echo "ThisIsTheText" | ./encrypt "firstkey" "secondkey" |  ./decrypt "firstkey" "secondkey"

To run the speed program:

./speed

This program will test the encryption of 

d41c0a3ec403c150ebfbe644df980c51
---
93e2dba057e11af0bc1afcb46382f0e5
---
826e025bd58f18ab6995e41f0a1714fa
---
76942f3ca31b3797ca8ed388c099c772
---
90526f8633495811f9c78b99395e4ceb
---
d87b8694eb32de8512f5551c2bab19f7   |   f7d87b8694eb32de8512f5551c2bab19
---
9aafee65719d30e0636865fc48c37c0b
---
f4bfc5378522f5d7e64a902bae89ec20
---
d37172d356538704b019172f1e90fb0f
---
a87e04a1fe2d83a54e34948a50a46f85
---
d7d693f229fb105767cf84dd376beb58
Round->5



---
d41c0a3ec403c150ebfbe644df980c51
---
93e2dba057e11af0bc1afcb46382f0e5
---
826e025bd58f18ab6995e41f0a1714fa
---
76942f3ca31b3797ca8ed388c099c772
---
90526f8633495811f9c78b99395e4ceb
---

---
9aafee65719d30e0636865fc48c37c0b
---
f4bfc5378522f5d7e64a902bae89ec20
---
d37172d356538704b019172f1e90fb0f
---
a87e04a1fe2d83a54e34948a50a46f85
---
d7d693f229fb105767cf84dd376beb58