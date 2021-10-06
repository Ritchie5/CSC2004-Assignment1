import wave
import numpy as np


def ConvertToBin(input):  # convert data to binary function
    if type(input) == str:  # payload input
        # print("String format detected")
        return ''.join(format(ord(x), '08b') for x in input)
    elif type(input) == bytes or type(input) == np.ndarray:  # bytes input
        # print("Byte format detected")
        return
    elif type(input) == int or type(input) == np.int8:  # integer input
        # print("Integer format detected")
        return format(input, '08b')
    else:
        raise TypeError(
            "Input type not supported, please provide data in String, Bytes or Integer format")


def textEncode(payload, coverObj, bitPos):
    print(payload)
    coverObj = wave.open(coverObj, mode="rb")
    frame_bytes = bytearray(list(coverObj.readframes(coverObj.getnframes())))  # convert to byte data
    # print("OG:")
    # for i in range(0,8):
    #   print(frame_bytes[i])
    # print(frame_bytes)
    # payload = "WOOOOOOOOOOOOOOOOOO"
    payload += "#####"
    # payload = payload + int((len(frame_bytes)-(len(payload)*8*8))/8) *'#'
    # print(payload)
    # binaryPayload=ConvertToBin(payload)
    # binaryPayload=list(binaryPayload)
    # print(binaryPayload)
    binaryPayload = ConvertToBin(payload)

    counter = 0
    # frame_bytes=int(frame_bytes)
    for i in range(len(frame_bytes)):
        listBytes = list(format(frame_bytes[i], '08b'))
        for x in range(len(bitPos)):
            if counter < len(binaryPayload):
                # print(frame_bytes[i])
                print(listBytes)
                # frame_bytes[i]=int(str(format(frame_bytes[i],'08b')[:-1])+binaryPayload[counter],2)
                listBytes[bitPos[x]] = binaryPayload[counter]
                frame_bytes[i] = int("".join(listBytes), 2)
                # print(frame_bytes[i])
                counter += 1
            if counter >= len(binaryPayload):
                break
    # print("MODDED:")
    # for i in range(len(frame_bytes)):
    #    print(format(frame_bytes[i],'08b'))
    # print(frame_bytes)
    frame_modified = bytes(frame_bytes)
    # print("D")
    # for i in range(len(frame_bytes)):
    # print(format(frame_modified[i],'08b'))
    # print(frame_modified)
    newAudio = wave.open('Audio\EncodedAudio.wav', 'wb')
    newAudio.setparams(coverObj.getparams())
    newAudio.writeframes(frame_modified)
    newAudio.close()
    coverObj.close()


def textDecode(stegoObj, bitPos):
    stegoObj = wave.open(stegoObj, mode='rb')
    frame_bytes = bytearray(list(stegoObj.readframes(stegoObj.getnframes())))
    # print(frame_bytes)
    binaryPayload = ""
    for i in range(len(frame_bytes)):
        for x in range(len(bitPos)):
            # print(format(frame_bytes[i],'08b'))
            # payload+=(format(frame_bytes[i],'08b')[-1])
            binaryPayload += (format(frame_bytes[i], '08b')[bitPos[x]])
    # print(payload)
    binaryPayloadFormat = [binaryPayload[i:i + 8] for i in range(0, len(binaryPayload), 8)]
    payload = ""
    for byte in binaryPayloadFormat:
        payload += chr(int(byte, 2))
        if payload[-5:] == "#####":
            break

    text = (payload[:-5])
    file = open(r"Text\messageOutput.txt", "w")
    file.write(text)
    stegoObj.close()


# encode()
# decode()

choice = int(input("1.Encode\n2.Decode\nEnter your choice:"))
if choice == 1:
    payload = input("Enter the path of the .txt you want to hide:")
    payload = open(payload, "r")
    payload = payload.read()
    coverObj = input("Enter the path to the coverObj file you want to hide the secret message:")
    # bitPos = int(input("Enter the bit you want to encode (0-7 with 0 as the msb):"))
    bits = int(input("Bits to replace?\n"))
    bitPos = []
    for i in range(bits):
        bitPosInput = int(input("Enter bit position #" + str(i + 1) + " to replace(0-7) :\n"))
        bitPos.append(bitPosInput)
    bitPos.sort()
    textEncode(payload, coverObj, bitPos)

elif choice == 2:
    stegoObj = input("Enter the path of the coverObj file with embedded secret message:")
    # bitPos = int(input("Enter the bit position in which is was encoded in: "))
    bits = int(input("Bits to replace?\n"))
    bitPos = []
    for i in range(bits):
        bitPosInput = int(input("Enter bit position #" + str(i + 1) + " to replace(0-7) :\n"))
        bitPos.append(bitPosInput)
    bitPos.sort()
    textDecode(stegoObj, bitPos)
else:
    print("Invalid code, please restart the program!")