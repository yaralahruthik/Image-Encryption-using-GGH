from PIL import Image
import random
import numpy as np
import base64
import binascii
import os


# This function generates a private and public key

def keyGen(dimension):
    privateKey = []
    print("Searching for a private key")
    ratio = 1
    '''
    while True:
        privateKey = np.random.randint(-10, 10, size=(dimension,dimension))
        ratio = hadamardRatio(privateKey, dimension)
        if(.9 <= ratio <= 1):
            print(privateKey)
            break
    '''
    privateKey = np.identity(dimension)
    print(privateKey)

    print("Searching for a public key")
    while True:
        uniMod = randUniMod(dimension)
        temp = np.matmul(uniMod, privateKey)
        ratio = hadamardRatio(temp, dimension)
        if ratio <= .1:
            publicKey = temp
            break
    print(publicKey)

    return privateKey, publicKey, uniMod


# This function returns the Hadamard Ratio of a matrix

def hadamardRatio(matrix, dimension):
    detOfLattice = np.linalg.det(matrix)
    detOfLattice = detOfLattice if detOfLattice > 0 else -detOfLattice
    mult = 1
    for v in matrix:
        mult = mult * np.linalg.norm(v)
    hadRatio = (detOfLattice / mult) ** (1.0/dimension)
    return hadRatio


# This function returns a Random Unimodular matrix

def randUniMod(dimension):
    random_matrix = [[np.random.randint(-10, 10,)
                      for _ in range(dimension)] for _ in range(dimension)]
    upperTri = np.triu(random_matrix, 0)
    lowerTri = [[np.random.randint(-10, 10) if x <
                 y else 0 for x in range(dimension)] for y in range(dimension)]

    #Creating an upper trianglular and lower triangular matrices with diagonals as +1 or -1
    for r in range(len(upperTri)):
    	for c in range(len(upperTri)):
    		if(r == c):
    			if bool(random.getrandbits(1)):
    				upperTri[r][c] = 1
    				lowerTri[r][c] = 1
    			else:
    				upperTri[r][c] = -1
    				lowerTri[r][c] = -1
    uniModular = np.matmul(upperTri, lowerTri)
    return uniModular


# Encoded text to Encrypted Ints

def encodedToBinaryToEncrypted(r, g, b, seekVal):
    encryptedRedInts = []
    encryptedGreenInts = []
    encryptedBlueInts = []
    encryptedRedInts = r[seekVal:seekVal+10]
    encryptedGreenInts = g[seekVal:seekVal+10]
    encryptedBlueInts = b[seekVal:seekVal+10]

    return encryptedRedInts, encryptedGreenInts, encryptedBlueInts


# Encryption Function

def encrypt(encryptedInts, publicKey):
    cypherText = []
    cypherText = np.matmul(encryptedInts, publicKey)

    #print("\n---------------------Cypher Array---------------------\n", cypherText)
    return cypherText


# Decryption Function

def decrypt(cypherText, privateKey, uniModular):
    A = privateKey
    x = cypherText
    BPRIME = np.linalg.inv(A)
    BB = np.matmul(BPRIME, x)
    uniModularInv = np.linalg.inv(uniModular)
    m = np.round(np.matmul(BB, uniModularInv)).astype(int)

    #print("\n---------------------Message Array---------------------\n", m)

    return m


def loadPixels(file_path):
    imagePixelLoad = Image.open(file_path)
    pix = imagePixelLoad.load()
    return imagePixelLoad, pix


def rgb(imagePixelLoad, pix):
    r = []
    g = []
    b = []
    for i in range(imagePixelLoad.size[0]):
        r.append([])
        g.append([])
        b.append([])
        for j in range(imagePixelLoad.size[1]):
            rgbPerPixel = pix[i, j]
            r[i].append(rgbPerPixel[0])
            g[i].append(rgbPerPixel[1])
            b[i].append(rgbPerPixel[2])

    m = imagePixelLoad.size[0]
    n = imagePixelLoad.size[1]
    return r, g, b, m, n


