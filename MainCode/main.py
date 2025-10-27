from PIL import Image
import numpy as np
import encryption
import decryption
mode = None
status = True
while(status):
    print("Input mode desired to be used \n 1. For Text to Image Generation \n 2. For Image decryption") 
    mode =input()
    if(mode == "1"):
        print("\nText to Image Generation Mode Chosen\n")
        
        textOrImage=input("Would you like to input text via (1) Direct Input or (2) Input File? ")
        
        if textOrImage =="1":
            text = input("Enter the text to convert to image: ")
            encryption.encryption(text)
        elif textOrImage =="2":
            file_path = "MainCode/testText"
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            encryption.encryption(text)
        status = False
    elif (mode =="2"):
        print("\nImage Decoder Mode Chosen\n")
        decryption.decryption()
        status = False
    else:
        print("Invalid input, please try again\n")
        continue
