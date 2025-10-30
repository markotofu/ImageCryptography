from PIL import Image
import numpy as np

numToLetter = [
	'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
	'0','1','2','3','4','5','6','7','8','9',
	' ','.',',','!','?',';',':','\'','"','-','(',')',
	'[',']','{','}','@','#','$','/','\\','&','*','+','=','_','%','<','>','\n'
]

def imgToArray(img):
    width, height = img.size
    total_pixels = width * height
    arr = np.zeros((total_pixels, 3), dtype=int)
    
    pixel_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            arr[pixel_index][0] = r
            arr[pixel_index][1] = g
            arr[pixel_index][2] = b
            pixel_index += 1
    
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
    