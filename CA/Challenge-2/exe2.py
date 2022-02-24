#s = 'The quick brown fox jumps over the lazy dog.'.encode('utf-8')
#print(s.hex())
from itertools import islice

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

"""
logger = open("log.txt","w")

f1 = open("y_clean.txt", "r")
f2 = open("x_clean.txt", "r")

y = f1.read()
x = f2.read()

xor_val = hex(int(x, 16) ^ int(y, 16))
xor_val = xor_val.replace("0x","")
xor_val = chunk(xor_val,2)
"""
testFile = open("log.txt", "r")
text = testFile.read()

#logger.write(str(list(xor_val)))
print(len(text))
"""
for symb in xor_val:
    try:
        logger.write(symb[0]+symb[1])
        sda = 1
        #logger.write(bytes.fromhex(symb[0]+symb[1]).decode('utf-8'))
    except:
        logger.write(symb[0]+symb[1])
        dsadsa = 1
        #print()
        #logger.write("err -> " + symb[0]+symb[1])
f1.close()
f2.close()
"""
testFile.close()
#logger.close()