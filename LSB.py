import cv2
import numpy as np


def ConvertToBin(input):  # convert data to binary function
    if type(input) == str:  # string input
        #print("String format detected")
        return ''.join(format(ord(x), '08b') for x in input)
    elif type(input) == bytes or type(input) == np.ndarray:  # bytes input
        #print("Byte format detected")
        return [format(x, "08b") for x in input]
    elif type(input) == int or type(input) == np.int8:  # integer input
        #print("Integer format detected")
        return format(input, '08b')
    else:
        raise TypeError(
            "Input type not supported, please enter in String, Bytes or Integer format")


def Encode(imgname, payload):
    img = cv2.imread(imgname)
    #img = cv2.resize(img, (50, 50))
    print("Image size: " + str(img.shape[0]) + " by " +
          str(img.shape[1]) + " pixels")  # image size(pixels)
    maxpayload = img.shape[0]*img.shape[1]*3//8
    print("Maximum payload to encode: " + str(maxpayload)+" bytes")
    print(len(payload))
    payload += '#####'
    binaryPayload = ConvertToBin(payload)
    print(binaryPayload)
    if len(payload) > maxpayload:
        print("Length of payload is to big for image of this size, please use a larger image or reduce the payload")
    index = 0
    binaryPayloadLength = len(binaryPayload)
    print(binaryPayloadLength)
    imgEncode = img
    # LSB Encoding
    for values in imgEncode:
        for pixel in values:
            b, g, r = ConvertToBin(pixel)
            if index < binaryPayloadLength:
                pixel[0] = int(b[:-1] + binaryPayload[index], 2)
                index += 1
                # print(index)
                # print((pixel[0]))
            if index < binaryPayloadLength:
                pixel[1] = int(g[:-1] + binaryPayload[index], 2)
                index += 1
                # print(index)
                # print((pixel[1]))
            if index < binaryPayloadLength:
                pixel[2] = int(r[:-1] + binaryPayload[index], 2)
                index += 1
                # print(index)
                # print((pixel[2]))
            if index >= binaryPayloadLength:
                break

    cv2.imwrite('Encoded Image.png', imgEncode)
    return imgEncode


def Decode(imgname):
    img = cv2.imread(imgname)
    binaryPayload = ""
    for x in img:
        for pixel in x:
            b, g, r = ConvertToBin(pixel)
            binaryPayload += b[-1]
            binaryPayload += g[-1]
            binaryPayload += r[-1]

    binaryPayloadFormat = [binaryPayload[i:i+8]
                           for i in range(0, len(binaryPayload), 8)]
    # print(binaryPayloadFormat)
    payload = ""
    for byte in binaryPayloadFormat:
        payload += chr(int(byte, 2))
        # print(payload)
        if payload[-5:] == "#####":
            break
    print(payload[:-5])
    return payload[:-5]


def main():
    print("This program is using OpenCV " + cv2. __version__)
    print("NOTE: LSB only works on lossless-compression images like PNG, TIFF, and BMP")

    img = 'Lenna.png'
    ogimg = cv2.imread('Lenna.png')
    #payload = "Steganography is the practice of hiding a secret message inside of (or even on top of) something that is not secret. That something can be just about anything you want. These days, many examples of steganography involve embedding a secret piece of text inside of a picture. Or hiding a secret message or script inside of a Word or Excel document.  The purpose of steganography is to conceal and deceive. It is a form of covert communication and can involve the use of any medium to hide messages. It’s not a form of cryptography, because it doesn’t involve scrambling data or using a key. Instead, it is a form of data hiding and can be executed in clever ways. Where cryptography is a science that largely enables privacy, steganography is a practice that enables secrecy – and deceit."
    payload = "MY MILKSHAKE BRINGS ALL THE BOYS TO THE YARD"
    imgEncode=Encode(img, payload)
    Decode('Encoded Image.png')
    # show resulting image for comparison
    cv2.imshow('Original Image', ogimg)
    cv2.imshow('Encoded Image', imgEncode)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
