from PIL import Image
import numpy as np

numToLetter = [
	'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
	'1','2','3','4','5','6','7','8','9','0',
	'.',',','!','?',' ', "\n"
]

def imgToArray(img):
    width, height = img.size
    arr = np.zeros((width, 3), dtype=int)
    for i in range(width):
        r, g, b = img.getpixel((i, 0))
        arr[i][0] = r
        arr[i][1] = g
        arr[i][2] = b
    return arr

def decryption():
    ImagePath = "output_image.png"
    img = Image.open(ImagePath)
    arr = imgToArray(img)
    finalText =""
    for i in range(arr.shape[0]):
        for j in range(3):
            char_num = arr[i][j]
            if char_num < len(numToLetter):
                finalText += numToLetter[char_num]
    print("Decrypted Text: \n")
    print(finalText)
    