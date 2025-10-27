
from PIL import Image
import numpy as np

numToLetter = [
	'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
	'1','2','3','4','5','6','7','8','9','0',
	'.',',','!','?',' ', "-","\n"
]

def textToArray(textSize, userText):
    total_pixels = int(textSize / 3)
    if textSize % 3 != 0:
        total_pixels += 1
    width = int(np.sqrt(total_pixels))
    height = int(np.ceil(total_pixels / width))

    arr_list = [np.zeros((3, 1)) for _ in range(total_pixels)]

    for i in range(total_pixels):
        for j in range(3):
            char_index = i * 3 + j
            if char_index < textSize:
                char = userText[char_index]
                char_num = numToLetter.index(char) if char in numToLetter else 0
                arr_list[i][j][0] = char_num
            else:
                arr_list[i][j][0] = 0

    img = Image.new('RGB', (width, height))
    
    pixel_index = 0
    for y in range(height):
        for x in range(width):
            if pixel_index < total_pixels:
                r = int(arr_list[pixel_index][0][0])
                g = int(arr_list[pixel_index][1][0])
                b = int(arr_list[pixel_index][2][0])
                img.putpixel((x, y), (r, g, b))
                pixel_index += 1
            else:
                img.putpixel((x, y), (0, 0, 0))
    
    return img

def encryption(userText):
    print(userText)
    char_count = len(userText)
    print(f"Number of characters: {char_count}")
    img = textToArray(char_count, userText)
    img.save("output_image.png")

