import aes
import des
import sys
import argparse


aes = aes()
des = des()

my_parser = argparse.ArgumentParser()

my_parser.add_argument('File',metavar='File_Path',type=str,help='The path to file with seperator (-)')

# Parse arguments
args = my_parser.parse_args()

file_name = args.File

file_pieces = file_name.split("-")

if __name__ == "__main__":
    
    try:
        if sys.argv[1] == "enc":
            aes.encrypt(sys.argv[2], sys.argv[3],sys.argv[4])
        if sys.argv[1] == "dec":
            aes.decrypt(sys.argv[2], sys.argv[3],sys.argv[4])
    except :
        print("Argument 1 is encrypt or decrypt (enc,dec), Argument 2 is passwordFile, Argument 3 is the inputFile, Argument 4 is the outputFile")