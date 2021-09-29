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
            "Input type not supported, please provide data in String, Bytes or Integer format")


def Encode(imgname, payload):
    img = cv2.imread(imgname)
    #img = cv2.resize(img, (50, 50))
    print("Image size: " + str(img.shape[0]) + " by " +
          str(img.shape[1]) + " pixels")  # image size(pixels)
    maxpayload = img.shape[0]*img.shape[1]*3//8
    print("Maximum payload to encode: " + str(maxpayload)+" bytes")
    # print(len(payload))
    payload += '#####'
    binaryPayload = ConvertToBin(payload)
    # print(binaryPayload)
    if len(payload) > maxpayload:
        print("Length of payload is to big for image of this size, please use a larger image or reduce the payload")
    index = 0
    binaryPayloadLength = len(binaryPayload)
    # print(binaryPayloadLength)
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

def DynamicEncode(imgname,payload,bitPos):
    print(bitPos)
    img = cv2.imread(imgname)
    print("Image size: " + str(img.shape[0]) + " by " +
          str(img.shape[1]) + " pixels")  # image size(pixels)
    maxpayload = img.shape[0]*img.shape[1]*3//8
    print("Maximum payload to encode: " + str(maxpayload)+" bytes")
    # print(len(payload))
    payload += '#####'
    binaryPayload = ConvertToBin(payload)
    # print(binaryPayload)
    if len(payload) > maxpayload:
        print("Length of payload is to big for image of this size, please use a larger image or reduce the payload")
    index = 0
    binaryPayloadLength = len(binaryPayload)
    # print(binaryPayloadLength)
    imgEncode = img
    # LSB Encoding
    for values in imgEncode:
        for pixel in values:
            b, g, r = ConvertToBin(pixel)
            listB=list(b)
            listG=list(g)
            listR=list(r)
            for i in range(len(bitPos)):
                if index < binaryPayloadLength:
                    #print(index)
                    print("Replacing pixel["+str(bitPos[i])+"] in B with "+ binaryPayload[index])
                    print("".join(listB))
                    listB[bitPos[i]]=binaryPayload[index]
                    print("".join(listB))
                    pixel[0] = int("".join(listB), 2)
                    index += 1
                else:
                   break
            for i in range(len(bitPos)):
                if index < binaryPayloadLength:
                    #print(index)
                    print("Replacing pixel["+str(bitPos[i])+"] in G with "+ binaryPayload[index])
                    print("".join(listG))
                    listG[bitPos[i]]=binaryPayload[index]
                    print("".join(listG))
                    pixel[1] = int("".join(listG), 2)
                    index += 1
                else:
                    break
            for i in range(len(bitPos)):
                if index < binaryPayloadLength:
                    #print(index)
                    print("Replacing pixel["+str(bitPos[i])+"] in R with "+ binaryPayload[index])
                    print("".join(listR))
                    listR[bitPos[i]]=binaryPayload[index]
                    print("".join(listR))
                    pixel[2] = int("".join(listR), 2)
                    index += 1
                else:
                    break
    cv2.imwrite('Encoded Image.png', imgEncode)
    return imgEncode


def Decode(imgname):
    img = cv2.imread(imgname)
    binaryPayload = ""
    for x in img:
        for pixel in x:
            b, g, r = ConvertToBin(pixel)
            binaryPayload += b[:3]
            binaryPayload += g[:3]
            binaryPayload += r[:3]

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
    print("Main menu:\n1)Encode\n2)Decode")
    option = int(input("Enter in option\n"))
    # print(option)
    if option == 1:
        print("Payload Type to encode\n1)Text\n2)Image")
        payloadType = int(input("Enter Payload Type (1-?):"))
        if payloadType == 1:
            imgname = input("Enter image name\n")
            payload = input("Enter secret message\n")
            bits = int(input("Bits to replace?\n"))
            bitPos=[]
            for i in range(bits):
                bitPosInput = int(input("Enter bit position to replace(0-7):\n"))
                bitPos.append(bitPosInput)
            bitPos.sort()
            #print(bitPos)
            #Encode(imgname, payload)
            DynamicEncode(imgname,payload,bitPos)

    elif option == 2:
        imgname = input("Enter image name\n")
        Decode(imgname)

    # Display does not with when code above is written for some reason, but code is working fine...
    # show resulting image for comparison
    #help = cv2.imread("Lenna.png")
    #cv2.imshow('Original Image', help)
    #cv2.imshow('Encoded Image', "Encoded Image.png")
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
