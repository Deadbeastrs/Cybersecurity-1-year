import sys

def gcdExtended(a, b): 
    if a == 0 :  
        return b, 0, 1
    gcd, x1, y1 = gcdExtended(b%a, a) 
    x = y1 - (b//a) * x1 
    y = x1 
    
    return gcd, x, y

def find_a_b(e1,e2):
    a = modinv(e1,e2)
    b = (1-e1*a)/e2
    return a,b

def euclidean_gcd(x,y):
    while(y):
        x, y = y, x %y
    return x

def modinv(a, m):
    g, x, y = gcdExtended(a, m)
    if g != 1:
        return -1
    else:
        return x % m

def findResult(c1,a,b,N,inv):
    return (pow(c1,a,N) * pow(inv,-int(b),N)) % N

def main():
    sys.setrecursionlimit(15000)
    # Parsing data.txt file
    datafile = open("data.txt","r")
    lineList = datafile.readlines()
    for line in lineList:
        if("N=" in line):
            N = int(line.replace("N=",""))
        elif("e1=" in line):
            e1 = int(line.replace("e1=",""))
        elif("e2=" in line):
            e2 = int(line.replace("e2=",""))
        elif("C1=" in line):
            c1 = int(line.replace("C1=",""))
        elif("C2=" in line):
            c2 = int(line.replace("C2=",""))
    
    #Start

    a,b = find_a_b(e1,e2)

    inv = modinv(c2,N)
    
    result = findResult(c1,a,b,N,inv)
    
    plain_text = str(result)
    
    hex_array = hex(int(plain_text)).replace("0x","")
    
    text_inverted = bytes.fromhex(hex_array).decode('UTF-8')
    # Final Result
    print(''.join(reversed(text_inverted)))
    

if __name__ == "__main__":
    main()