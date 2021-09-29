from typing import no_type_check


import numpy as np
import cv2


img = cv2.imread("Encoded Image.png")
count = 0
for x in img:
    for pixel in x:
        print(bin(pixel[0])[-2:])
        print(bin(pixel[1])[-2:])
        print(bin(pixel[2])[-2:])
        print("\n")
        count+=1
        if count>=10:
            break
    if count>=10:
        break
            