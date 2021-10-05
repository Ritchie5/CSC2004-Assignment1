import cv2
import numpy as np
import struct


def ConvertToBin(input):  # convert data to binary function
    if type(input) == str:  # string input
        #print("String format detected")
        return ''.join(format(ord(x), '08b') for x in input)
    elif type(input) == bytes or type(input) == np.ndarray:  # bytes input
        #print("Byte format detected")
        return 
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


def DynamicEncode(imgname, payload, bitPos,payloadType):
    #print(bitPos)
    img = cv2.imread(imgname)
    #print(img)
    print("Image size: " + str(img.shape[0]) + " by " +
          str(img.shape[1]) + " pixels")  # image size(pixels)
    maxpayload = img.shape[0]*img.shape[1]*3//8
    print("Maximum payload to encode: " + str(maxpayload)+" bytes")
    # print(len(payload))
    if payloadType==1:
        payload += '#####'
        binaryPayload = ConvertToBin(payload)
        # print(binaryPayload)
    elif payloadType==2:
        f = open(imgname,'rb')
        file=f.read()
        print(file)
        #fileToString=int(file)
        fuck=list(struct.unpack("{}B".format(len(file)), file))
        #fileToString+="#####"
        print(fuck)
        data = []
        delimiter = [5,5,5,5,5,5,5,5,5,5]
        
        print(data)
        print(fuck[0])
        for i in range(len(fuck)):
            data.append(ConvertToBin(fuck[i]))
    
        for i in range(len(delimiter)):
            data.append(ConvertToBin(delimiter[i]))
        #data+=delimiter
        #print(fileToString)
        print(data)
        data="".join(data)
        binaryPayload = data
        print(binaryPayload)
        print(len(data))
        #payload=len(data)
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
            listB = list(b)
            listG = list(g)
            listR = list(r)
            for i in range(len(bitPos)):
                if index < binaryPayloadLength:
                    # print(index)
                    # print("Replacing pixel["+str(bitPos[i]) +
                    #       "] in B with " + binaryPayload[index])
                    # print("".join(listB))
                    listB[bitPos[i]] = binaryPayload[index]
                    # print("".join(listB))
                    pixel[0] = int("".join(listB), 2)
                    index += 1
                else:
                    break
            for i in range(len(bitPos)):
                if index < binaryPayloadLength:
                    # print(index)
                    # print("Replacing pixel["+str(bitPos[i]) +
                    #       "] in G with " + binaryPayload[index])
                    # print("".join(listG))
                    listG[bitPos[i]] = binaryPayload[index]
                    # print("".join(listG))
                    pixel[1] = int("".join(listG), 2)
                    index += 1
                else:
                    break
            for i in range(len(bitPos)):
                if index < binaryPayloadLength:
                    # print(index)
                    # print("Replacing pixel["+str(bitPos[i]) +
                    #       "] in R with " + binaryPayload[index])
                    # print("".join(listR))
                    listR[bitPos[i]] = binaryPayload[index]
                    # print("".join(listR))
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


def DynamicDecode(imgname, bitPos,payloadType):
    img = cv2.imread(imgname)
    
    binaryPayload = ""
    for x in img:
        for pixel in x:
            b, g, r = ConvertToBin(pixel)
            for i in range(len(bitPos)):
                binaryPayload += b[bitPos[i]]
            for i in range(len(bitPos)):
                binaryPayload += g[bitPos[i]]
            for i in range(len(bitPos)):
                binaryPayload += r[bitPos[i]]

    binaryPayloadFormat = [binaryPayload[i:i+8]
                           for i in range(0, len(binaryPayload), 8)]
    print(binaryPayloadFormat)
    
    
    #print(payload[:-5])
    if payloadType==1:
        payload = ""
        for byte in binaryPayloadFormat:
            payload += chr(int(byte, 2))
            #print(payload)
            if payload[-5:] == "#####":
                break
        print(payload[:-5])
    elif payloadType==2:
        #print(payload[:-5])
        #f=open("Decode Image.png",'wb')
        #with open("Decode.png","wb") as xdimg:
        #    xdimg.write(bytes(payload[:-5],'utf-8'))
        payload=[]
        for byte in binaryPayloadFormat:
            payload.append(int(byte,2))
            if payload[-10:]==[5,5,5,5,5,5,5,5,5,5]:
                break
        print(payload)
        f=open("dump.txt",'w')
        f.write(str(payload))
        f.close

    return payload[:-5]


def main():
    print("This program is using OpenCV " + cv2. __version__)
    print("NOTE: LSB only works on lossless-compression images like PNG, TIFF, and BMP")
    print("Main menu:\n1)Encode\n2)Decode")
    option = int(input("Enter in option\n"))
    if option == 1:
        print("Payload Type to encode\n1)Text\n2)Image")
        payloadType = int(input("Enter Payload Type(1-2):"))
        if payloadType == 1:
            print("Encoding Text in Image...")
            imgname = input("Enter image name: ")
            payload = input("Enter secret message: ")
            bits = int(input("Bits to replace?: "))
            bitPos = []
            for i in range(bits):
                bitPosInput = int(
                    input("Enter bit position #" + str(i+1)+"to replace(0-7) :\n"))
                bitPos.append(bitPosInput)
            bitPos.sort()
            # print(bitPos)
            #Encode(imgname, payload)
            DynamicEncode(imgname, payload, bitPos,payloadType)
        elif payloadType == 2:
            print("Encoding Image in Image")
            imgname = input("Enter image name(cover image): ")
            payload = input("Enter image name(to be hidden): ")
            bits = int(input("Bits to replace?: "))
            bitPos = []
            for i in range(bits):
                bitPosInput = int(
                    input("Enter bit position #" + str(i+1)+" to replace(0-7) :\n"))
                bitPos.append(bitPosInput)
            bitPos.sort()
            DynamicEncode(imgname,payload,bitPos,payloadType)
    elif option == 2:
        imgname = input("Enter image name\n")
        payloadType = int(input("Payload Type?\n1)Text\n2)Image: "))
        print("Enter in key to decode\n")
        bits = int(input("Enter number of bits replaced: "))
        bitPos = []
        for i in range(bits):
            bitPosInput = int(
                input("Enter bit position #" + str(i+1)+" replaced(0-7): "))
            bitPos.append(bitPosInput)
        bitPos.sort()
        print(bitPos)
        DynamicDecode(imgname, bitPos,payloadType)


if __name__ == "__main__":
    main()
