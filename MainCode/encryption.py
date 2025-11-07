
from PIL import Image
import numpy as np
import random

key = ""
numToLetter = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8','9',
    ' ','.',',','!','?',';',':','"','-','(',')','<','>','{','}'
    '@','#','$','&','*','+','=','_','%','\n','þ'
]
NULL_CHAR_INDEX = len(numToLetter) - 1  # Index 59: 'þ' (our null character)


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
                char = userText[i].lower()  # Convert to lowercase
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
    inputArray= dummyPixelGenerator(inputArray)
    inputArray= arrayToGrid(inputArray)
    
    # Apply matrix obfuscation multiple times (randomly 2-5 times)
    num_matrix_rounds = random.randint(2, 5)
    for i in range(num_matrix_rounds):
        inputArray= matrixObfuscation(inputArray)
    
    # # Apply determinant-based cascading transformation
    # inputArray = detMultiplier(inputArray)

    return inputArray

def matrixObfuscation(grid):
    """Apply reversible 3x3 matrix transformation using modular arithmetic (mod 256)
    Expects grid format: list of rows, each row contains pixels"""
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
    
    # Process grid format: list of rows, each row contains pixels
    transformedGrid = []
    for row in grid:
        transformedRow = []
        for pixel in row:
            pixel_vec = np.array(pixel, dtype=int)
            transformed = np.dot(M, pixel_vec) % 256
            transformedRow.append(transformed.tolist())
        transformedGrid.append(transformedRow)
    
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
    
    return transformedGrid

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
    Cascading determinant multiplication:
    1. Pick random position in second row (skip top row)
    2. Calculate determinant from 3 consecutive pixels
    3. Multiply first pixel by determinant
    4. Shift window: use the modified pixel and next 2 pixels to calculate new determinant
    5. Continue multiplying each subsequent pixel until end of array
    Note: Top row (row 0) is NOT affected
    """
    global key
    width = len(grid[0]) if len(grid) > 0 else 0
    
    # Pick a random starting position in the SECOND row (skip top row)
    if width <= 3:
        randomPos = 1
    else:
        randomPos = random.randint(1, width - 2)
    
    # Store the random position in the key
    command = f"4m{randomPos}"
    key += command
    
    # Save top row unchanged
    topRow = grid[0][:]
    
    # Flatten grid EXCLUDING the first row
    allPixels = []
    for rowIdx in range(1, len(grid)):  # Start from row 1, skip row 0
        for pixel in grid[rowIdx]:
            allPixels.append(pixel)
    
    # Calculate starting index in the data rows (not including top row)
    startIndex = randomPos
    
    # Get initial three pixels for first determinant
    if startIndex >= len(allPixels) - 2 or len(allPixels) < 3:
        # Not enough pixels, return unchanged
        return grid
    
    pixelLeft = allPixels[startIndex - 1]
    pixelCenter = allPixels[startIndex]
    pixelRight = allPixels[startIndex + 1]
    
    # Process each pixel from startIndex to end
    currentIndex = startIndex
    
    while currentIndex < len(allPixels):
        # Create 3x3 matrix from current window
        matrix = np.array([
            pixelLeft,
            pixelCenter,
            pixelRight
        ])
        
        # Calculate determinant
        det = int(np.linalg.det(matrix))
        
        # Use determinant for transformation
        multiplier = (abs(det) % 3) + 1  # 1, 2, or 3
        addValue = (abs(det) % 127) + 1   # 1 to 127 (keep it moderate)
        
        # Transform pixel: add, multiply, subtract
        transformed = []
        for i in range(3):
            val = pixelLeft[i]
            val = (val + addValue) % 256      # Add to avoid zeros
            val = (val * multiplier) % 256     # Multiply by small multiplier
            val = (val - addValue) % 256      # Subtract for extra obfuscation
            transformed.append(val)
        
        allPixels[currentIndex - 1] = transformed
        
        # Shift the window: left becomes the modified pixel
        pixelLeft = transformed
        pixelCenter = pixelRight
        
        # Move to next pixel
        currentIndex += 1
        
        # Get next right pixel if available
        if currentIndex + 1 < len(allPixels):
            pixelRight = allPixels[currentIndex + 1]
        else:
            # Last pixel - transform it with current window
            if currentIndex < len(allPixels):
                matrix = np.array([pixelLeft, pixelCenter, [0, 0, 0]])
                det = int(np.linalg.det(matrix))
                multiplier = (abs(det) % 3) + 1
                addValue = (abs(det) % 127) + 1
                
                transformed = []
                for i in range(3):
                    val = pixelCenter[i]
                    val = (val + addValue) % 256
                    val = (val * multiplier) % 256
                    val = (val - addValue) % 256
                    transformed.append(val)
                
                allPixels[currentIndex] = transformed
            break
    
    # Reconstruct grid: top row unchanged, then modified data rows
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    newGrid = [topRow]  # Start with unchanged top row
    
    # Rebuild data rows from modified pixels
    pixelIndex = 0
    for y in range(1, height):  # Start from row 1
        row = []
        for x in range(width):
            if pixelIndex < len(allPixels):
                row.append(allPixels[pixelIndex])
                pixelIndex += 1
        newGrid.append(row)
    
    return newGrid

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
