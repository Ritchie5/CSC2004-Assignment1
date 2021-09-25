import cv2
import numpy as np

def ConvertToBin(input):
    if type(input) == str:  # string input
        print("String format detected")
        return ''.join(format(ord(x), '08b') for x in input)
    elif type(input) == bytes or type(input) == np.ndarray:  # bytes input
        return [format(x, "08b") for x in input]
    elif type(input) == int or type(input) == np.int8:  # integer input
        return format(input, '08b')
    else:
        raise TypeError(
            "Input type not supported, please enter in String, Bytes or Integer format")


print("This program is using OpenCV " + cv2. __version__)
print("NOTE: LSB only works on lossless-compression images like PNG, TIFF, and BMP")
img = 'Lenna.png'
payload = "You will never see this message 238"
img = cv2.imread(img)
print("Image size: " + str(img.shape[0]) + " by " +
      str(img.shape[1]) + " pixels")  # image size(pixels)

# choose how many bits to replace
print(ConvertToBin(payload))



# show resulting image for comparison
'''cv2.imshow('Original Image', img)
cv2.imshow('Final Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
