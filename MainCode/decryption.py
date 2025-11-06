from PIL import Image
import numpy as np

numToLetter = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    '0','1','2','3','4','5','6','7','8','9',
    ' ','.',',','!','?',';',':','"','-','(',')',
    '@','#','$','&','*','+','=','_','%','\n','þ'
]
NULL_CHAR_INDEX = len(numToLetter) -1   # Index 85: 'þ' (our null character)


def modular_inverse(a, m):
    """Compute modular multiplicative inverse of a modulo m using Extended Euclidean Algorithm"""
    if a < 0:
        a = (a % m + m) % m
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None  # Modular inverse doesn't exist
    return (x % m + m) % m


def matrix_inverse_mod(matrix, modulus):
    """Compute the modular inverse of a 3x3 matrix mod modulus"""
    # Calculate determinant
    det = int(np.round(np.linalg.det(matrix)))
    det = det % modulus
    
    # Check if determinant is coprime with modulus (odd for mod 256)
    det_inv = modular_inverse(det, modulus)
    if det_inv is None:
        return None
    
    # Calculate adjugate matrix (transpose of cofactor matrix)
    cofactors = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            cofactor = int(np.round(np.linalg.det(minor)))
            cofactors[i][j] = ((-1) ** (i + j)) * cofactor
    
    adjugate = cofactors.T
    
    # Inverse = (det^-1 * adjugate) mod modulus
    inverse = (det_inv * adjugate) % modulus
    return inverse.astype(int)

def imgToGrid(img):
    """Convert image to 2D grid of pixels"""
    width, height = img.size
    grid = []
    
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            pixel = [r, g, b]
            row.append(pixel)
        grid.append(row)
    
    return grid


def reverseGrid(grid):
    """Remove the top random row and flatten grid to 1D pixel array"""
    # Remove first row (random row)
    dataRows = grid[1:]
    
    # Flatten to 1D pixel array
    pixelArray = []
    for row in dataRows:
        for pixel in row:
            pixelArray.append(pixel)
    
    return pixelArray


def reverseDummyPixels(pixelArray, dummyMultiplier):
    """Remove dummy pixels based on multiplier"""
    realPixels = []
    
    # Pattern: dummyMultiplier dummy pixels, then 1 real pixel
    i = 0
    while i < len(pixelArray):
        # Skip dummy pixels
        i += dummyMultiplier
        # Get real pixel if it exists
        if i < len(pixelArray):
            realPixels.append(pixelArray[i])
            i += 1
    
    return realPixels


def reverseColorShuffle(pixelArray, usedChannels):
    """Extract character data from used channels only"""
    charData = []
    
    for pixel in pixelArray:
        for channelPos in usedChannels:
            value = pixel[channelPos]
            charData.append(value)
    
    return charData


def reverseMatrixObfuscation(pixelArray, matrixData):
    """Reverse the matrix transformation using modular inverse"""
    # Parse matrix from data string
    matrix_values = list(map(int, matrixData.split(',')))
    M = np.array(matrix_values).reshape((3, 3))
    
    # Compute modular inverse
    M_inv = matrix_inverse_mod(M, 256)
    
    if M_inv is None:
        # Fallback: return original if inverse doesn't exist
        return pixelArray
    
    # Apply inverse transformation: P = (M^-1 × P') mod 256
    originalPixels = []
    for pixel in pixelArray:
        pixel_vec = np.array(pixel, dtype=int)
        original = np.dot(M_inv, pixel_vec) % 256
        originalPixels.append(original.tolist())
    
    return originalPixels


def parseKey(key):
    """Parse the encryption key into commands"""
    commands = []
    i = 0
    
    while i < len(key):
        # Check if it's the 'm' command (no length prefix)
        if key[i] == 'm':
            cmdType = key[i]
            i += 1
            # Read until end of key (m command is always last)
            cmdData = key[i:]
            commands.append({'type': cmdType, 'data': cmdData})
            break
        # Read the number indicating command length (can be multi-digit)
        elif key[i].isdigit():
            # Read all consecutive digits for the length
            length_str = ""
            while i < len(key) and key[i].isdigit():
                length_str += key[i]
                i += 1
            cmdLength = int(length_str)
            
            # Read the command type
            if i < len(key):
                cmdType = key[i]
                i += 1
            else:
                break
            
            # Read the rest of the command based on length
            # Length includes the type character, so data length is cmdLength - len(length_str) - 1
            data_length = cmdLength - len(length_str) - 1
            cmdData = key[i:i + data_length]
            i += data_length
            
            commands.append({'type': cmdType, 'data': cmdData})
        else:
            # Skip any unexpected characters
            i += 1
    
    return commands


def decryption(encryptionKey):
    """Main decryption function - only requires the key as input"""
    ImagePath = "output_image.png"
    img = Image.open(ImagePath)
    
    # Convert image to grid
    grid = imgToGrid(img)
    
    # Parse the key
    commands = parseKey(encryptionKey)
    
    # Reverse the encryption process (in reverse order)
    # 1. Remove the determinant multiplier effect (if needed - currently just for key validation)
    
    # 2. Reverse arrayToGrid
    pixelArray = reverseGrid(grid)
    
    # 3. Reverse dummyPixelGenerator
    dummyCommand = [cmd for cmd in commands if cmd['type'] == 'd'][0]
    dummyMultiplier = int(dummyCommand['data'])
    pixelArray = reverseDummyPixels(pixelArray, dummyMultiplier)
    
    # 4. Reverse matrixObfuscation
    matrixCommands = [cmd for cmd in commands if cmd['type'] == 'M']
    if matrixCommands:
        matrixCommand = matrixCommands[0]
        pixelArray = reverseMatrixObfuscation(pixelArray, matrixCommand['data'])
    
    # 5. Reverse colorShuffle
    shuffleCommand = [cmd for cmd in commands if cmd['type'] == 's'][0]
    usedChannels = [int(ch) for ch in shuffleCommand['data']]
    charData = reverseColorShuffle(pixelArray, usedChannels)
    
    # Convert character indices back to text
    finalText = ""
    for charNum in charData:
        if charNum < len(numToLetter) and charNum != NULL_CHAR_INDEX:
            finalText += numToLetter[charNum]
    
    print("Decrypted Text: \n")
    print(finalText)
    return finalText
    