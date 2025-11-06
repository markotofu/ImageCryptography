
from PIL import Image
import numpy as np
import random

key = ""
numToLetter = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    '0','1','2','3','4','5','6','7','8','9',
    ' ','.',',','!','?',';',':','"','-','(',')',
    '@','#','$','&','*','+','=','_','%','\n','þ'
]
NULL_CHAR_INDEX = len(numToLetter) - 1  # Index 85: 'þ' (our null character)


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


def textToArray(textSize, userText):

    pixelArray = []
    for i in range(textSize):
                char = userText[i]
                char_num = numToLetter.index(char) if char in numToLetter else NULL_CHAR_INDEX
                pixelArray.append(char_num)

    grid = randomizedEncryption(pixelArray)
    
    # Create image from the grid
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    img = Image.new('RGB', (width, height))
    
    for y in range(height):
        for x in range(width):
            pixel = grid[y][x]
            r = int(pixel[0])
            g = int(pixel[1])
            b = int(pixel[2])
            img.putpixel((x, y), (r, g, b))
    
    return img

def randomizedEncryption(inputArray):
    count = 0 
    usedMethods = []
    inputArray= colorShuffle(inputArray)
    inputArray= matrixObfuscation(inputArray)
    inputArray= dummyPixelGenerator(inputArray)
    inputArray= arrayToGrid(inputArray)
    multiplier, randomPos = detMultiplier(inputArray)

    return inputArray

def matrixObfuscation(pixelArray):
    """Apply reversible 3x3 matrix transformation using modular arithmetic (mod 256)"""
    global key
    
    # Generate a random 3x3 matrix with odd determinant (coprime with 256)
    max_attempts = 100
    for attempt in range(max_attempts):
        # Use small random integers to avoid overflow
        M = np.random.randint(-5, 6, (3, 3))
        det = int(np.round(np.linalg.det(M)))
        
        # Check if determinant is odd (coprime with 256)
        if det % 2 != 0:
            # Verify the inverse exists
            M_inv = matrix_inverse_mod(M, 256)
            if M_inv is not None:
                break
    else:
        # Fallback to identity matrix if no valid matrix found
        M = np.eye(3, dtype=int)
    
    # Apply transformation to each pixel: P' = (M × P) mod 256
    transformedPixels = []
    for pixel in pixelArray:
        pixel_vec = np.array(pixel, dtype=int)
        transformed = np.dot(M, pixel_vec) % 256
        transformedPixels.append(transformed.tolist())
    
    # Encode matrix in key: flatten to 9 values
    matrix_flat = M.flatten().tolist()
    matrix_str = ','.join(map(str, matrix_flat))
    
    # Calculate total command length: <length_digits><type><data>
    # We need to account for the length prefix itself
    data_plus_type = 1 + len(matrix_str)  # 'M' + data
    length_digits = len(str(data_plus_type))
    total_length = length_digits + data_plus_type
    
    command = f"{total_length}M{matrix_str}"
    key += command
    
    return transformedPixels

def dummyPixelGenerator(inputArray):
    global key
    dummyMultiplier = random.randint(2, 7)
    finalArray = []
    
    # inputArray is now 2D: [[R, G, B], [R, G, B], ...]
    for i in range(len(inputArray)):
        # Add dummy pixels before each real pixel
        for j in range(dummyMultiplier):
            dummyPixel = [random.randint(0, NULL_CHAR_INDEX) for _ in range(3)]
            finalArray.append(dummyPixel)
        # Add the real pixel
        finalArray.append(inputArray[i])

    key += "3d"+str(dummyMultiplier)
    return finalArray



