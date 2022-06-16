# Problem 1: Encrypt/Decrypt with Playfair Cipher
def convertPlainTextToPairs (plainText):
    # append X if two letters are being repeated
    for s in range(0,len(plainText)+1,2):
        if s<len(plainText)-1:
            if plainText[s]==plainText[s+1]:
                plainText=plainText[:s+1]+'X'+plainText[s+1:]

    # append X if the total letters are odd, to make plaintext even
    if len(plainText)%2 != 0:
        plainText = plainText[:]+'X'

    return plainText

# Generate a cipher key matrix
def generateKeyMatrix (key): 
    # Creating an empty 5x5 matrix filled with zeros
    # [
    #   [0, 0, 0, 0, 0],
    #   [0, 0, 0, 0, 0], 
    #   [0, 0, 0, 0, 0], 
    #   [0, 0, 0, 0, 0], 
    #   [0, 0, 0, 0, 0]
    # ]
    matrix_5x5 = [[0 for i in range (5)] for j in range(5)]


    simpleKeyArr = []


    """
     Two conditions
     1. Characters can't repeat
     2. Replace J as I
     3. Replace K as C
     4. Make 25th character a space
    """
    for c in key:
        if c not in simpleKeyArr:
            if c == 'J':
                simpleKeyArr.append('I')
            elif c == 'K':
                simpleKeyArr.append('C')
            else:
                simpleKeyArr.append(c)


    # Now fill the remainder of alphabet to arr

    is_I_exist = "I" in simpleKeyArr
    is_C_exist = "C" in simpleKeyArr

    # A-Z's ASCII Value lies between 65 to 90 but as range's second parameter excludes that value we will use 65 to 91
    for i in range(65,91):
        if chr(i) not in simpleKeyArr:
            # I = 73
            # J = 74
            # K = 75
            # C = 67
            # We want I and C in simpleKeyArr not J and K


            if i==73 and not is_I_exist:
                simpleKeyArr.append("I")
                is_I_exist = True
            elif i == 67 and not is_C_exist:
                simpleKeyArr.append("C")
                is_C_exist = True
            elif (i==73 or i==74 and is_I_exist) or (i==67 or i==75 and is_C_exist):
                pass
            else:
                simpleKeyArr.append(chr(i))

    simpleKeyArr.append(" ")

   # Mapping simpleCharArr to Matrix
    index = 0
    for i in range(0,5):
        for j in range(0,5):
            matrix_5x5[i][j] = simpleKeyArr[index]
            index+=1



    return matrix_5x5

# Locate index of character in cipher key matrix
def indexLocator (char,cipherKeyMatrix):
    indexOfChar = []

    # convert the character value from J to I
    if char=="J":
        char = "I"
    if char=="K":
        char = "C"

    for i,j in enumerate(cipherKeyMatrix):
        # enumerate will return object like this:         
        # [
        #   (0, ['C', 'A', 'R', 'E', 'N']),
        #   (1, ['D', 'B', 'F', 'G', 'H']), 
        #   (2, ['I', 'L', 'M', 'O', 'P']), 
        #   (3, ['Q', 'S', 'T', 'U', 'V']), 
        #   (4, ['W', 'X', 'Y', 'Z', ' '])
        # ]
        # i,j will map to tupels of above array


        # j refers to inside matrix =>  ['C', 'A', 'R', 'E', 'N'],
        for k,l in enumerate(j):
            # again enumerate will return object that look like this in first iteration: 
            # [(0,'C'),(1,'A'),(2,'R'),(3,'E'),(4,'N')]
            # k,l will map to tupels of above array
            if char == l:
                indexOfChar.append(i) #add 1st dimension of 5X5 matrix => i.e., indexOfChar = [i]
                indexOfChar.append(k) #add 2nd dimension of 5X5 matrix => i.e., indexOfChar = [i,k]
                return indexOfChar
              
            # Now with the help of indexOfChar = [i,k] we can pretty much locate every element,
            # inside our 5X5 matrix like this =>  cipherKeyMatrix[i][k]

# Encrypt plaintext
def encryption (plainText,key):
    cipherText = []
    # 1. Generate Key Matrix
    keyMatrix = generateKeyMatrix(key)

    i = 0
    while i < len(plainText):
        # 2 Find where the pair are located in matrix
        n1 = indexLocator(plainText[i],keyMatrix)
        n2 = indexLocator(plainText[i+1],keyMatrix)

        # 3.1  If same column then go down one
        if n1[1] == n2[1]:
            i1 = (n1[0] + 1) % 5
            j1 = n1[1]

            i2 = (n2[0] + 1) % 5
            j2 = n2[1]
            cipherText.append(keyMatrix[i1][j1])
            cipherText.append(keyMatrix[i2][j2])

        # 3.2 If on same row, go right
        elif n1[0]==n2[0]:
            i1= n1[0]
            j1= (n1[1] + 1) % 5

            i2= n2[0]
            j2= (n2[1] + 1) % 5
            cipherText.append(keyMatrix[i1][j1])
            cipherText.append(keyMatrix[i2][j2])


        # 3.3 If on different columns and rows, then make a reactangle with pair
        # Swap corner characters with opposite character.
        else:
            i1 = n1[0]
            j1 = n1[1]

            i2 = n2[0]
            j2 = n2[1]

            cipherText.append(keyMatrix[i1][j2])
            cipherText.append(keyMatrix[i2][j1])

        i += 2  
    return cipherText

#To decrypt the cipher text
def decryption (cipherText, key):
    plainText = []

    keyMatrix = generateKeyMatrix(key) 

    i = 0
    while i < len(cipherText):
        # 2.1 calculate two grouped characters indexes from keyMatrix
        n1 = indexLocator(cipherText[i],keyMatrix)
        n2 = indexLocator(cipherText[i+1],keyMatrix)

        # 3.1  If same column then go up one
        if n1[1] == n2[1]:
            i1 = (n1[0] - 1) % 5
            j1 = n1[1]

            i2 = (n2[0] - 1) % 5
            j2 = n2[1]
            plainText.append(keyMatrix[i1][j1])
            plainText.append(keyMatrix[i2][j2])
            

        # 3.2 If on same row, go right
        elif n1[0]==n2[0]:
            i1= n1[0]
            j1= (n1[1] - 1) % 5


            i2= n2[0]
            j2= (n2[1] - 1) % 5
            plainText.append(keyMatrix[i1][j1])
            plainText.append(keyMatrix[i2][j2])

        # 3.3 If on different columns and rows, then make a reactangle with pair
        # Swap corner characters with opposite character.
        else:
            i1 = n1[0]
            j1 = n1[1]

            i2 = n2[0]
            j2 = n2[1]

            plainText.append(keyMatrix[i1][j2])
            plainText.append(keyMatrix[i2][j1])
      
        i += 2  
    return plainText

def main():

    #Getting user inputs Key (to make the 5x5 char matrix) and Plain Text
    key = input("Enter key: ").replace(" ","").upper()
    plainText =input("Plain Text: ").replace(" ","").upper()

    convertedPlainText = convertPlainTextToPairs(plainText)

    cipherText = encryption(convertedPlainText,key)
    print("Encrypted text: "," ".join(cipherText))

    decryptPlainText = decryption(cipherText,key)
    print("Decrypted text: "," ".join(decryptPlainText))
    

if __name__ == "__main__":
    main()