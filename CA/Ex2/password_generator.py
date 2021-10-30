import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def main(password,filename):

    file = open(filename,"wb")
    salt = b'\x00'
    kdf = PBKDF2HMAC( hashes.SHA1(), 16, salt, 1000, default_backend() )
    key = kdf.derive( bytes( password, 'UTF-8') )

    print("KEY:" + str(key)) 
    file.write(key)
    file.close()
    return 1



if __name__ == "__main__":
    
    try:
        main(sys.argv[1], sys.argv[2])
    except:
        print("Argument 1 is the password, Argument 2 is the file")