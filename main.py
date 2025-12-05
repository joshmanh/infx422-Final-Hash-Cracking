import csv
import hashlib
import time
import os
import re


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


def getHashes(filePath, userHash):
    hashes = {}
    hashEncoding = ""
    try:
        print(f"Attempting to load hashes from {filePath}. Please wait...")
        with open(filePath, encoding="latin-1", errors="ignore") as f:

            if re.search(r'\.txt$', filePath):
                for line in f:
                    password = line.rstrip("\n")
                    if password == "":
                        continue
                    if userHash == "md5":
                        hashAlgorithm = hashlib.md5()
                    elif userHash == "sha1":
                        hashAlgorithm = hashlib.sha1()
                    elif userHash == "sha256":
                        hashAlgorithm = hashlib.sha256()
                    else:
                        hashAlgorithm = hashlib.md5()
                    encodedPassword = password.encode('utf-8')
                    hashAlgorithm.update(encodedPassword)
                    hashes.setdefault(hashAlgorithm.hexdigest(), password)

            elif re.search(r'\.csv$', filePath):
                reader = csv.reader(f)
                header = next(reader)  # It grabs and stores the first row, assumes a header exists in the csv
                for row in reader:
                    password = row[0]  # The program assumes the password is in the second column of the csv
                    if password == "":
                        continue
                    if userHash == "md5":
                        hashAlgorithm = hashlib.md5()
                    elif userHash == "sha1":
                        hashAlgorithm = hashlib.sha1()
                    elif userHash == "sha256":
                        hashAlgorithm = hashlib.sha256()
                    else:
                        hashAlgorithm = hashlib.md5()
                    encodedPassword = password.encode('utf-8')
                    hashAlgorithm.update(encodedPassword)
                    hashes.setdefault(hashAlgorithm.hexdigest(), password)
            #
            # THIS SECTION IS FOR JSON FILES
            # elif re.search(r'\.json$', filePath):

        print(f"Loaded {len(hashes)} hashes...")
        return hashes
    except Exception as e:
        print(f"Error: {e}")
        return {}

def getPasswordHashes(filePath):
    hashes = []

    if re.search(r'\.txt$', filePath):
        with open(filePath) as f:
            for line in f:
                hash = line.rstrip("\n")
                hashes.append(hash)
    elif re.search(r'\.csv$', filePath):
        with open(filePath) as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                hash = row[1]
                hashes.append(hash)
    # elif re.search(r'\.json$', filePath):

    return hashes

def detectHashType(hashExample):
    if len(hashExample) == 32:
        print("The program has detected that the hashes are utilizing MD5 hashing algorithm. It is recommended to use this type.")
    elif len(hashExample) == 40:
        print("The program has detected that the hashes are utilizing SHA1 hashing algorithm. It is recommended to use this type.")
    elif len(hashExample) == 64:
        print("The program has detected that the hashes are utilizing SHA256 hashing algorithm. It is recommended to use this type.")
    else:
        print("The program is unable to detect the hashing algorithm used. Recommend using each one until the password(s) is/are identified.")

def getUserHashType():
    hashSelected = False
    while not hashSelected:
        print("Available Hashing Algorithms:")
        print("1. MD5")
        print("2. SHA1")
        print("3. SHA256")
        userHash = input("Select the hashing algorithm you would like to use (e.x. 1): ")

        if userHash == "1":
            userHash = "md5"
            hashSelected = True
        elif userHash == "2":
            userHash = "sha1"
            hashSelected = True
        elif userHash == "3":
            userHash = "sha256"
            hashSelected = True
        else:
            print("Invalid selection!\n")
    return userHash

def compareHashes(passwordHashes, dictionaryHashes):
    passwordStorage = {}

    isFound = False
    defaultTime = 0
    decryptedHash = ""
    attemptCounter = 0

    for hash in passwordHashes:
        passwordStorage[hash] = [isFound, defaultTime, decryptedHash, attemptCounter]

    for pHash in passwordHashes:
        attemptCounter = 0
        startTime = time.time()
        for dHash in dictionaryHashes:
            attemptCounter += 1
            if pHash == dHash:
                isFound = True
                endTime = time.time()
                decryptedHash = decryptResult(pHash, dictionaryHashes)
                passwordStorage[pHash] = [isFound, endTime - startTime, decryptedHash, attemptCounter]
                break

    displayResults(passwordStorage)


def decryptResult(pHash, dictionaryHashes):
    password = dictionaryHashes.get(pHash)
    return password

def displayResults(passwordStorage):
    print("\n#########################################")
    print("RESULTS:\n")
    for hash, data in passwordStorage.items():
        if data[0]:
            print(f"\nHash Found: {hash}")
            print(f"Time: {data[1]}s")
            print(f"Attempts Count: {data[3]}")
            print(f"Password: {data[2]}\n")
    print("#########################################")

def main():
    print("Starting Hash Cracking program...\n")

    hashes = []

    passwordsFilePath = getPasswordsFile()

    dictionaryFilePath = getDictionaryFile()

    passwordHashes = getPasswordHashes(passwordsFilePath)

    detectHashType(passwordHashes[0])

    userHash = getUserHashType()

    dictionaryHashes = getHashes(dictionaryFilePath, userHash)

    compareHashes(passwordHashes, dictionaryHashes)

    print("\nProgram Complete")

##############################
main()