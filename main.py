import csv
import hashlib
import time
import os
import re
import json

def getPasswordsFile():
    """
    Allows the user to select a password file from a list of files in the passwords folder.

    This function reads the /passwords directory and displays a list of available files to the user.
    The user is then allowed to select a file by entering the associated number. The function checks if
    the selected number is valid and returns the filepath if it is.

    :return: finalFilePath: The filepath of the selected file.
    """
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
    """
    Obtains the filepath of the selected dictionary file.

    This function checks in both the /dictionaries/txt and dictionaries/csv directories for available files. If any are available,
    the function displays a list of them to the user, allowing them to select one. If the selected file is valid, the function returns
    the filepath.

    :return: finalFilePath: The filepath of the selected dictionary file.
    """
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
    """
    Calculates and stores the hashes of the file at the specified path.

    This function creates a python dictionary to house the hashes and their corresponding passwords. Based on the hashing
    algorithm provided (in variable userHash), the function determines whether the file is in text, csv, or json format.
    It accommodates for the file type and reads through it, collecting the passwords and calculating their hashes. It then stores
    the hashes and passwords in the python dictionary and returns it.

    :param filePath: The filepath of the file containing the passwords to be hashed.
    :param userHash: The hashing algorithm selected by the user.
    :return: hashes: The Python dictionary containing the hashes and passwords.

    """
    hashes = {}
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
    """
    Calculates and stores the hashes of the user selected passwords file (the file containing passwords to be cracked).

    This function reads the file at the specified path and determines if it is in text, csv, or json format. Based on the file type,
    it reads through the file and collects the hashes, storing them in a list. The function then returns the list of hashes. This is different
    from the getHashes function, specifically because this function does not have the plaintext passwords as part of the file data.

    :param filePath:
    :return: hashes: A list of the hashed passwords
    """
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
    elif re.search(r'\.json$', filePath):
        with open(filePath) as f:
            fileData = json.load(f)
            for user in fileData:
                hashes.append(user["password"])
    return hashes

def detectHashType(hashExample):
    """
    Detects the hashing algorithm performed on the password(s) wanting to be cracked.

    This function takes in a single hash and uses its length to determine which hashing algorithm was used.
    It prints a recommendation on which hashing algorithm the user should use.

    :param hashExample: A single example hash obtained from the user's password file.
    :return:
    """
    if len(hashExample) == 32:
        print("The program has detected that the hashes are utilizing MD5 hashing algorithm. It is recommended to use this type.")
    elif len(hashExample) == 40:
        print("The program has detected that the hashes are utilizing SHA1 hashing algorithm. It is recommended to use this type.")
    elif len(hashExample) == 64:
        print("The program has detected that the hashes are utilizing SHA256 hashing algorithm. It is recommended to use this type.")
    else:
        print("The program is unable to detect the hashing algorithm used. Recommend using each one until the password(s) is/are identified.")

def getUserHashType():
    """
    Gets the hashing algorithm the user wants to use for the cracking process.

    This function prompts the user to select a hashing algorithm from MD5, SHA1, or SHA256. It checks if the selection is valid, and if
    it is, returns the user's selection.

    :return: userHash: the hashing algorithm selected by the user.
    """
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
    """
    Compares the hashes of the user's passwords against the hashes of the dictionary.

    This function uses a nested for loop to iterate through each hash in the dictionary and compare it to each hash of the user's password list.
    If a match is found, the function stores a truthy boolean value, the total execution time for the hash comparison, the plaintext password,
    and the number of attempts occurred to reach a match in a dictionary (passwordStorage). After finishing all loops, it runs the displayResults function.

    :param passwordHashes: A list of the hashes user passwords (to be cracked).
    :param dictionaryHashes: A dictionary containing the hashes of the dictionary file and their corresponding plaintext passwords.
    :return:
    """
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
    """
    Gets the plaintext password corresponding to the provided hash.

    A small function used in compareHashes to obtain the plaintext password of the given hash in the dictionary.

    :param pHash: The hash wanted to be decrypted.
    :param dictionaryHashes: The dictionary containing the hashes and their corresponding plaintext passwords.
    :return: The plaintext password corresponding to the provided hash.
    """
    password = dictionaryHashes.get(pHash)
    return password

def displayResults(passwordStorage):
    """
    Displays the results of the cracking process.

    A small function used in compareHashes to display the results of the cracking process in a readable format.

    :param passwordStorage: A dictionary containing the results of the cracking process.
    :return:
    """
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
    """
    Main function of the hashing-cracking program.
    :return:
    """
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

#########################################
if __name__ == "__main__":
    main()