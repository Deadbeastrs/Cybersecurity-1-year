import sys
from mtwister import mersenne_rng
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def genConfusionPattern(confusion_string):
    seed = ""
    for char in confusion_string:
        seed = int(str(seed) + str(ord(char))) % 2147483647
    rng = mersenne_rng(int(seed))
    confusionPattern = []
    for i in range(0,len(confusion_string)):
        confusionPattern.append(rng.get_random_number() % 256)
    return confusionPattern


def main():

    if len(sys.argv) != 4:
        print("Usage: python3 randgen.py password confusion_string iter")
        return 0

    password = sys.argv[1]
    confusion_string = sys.argv[2]
    iter_count = sys.argv[3]

    salt = str.encode(confusion_string)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA1(),length=16,salt=salt,iterations=int(iter_count))

    key = kdf.derive(str.encode(password))

    seed = ""

    for byte in key:
        seed = int(str(seed) + str(byte)) % 2147483647

    confusionPattern = genConfusionPattern(confusion_string)

    buffer = [0] * len(confusion_string)

    temp = 0

    mainRng = None

    for i in range(0,int(iter_count)):
        mainRng = mersenne_rng(int(seed))
        while(1):
            buffer[temp] = mainRng.get_random_number() % 256
            
            if buffer == confusionPattern:
                seed = 0
                for k in range(0,16):
                    seed = int(str(seed) + str(mainRng.get_random_number() % 256)) % 2147483647
                break
            
            temp+=1
            if temp == len(confusion_string) :
                temp = 0
        

    for i in range(0,16):
        randNum = mainRng.get_random_number()
        bytes_val = randNum.to_bytes(4, 'little')
        sys.stdout.buffer.write(bytes_val)
           
main()