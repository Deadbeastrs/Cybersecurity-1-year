import sys
import gmpy2
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def nextSafePrime(num):
    while 1:
        prime = gmpy2.next_prime(num)
        safeprime = prime * 2 + 1
        if(gmpy2.is_prime(safeprime)):
            break
        num = prime
        
    return prime

def generate_key(seed):

    seed = seed | (1<<511)

    seed = seed | (1<<510)

    p = nextSafePrime(seed)

    seed2 = p

    seed2 = seed2 | (1<<511)

    seed2 = seed2 | (1<<510)

    q = nextSafePrime(seed2)

    z = (p-1) * (q-1)
    e1 = 2 ** 16 + 1
    d = pow(e1, -1, z)
    n = int(p*q)
    dmq1 = rsa.rsa_crt_dmq1(d, q)
    dmp1 = rsa.rsa_crt_dmp1(d, p)
    iqmp = rsa.rsa_crt_iqmp(p, q)
    
    publicNumbers = rsa.RSAPublicNumbers(e1, n)
    privateNumbers = rsa.RSAPrivateNumbers(int(p), int(q), int(d), int(dmp1), int(dmq1), int(iqmp), publicNumbers)

    privateKey = privateNumbers.private_key()
    publicKey = publicNumbers.public_key()

    privateKeyPem = privateKey.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
    )

    publicKeyPem = publicKey.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open('private.pem', 'wb') as f:
        f.write(privateKeyPem)

    with open('public.pem', 'wb') as f:
        f.write(publicKeyPem)
    

data = sys.stdin.buffer.read(64)

padding = 64 - len(data) 

temp = list(data)

for i in range(0,padding):
    temp.append(0)

data = bytes(temp)

dataInt = int.from_bytes(data, byteorder='big', signed=False)
generate_key(dataInt)