def colorShuffle(inputArray):
    global key
    # Shuffle channel order
    channels = [0, 1, 2]
    random.shuffle(channels)
    
    # Randomly remove channels
    usedChannels = channels.copy()
    for i in range(len(usedChannels)-1):
        if random.randint(1,3) == 1:
            usedChannels.pop(0)
    
    # Find which channels were removed
    allChannels = [0, 1, 2]
    removedChannels = [ch for ch in allChannels if ch not in usedChannels]
    
    # Calculate number of pixels needed
    numUsedChannels = len(usedChannels)
    numPixels = len(inputArray) // numUsedChannels
    if len(inputArray) % numUsedChannels != 0:
        numPixels += 1  # Need extra pixel for remaining characters
    
    # Create 2D pixel representation
    pixelData = []
    charIndex = 0
    
    for i in range(numPixels):
        pixel = [NULL_CHAR_INDEX, NULL_CHAR_INDEX, NULL_CHAR_INDEX]  # Default to null character
        
        # Place character data in used channels
        for channelPos in usedChannels:
            if charIndex < len(inputArray):
                pixel[channelPos] = inputArray[charIndex]
                charIndex += 1
            else:
                pixel[channelPos] = NULL_CHAR_INDEX  # Null character for padding
        
        # Fill removed channels with random values
        for channelPos in removedChannels:
            pixel[channelPos] = random.randint(0, NULL_CHAR_INDEX)
        
        pixelData.append(pixel)
    
    # Build command string
    command = str(2+len(usedChannels)) + "s"
    for ch in usedChannels:
        command += str(ch)
    
    key += command
    return pixelData


def dimensionChecker(inputArray):
    # Calculate width and height for square-ish image
    num_pixels = len(inputArray)
    if num_pixels == 0:
        return 1, 1
    
    width = int(np.sqrt(num_pixels))
    height = int(np.ceil(num_pixels / width))
    return width, height


def detMultiplier(grid):
    """
    Picks a random pixel from the top row (not at ends), creates a 3x3 matrix from it
    and its neighbors, finds the determinant, and returns a multiplier (1, 2, or 3).
    """
    global key
    topRow = grid[0]
    width = len(topRow)
    
    # Pick a random position from top row (not at ends)
    if width <= 3:
        randomPos = 1  # If exactly 3 wide, use middle position
    else:
        randomPos = random.randint(1, width - 2)  # Exclude first and last
    
    # Get the three pixels: left, center (picked), right
    pixelLeft = topRow[randomPos - 1]
    pixelCenter = topRow[randomPos]
    pixelRight = topRow[randomPos + 1]
    
    # Create a 3x3 matrix from the three pixels
    matrix = np.array([
        pixelLeft,    # [R, G, B] from left pixel
        pixelCenter,  # [R, G, B] from center pixel
        pixelRight    # [R, G, B] from right pixel
    ])
    
    # Calculate determinant
    det = int(np.linalg.det(matrix))
    
    # Convert to multiplier (1, 2, or 3)
    multiplier = (abs(det) % 3) + 1  # Ensures result is 1, 2, or 3
    
    command = "m" + str(randomPos) + "," + str(multiplier)
    key += command
    
    return multiplier, randomPos


def arrayToGrid(inputArray):

    width, height = dimensionChecker(inputArray)
    
    # Create a random row at the top
    randomRow = []
    for i in range(width):
        randomPixel = [random.randint(0, NULL_CHAR_INDEX) for _ in range(3)]
        randomRow.append(randomPixel)
    
    # Create the grid with random row at top
    grid = [randomRow]  # Start with random row
    
    # Add the actual data rows
    pixelIndex = 0
    for y in range(height):
        row = []
        for x in range(width):
            if pixelIndex < len(inputArray):
                row.append(inputArray[pixelIndex])
                pixelIndex += 1
            else:
                # Padding with null pixels if needed
                row.append([NULL_CHAR_INDEX, NULL_CHAR_INDEX, NULL_CHAR_INDEX])
        grid.append(row)
    
    return grid


def encryption(userText):
    global key
    key = ""  # Reset key for new encryption
    print(userText)
    textSize = len(userText)
    img = textToArray(textSize, userText)
    img.save("output_image.png")
    print(f"Encryption Key: {key}")
    return key
