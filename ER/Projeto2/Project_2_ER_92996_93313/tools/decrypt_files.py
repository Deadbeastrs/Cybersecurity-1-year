from Crypto.Cipher import AES
import imghdr
import base64
import os
import sys


if len(sys.argv) != 3:
	print("python3 decrypt_files <key> <file>")
	exit(1)

key_file = open(sys.argv[1],'rb')

key = key_file.read()

for i in range(0,256):
	new = bytes([i])
	iv1 = b'\x43\x72\x59\x70\x54\x30\x5f\x31\x53\x5f\x62\x34\x63\x4b\x00' + new
	
	f_raw = open(sys.argv[2],"rb")
	cipherimage = f_raw.read()
	
	mode = AES.MODE_OFB

	decryptor = AES.new(key, mode, iv=iv1)
	
	image = decryptor.decrypt(cipherimage)
	
	f = open("{}.decrypted".format(sys.argv[2]), "wb")
	f.write(image)
	f.close()
	
	if imghdr.what("{}.decrypted".format(sys.argv[2])) != None:
		break