def writePixels(r, g, b, m, n):
    redArray = np.asarray(r)
    greenArray = np.asarray(g)
    blueArray = np.asarray(b)
    with open('red.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(r[i][j]) + " ")
    rfile.close()
    with open('green.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(g[i][j]) + " ")
    rfile.close()
    with open('blue.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(b[i][j]) + " ")
    rfile.close()


def writeEncryptedPixels(r, g, b, m, n):
    redArray = np.asarray(r)
    greenArray = np.asarray(g)
    blueArray = np.asarray(b)
    with open('redEnc.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(r[i][j]) + " ")
    rfile.close()
    with open('greenEnc.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(g[i][j]) + " ")
    rfile.close()
    with open('blueEnc.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(b[i][j]) + " ")
    rfile.close()


def writeDecryptedPixels(r, g, b, m, n):
    redArray = np.asarray(r)
    greenArray = np.asarray(g)
    blueArray = np.asarray(b)
    with open('redDec.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(r[i][j]) + " ")
    rfile.close()
    with open('greenDec.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(g[i][j]) + " ")
    rfile.close()
    with open('blueDec.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(b[i][j]) + " ")
    rfile.close()


def readPixels():
    with open("red.txt") as f:
        for line in f:
            r = list(map(int, line.split()))
    with open("green.txt") as f:
        for line in f:
            g = list(map(int, line.split()))
    with open("blue.txt") as f:
        for line in f:
            b = list(map(int, line.split()))
    return r, g, b


def writeEncryptedPixelsForImage(r, g, b, m, n):
    redArray = np.asarray(r)
    greenArray = np.asarray(g)
    blueArray = np.asarray(b)
    redArray = redArray%26
    greenArray = greenArray%26
    blueArray = blueArray%26
    with open('redEncPix.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(int(redArray[i][j])) + " ")
    rfile.close()
    with open('greenEncPix.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(int(greenArray[i][j])) + " ")
    rfile.close()
    with open('blueEncPix.txt', 'w') as rfile:
        for i in range(m):
            for j in range(n):
                rfile.write(str(int(blueArray[i][j])) + " ")
    rfile.close()


def encryptedImagePixelBack():
    im = Image.new('RGB', (100, 100))
    pix = im.load()
    R = []
    G = []
    B = []
    with open("redEncPix.txt") as f:
        for line in f:
            R = list(map(int, line.split()))
    with open("greenEncPix.txt") as f:
        for line in f:
            G = list(map(int, line.split()))
    with open("blueEncPix.txt") as f:
        for line in f:
            B = list(map(int, line.split()))

    R = np.reshape(R, (100, 100))
    G = np.reshape(G, (100, 100))
    B = np.reshape(B, (100, 100))
    shape1, shape2 = np.shape(R)
    for i in range(shape1):
        for j in range(shape2):
            pix[i, j] = (R[i][j], G[i][j], B[i][j])

    im.save("EncryptedImage.jpg")


def writeBackPixels():
    im = Image.new('RGB', (100, 100))
    pix = im.load()
    R = []
    G = []
    B = []
    with open("redDec.txt") as f:
        for line in f:
            R = list(map(int, line.split()))
    with open("greenDec.txt") as f:
        for line in f:
            G = list(map(int, line.split()))
    with open("blueDec.txt") as f:
        for line in f:
            B = list(map(int, line.split()))

    R = np.reshape(R, (100, 100))
    G = np.reshape(G, (100, 100))
    B = np.reshape(B, (100, 100))
    shape1, shape2 = np.shape(R)
    for i in range(shape1):
        for j in range(shape2):
            pix[i, j] = (R[i][j], G[i][j], B[i][j])

    im.save("decryptedImage.jpg")



def main():
    cypherTextRedFile = []
    cypherTextGreenFile = []
    cypherTextBlueFile = []
    
    alice = keyGen(10)

    imagePixelLoad, pix = loadPixels("InputImages\\1.jpg")
    r, g, b, m, n = rgb(imagePixelLoad, pix)
    writePixels(r, g, b, m, n)
    r, g, b = readPixels()
    
    print("\n------------------------------Encrypting------------------------------\n")
    seekVal = 0
    while True:
        RedInts, GreenInts, BlueInts = encodedToBinaryToEncrypted(r, g, b, seekVal)
        if (seekVal == 10000):
            break
        else:
            seekVal = seekVal + 10

        bobRed = encrypt(RedInts, alice[1])
        bobGreen = encrypt(GreenInts, alice[1])
        bobBlue = encrypt(BlueInts, alice[1])
        cypherTextRedFile.append(bobRed)
        cypherTextGreenFile.append(bobGreen)
        cypherTextBlueFile.append(bobBlue)
    
    shape1, shape2 = np.shape(cypherTextRedFile)
    writeEncryptedPixels(cypherTextRedFile, cypherTextGreenFile, cypherTextBlueFile, shape1, shape2)
    writeEncryptedPixelsForImage(cypherTextRedFile, cypherTextGreenFile, cypherTextBlueFile, shape1, shape2)
    encryptedImagePixelBack()

    print("\n------------------------------Decrypting------------------------------\n")
    seekVal = 0
    decryptedReds = []
    decryptedGreens = []
    decryptedBlues = []

    while True:
        if (seekVal == len(cypherTextRedFile)):
            break
        else:
            aliceRedReceives = decrypt(cypherTextRedFile[seekVal], alice[0], alice[2])
            aliceGreenReceives = decrypt(cypherTextGreenFile[seekVal], alice[0], alice[2])
            aliceBlueReceives = decrypt(cypherTextBlueFile[seekVal], alice[0], alice[2])
            decryptedReds.append(aliceRedReceives)
            decryptedGreens.append(aliceGreenReceives)
            decryptedBlues.append(aliceBlueReceives)
        
        seekVal = seekVal + 1

    shape1, shape2 = np.shape(decryptedReds)
    writeDecryptedPixels(decryptedReds, decryptedGreens, decryptedBlues, shape1, shape2)
    writeBackPixels()

    


if __name__ == "__main__":
    main()
