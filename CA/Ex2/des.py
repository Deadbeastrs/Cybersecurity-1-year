import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class des:
    def encrypt(self,KeyFileName,PlainTextFile,OutputFile,CypherMode):

        file1 = open( KeyFileName, "rb" )
        key = file1.read()
        iv = os.urandom( algorithms.TripleDES.block_size // 8)
        if CypherMode == "CBC":
            cipher = Cipher( algorithms.TripleDES( key ), modes.CBC( iv ), default_backend())
        elif CypherMode == "OFB":
            cipher = Cipher( algorithms.TripleDES( key ), modes.OFB( iv ), default_backend())
        elif CypherMode == "CFB":
            cipher = Cipher( algorithms.TripleDES( key ), modes.CFB( iv ), default_backend())
        elif CypherMode == "CTR":
            cipher = Cipher( algorithms.TripleDES( key ), modes.CTR( iv ), default_backend())
        elif CypherMode == "ECB":
            cipher = Cipher( algorithms.TripleDES( key ), modes.ECB(), default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7( algorithms.TripleDES.block_size ).padder()

        file2 = open(PlainTextFile,"rb")
        file3 = open(OutputFile,"wb")
        file3.write(iv)

        offset = 0
        chunkSize = algorithms.TripleDES.block_size

        while True:
            file2.seek(offset,0)
            plaintext = file2.read(chunkSize)
            if not plaintext:

                ciphertext = encryptor.update( padder.finalize() )
                file3.write(ciphertext)
                print(ciphertext)

                break
        
            else:
                ciphertext = encryptor.update( padder.update( plaintext ))
                file3.write(ciphertext)
                print(ciphertext)

            offset = offset + chunkSize

        file1.close()
        file2.close()
        file3.close()

        return 1

    #-------------------------------------

    def decrypt(self,KeyFileName,PlainTextFile,OutputFile,CypherMode):

        file1 = open( KeyFileName, "rb" )
        key = file1.read()
        file2 = open(PlainTextFile,"rb")
        file3 = open(OutputFile,"wb")
        file2.seek(0,0)
        iv = file2.read(algorithms.TripleDES.block_size // 8)
        if CypherMode == "CBC":
            cipher = Cipher( algorithms.TripleDES( key ), modes.CBC( iv ), default_backend())
        elif CypherMode == "OFB":
            cipher = Cipher( algorithms.TripleDES( key ), modes.OFB( iv ), default_backend())
        elif CypherMode == "CFB":
            cipher = Cipher( algorithms.TripleDES( key ), modes.CFB( iv ), default_backend())
        elif CypherMode == "CTR":
            cipher = Cipher( algorithms.TripleDES( key ), modes.CTR( iv ), default_backend())
        elif CypherMode == "ECB":
            cipher = Cipher( algorithms.TripleDES( key ), modes.ECB(), default_backend())
        encryptor = cipher.decryptor()
        unpadder = padding.PKCS7( algorithms.TripleDES.block_size ).unpadder()

        chunkSize = algorithms.TripleDES.block_size
        offset = algorithms.TripleDES.block_size // 8
        while True:
            file2.seek(offset,0)
            plaintext = file2.read(algorithms.TripleDES.block_size)

            if not plaintext:
                ciphertext = unpadder.finalize()
                
                file3.write(ciphertext)
                break
        
            else:
                ciphertext = encryptor.update(plaintext)

                file3.write(unpadder.update(ciphertext))
                file3.flush()

            offset = offset + chunkSize

        file1.close()
        file2.close()
        file3.close()

        return 1

if __name__ == "__main__":
    try:
        des = des()
        if sys.argv[1] == "enc":
            des.encrypt(sys.argv[2], sys.argv[3],sys.argv[4])
        if sys.argv[1] == "dec":
            des.decrypt(sys.argv[2], sys.argv[3],sys.argv[4])
    except :
        print("Argument 1 is encrypt or decrypt (enc,dec), Argument 2 is passwordFile, Argument 3 is the inputFile, Argument 4 is the outputFile")
    