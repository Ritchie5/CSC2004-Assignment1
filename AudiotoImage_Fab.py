import speech_recognition as sr
import cv2
import numpy as np

# Function to convert audio to text
def audio_to_text(audioFile):
    r = sr.Recognizer()
    with sr.AudioFile(audioFile) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        # print(len(text))
    return text

# Function to convert text to binary
def text_to_binary(text):
    if type(text) == str:
        return ''.join([format(ord(i), "08b") for i in text])
    elif type(text) == bytes or type(text) == np.ndarray:
        return [format(i, "08b") for i in text]
    elif type(text) == int or type(text) == np.uint8:
        return format(text, "08b")
    else:
        raise TypeError("Input type not supported")

# Function is use to encode text using LSB algorithm
def textEncode(image, audio,bitPos):

    text = audio_to_text(audio)

    # calculate the maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8

    # Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(text) > n_bytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")

    text += "#####"  # you can use any string as the delimeter

    data_index = 0
    # Convert text to binary
    binary_secret_msg = text_to_binary(text)

    data_len = len(binary_secret_msg)  # Find the length of data that needs to be hidden
    for values in image:
        for pixel in values:
            # convert RGB values to binary format
            b, g, r = text_to_binary(pixel)
            listB=list(b)
            listG=list(g)
            listR=list(r)
            # modify the LSB only if there is still data to store
            for i in range(len(bitPos)):
                if data_index < data_len:
                    # hide the data into least significant bit of red pixel
                    #pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                    listB[bitPos[i]]=binary_secret_msg[data_index]
                    pixel[0] = int("".join(listB), 2)
                    data_index += 1
            for i in range(len(bitPos)):
                if data_index < data_len:
                    # hide the data into least significant bit of green pixel
                    #pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                    listG[bitPos[i]]=binary_secret_msg[data_index]
                    pixel[1] = int("".join(listG), 2)
                    data_index += 1
            for i in range(len(bitPos)):
                if data_index < data_len:
                    # hide the data into least significant bit of  blue pixel
                    #pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                    listR[bitPos[i]]=binary_secret_msg[data_index]
                    pixel[2] = int("".join(listR), 2)
                    data_index += 1
            # Break out of loop once finish encoded the text
            if data_index >= data_len:
                break

    cv2.imwrite("Image\EncodedImagee.png", image)

# Function to decode image to text
def textDecode(image,bitPos):
    binary_data = ""
    for values in image:
        for pixel in values:
            b, g, r = text_to_binary(pixel)  # convert the red,green and blue values into binary format
            # binary_data += b[-1]  # extracting data from the least significant bit of red pixel
            # binary_data += g[-1]  # extracting data from the least significant bit of green pixel
            # binary_data += r[-1]  # extracting data from the least significant bit of blue pixel
            for i in range(len(bitPos)):
                binary_data += b[bitPos[i]]
            for i in range(len(bitPos)):
                binary_data += g[bitPos[i]]
            for i in range(len(bitPos)):
                binary_data += r[bitPos[i]]
    # split by 8-bits
    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####":  # check if we have reached the delimeter which is "#####"
            break

    text =  decoded_data[:-5]  # remove the delimeter to show the original hidden message
    file = open(r"Text\secret_message.txt", "w")
    file.write(text)
    print(text)

# Main
choice = int(input("1.Encode\n2.Decode\nEnter your choice:"))
if choice == 1:
    audio = input("Please input audio file to encode (with extension):")
    image = input("Please input image file as cover object (with extension):")
    bits = int(input("Bits to replace?\n"))
    bitPos=[]
    for i in range(bits):
        bitPosInput = int(input("Enter bit position #"+ str(i+1)+"to replace(0-7) :\n"))
        bitPos.append(bitPosInput)
    bitPos.sort()
    image = cv2.imread(image)
    encoded_image = textEncode(image, audio, bitPos)

elif choice == 2:
    image = input("Enter the path of image with embedded secret message:")
    print("Enter in key to decode\n")
    bits=int(input("Enter number of bits replaced: "))
    bitPos=[]
    for i in range(bits):
        bitPosInput=int(input("Enter bit position #"+ str(i+1)+" replaced(0-7): "))
        bitPos.append(bitPosInput)
    bitPos.sort()
    image = cv2.imread(image)
    text = textDecode(image,bitPos)


else:
    print("Invalid code, please restart the program!")