import hashlib
import time
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

def getDictionaryFile():
    selector = 1
    isDict = False

    txtDictsHasItem = True
    csvDictsHasItem = True

    txtOptions = {}
    csvOptions = {}

    txtDicts = os.listdir("./dictionaries/txt")
    csvDicts = os.listdir("./dictionaries/csv")

    if not txtDicts:
        txtDictsHasItem = False

    if not csvDicts:
        csvDictsHasItem = False


    if txtDictsHasItem:
        for file in txtDicts:
            txtOptions[selector] = file
            selector += 1

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
        temp = int(temp)
        print()
        if txtOptions.get(temp) == None and csvOptions.get(temp) == None:
            print("\nInvalid selection!\n")
            continue

        filePath = temp
        isDict = True

    if filePath in txtOptions:
        filePath = f"./dictionaries/txt/{txtOptions[filePath]}"
    else:
        filePath = f"./dictionaries/csv/{csvOptions[filePath]}"

    finalFilePath = filePath

    return finalFilePath


def getHashes(filePath):
    hashes = {}
    try:
        print(f"Attempting to load hashes from {filePath}. Please wait...")
        with open(filePath, encoding="latin-1", errors="ignore") as f:
            for line in f:
                line = line.strip("\n")
                if line == "":
                    continue
                md5 = hashlib.md5()
                encodedLine = line.encode('utf-8')
                md5.update(encodedLine)
                hashes.setdefault(md5.hexdigest(), line)
        print(f"Loaded {len(hashes)} hashes...")
        return hashes
    except Exception as e:
        print(f"Error: {e}")
        return {}

def getPasswordHashes(filePath):
    hashes = []

    with open(filePath) as f:
        for line in f:
            hash = line.strip()
            hashes.append(hash)
    return hashes



def compareHashes(passwordHashes, dictionaryHashes):
    passwordStorage = {}

    isFound = False
    defaultTime = 0
    decryptedHash = ""

    for hash in passwordHashes:
        passwordStorage[hash] = [isFound, defaultTime, decryptedHash]

    for pHash in passwordHashes:
        startTime = time.time()
        for dHash in dictionaryHashes:
            if pHash == dHash:
                isFound = True
                endTime = time.time()
                decryptedHash = decryptResult(pHash, dictionaryHashes)
                passwordStorage[pHash] = [isFound, endTime - startTime, decryptedHash]
                break

    displayResults(passwordStorage)


def decryptResult(pHash, dictionaryHashes):
    password = dictionaryHashes.get(pHash)
    password = password.strip()
    return password

def displayResults(passwordStorage):
    print("\n###############")
    print("RESULTS:")
    for hash, data in passwordStorage.items():
        if data[0]:
            print(f"\nHash Found: {hash}")
            print(f"Time: {data[1]}s")
            print(f"Password: {data[2]}\n")
    print("###############")

def main():
    print("Starting Hash Cracking program...\n")

    hashes = []

    passwordsFilePath = getPasswordsFile()

    dictionaryFilePath = getDictionaryFile()

    passwordHashes = getPasswordHashes(passwordsFilePath)

    dictionaryHashes = getHashes(dictionaryFilePath)

    compareHashes(passwordHashes, dictionaryHashes)

    print("\nProgram Complete")

##############################
main()