import hashlib
import os

def main():
    print("Starting Hash Cracking program...")
    hashes = []
    fileName = getPasswordsFile()
    passwordHashes = getPasswordHashes(fileName)


def getPasswordsFile():
    isFile = False

    while not isFile:
        temp = input("Enter the name of the file (I.E passwords.txt): ")
        filePath = f"./passwords/{temp}"
        try:
            with open(filePath) as f:
                print("File found!")
                isFile = True
        except Exception:
            print("File not found!")

    finalFilePath = filePath
    return finalFilePath


def getPasswordHashes(filePath):
    hashes = []

    with open(filePath) as f:
        for line in f:
            hashes.append(line.strip())

    return hashes


def getDictionaryHashes():
    hashes = []
    dictionaryOptions = []
    os.listdir("./dictionaries")














##############################
main()