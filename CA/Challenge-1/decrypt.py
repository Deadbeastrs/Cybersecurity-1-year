from collections import Counter
import argparse

my_parser = argparse.ArgumentParser()

my_parser.add_argument('File',metavar='File Path',type=str,help='The path to the encrypted file')
my_parser.add_argument('Language',metavar='Language',type=str,help='Choose laguage: eng,pt')
my_parser.add_argument('OutFile',metavar='Out File Path',type=str,help='The path to the file for output')

# Parse arguments
args = my_parser.parse_args()

file_name = args.File
lang = args.Language
outfile = args.OutFile

#decrypt with key
def decrypt(ciphertext, key):
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    ciphertext_int = [ord(i) for i in ciphertext]
    plaintext = ''
    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
        plaintext += chr(value + 65)
    return plaintext

#Find the estimated key length
def findKeyLength(charlist):
    similarity = []
    limit = 0 # Value used to limit the search
    for i in range(1,len(charlist)):
        similarity.append(len([a for a in list(zip(charlist[i:],charlist)) if a[0] == a[1]]))
        limit+= 1
        if limit == 100:
            limit = 0
            break

    min_val = min(similarity)
    max_val = max(similarity)

    distance = []
    counter = 0
    for a in range(0,len(similarity)):
        counter+=1
        if similarity[a] > min_val+((max_val-min_val) / 2) :
            distance.append(counter)
            counter = 0

    t_counter = Counter( distance)
    keyLength = t_counter.most_common(1)[0][0]
    return keyLength

def findKey(charlist,keyLength):
    simToProb = {}
    #Initialize arrays
    groups = []
    for i in range(0,keyLength):
        groups.append([])
    counter2 = 0
    for char in range(0,len(charlist)):
        groups[counter2].append(charlist[char])
        counter2 += 1
        if counter2 == keyLength:
            counter2 = 0

    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    leterFreq = {}

    for group in range(0,len(groups)):
        leterFreq[group] = []
        for letter in letters:
            leterFreq[group].append((letter,''.join(groups[group]).count(letter) / len(groups[group])))

    key = ""

    for singleLetterFreq in leterFreq:
        key += max(leterFreq[singleLetterFreq], key=lambda x: x[1])[0]

    dec_key = ""

    if lang == "eng":
        for charac in key:
            dec_key += chr(((ord(charac) - 97 + 22) % 26)+97) # Execute the E column correspondance, not needed for portuguese
    else:
        dec_key = key
    return dec_key

encrypted_text = open(file_name,"r")

encrypted_text_clean = encrypted_text.readlines()[0].replace('\n','')
charlist = [char for char in encrypted_text_clean]

keyLength = findKeyLength(charlist)

real_key = findKey(charlist,keyLength)

#Write to file
dypted_text = open(outfile,"w")
dypted_text.write(decrypt(encrypted_text_clean,real_key))
