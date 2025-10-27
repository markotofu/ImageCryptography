
from PIL import Image
import numpy as np

numToLetter = [
	'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
	'1','2','3','4','5','6','7','8','9','0',
	'.',',','!','?',' ', "\n"
]

def textToArray(textSize, userText):
    width = int(textSize/3)
    if textSize % 3 != 0:
        width += 1
    arr_list = [np.zeros((3, 1)) for _ in range(width)]
    for i in range (width):
        for j in range(3):
            char_index = i * 3 + j
            if char_index < textSize:
                char = userText[char_index]
                char_num = numToLetter.index(char) if char in numToLetter else 0
                arr_list[i][j][0] = char_num
            else:
                arr_list[i][j][0] = 0
    img = Image.new('RGB', (width, 1))
    for i in range(width):
        r = int(arr_list[i][0][0])
        g = int(arr_list[i][1][0])
        b = int(arr_list[i][2][0])
        img.putpixel((i, 0), (r, g, b))
    return img

def encryption(userText):
    print(userText)
    char_count = len(userText)
    print(f"Number of characters: {char_count}")
    img = textToArray(char_count, userText)
    img.save("output_image.png")

