import hashlib
import os


def getPasswordsFile():
    isFile = False

    folder = os.listdir("./passwords")
    selector = 1
    passOptions = {}

    for file in folder:
        passOptions[selector] = file
        selector += 1

    while not isFile:
        print("Available Password Files: ")
        for key, value in passOptions.items():
            print(f"{key}: {value}")
        print()
        temp = input("Select the number associated to the wanted file: ")
        selection = int(temp)

        if selection not in passOptions:
            print("Invalid selection!\n")
            continue

        filePath = f"./passwords/{passOptions[selection]}"

        try:
            with open(filePath) as f:
                print()
                isFile = True
        except Exception:
            print("File not found!\n")

    finalFilePath = filePath
    return finalFilePath


def getPasswordHashes(filePath):
    hashes = []

    with open(filePath) as f:
        for line in f:
            hashes.append(line.strip())

    return hashes


def getDictionaryHashes():
    isDict = False

    txtDictsHasItem = True
    csvDictsHasItem = True

    txtOptions = {}
    csvOptions = {}

    hashes = []

    txtDicts = os.listdir("./dictionaries/txt")
    csvDicts = os.listdir("./dictionaries/csv")

    if not txtDicts:
        csvDictsHasItem = False

    if not csvDicts:
        csvDictsHasItem = False

    selector = 1

    if txtDictsHasItem:
        for file in txtDicts:
            txtOptions[selector] = file
            selector += 1

        selector = 1

    if csvDictsHasItem:
        for file in csvDicts:
            csvOptions[selector] = file
            selector += 1

    while not isDict:
        if txtDictsHasItem:
            
            print("Available Text Dictionaries: ")
            for key, value in txtOptions.items():
                print(f"{key}: {value}")
            print()
        if csvDictsHasItem:
            print("Available CSV Dictionaries: ")
            for key, value in csvOptions.items():
                print(f"{key}: {value}")
            print()

        temp = input("Select the number associated to the wanted dictionary: ")











def main():
    print("Starting Hash Cracking program...")
    print("")

    hashes = []
    fileName = getPasswordsFile()
    passwordHashes = getPasswordHashes(fileName)

##############################
main()