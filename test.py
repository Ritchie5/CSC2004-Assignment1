import wave
import numpy as np

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

def encode():
    audio = wave.open("Audio\\okay-come-on.wav",mode="rb")
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes()))) #convert to byte data
    #print("OG:")
    #for i in range(0,8):
    #    print(format(frame_bytes[i],'08b'))
    #print(frame_bytes)
    string = "WOOOOOOOOOOOOOOOOOO"
    string +="#####"
    #string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
    #print(string)
    binarystring=ConvertToBin(string)
    #binarystring=list(binarystring)
    print(binarystring)

    counter=0
    #frame_bytes=int(frame_bytes)
    for i in range(len(frame_bytes)):
        if counter < len(binarystring):
            #print(frame_bytes[i])
            frame_bytes[i]=int(str(format(frame_bytes[i],'08b')[:-1])+binarystring[counter],2)
            #print(frame_bytes[i])
            counter+=1
        if counter>=len(binarystring):
            break
    #print("MODDED:")
    #for i in range(len(frame_bytes)):
        #print(format(frame_bytes[i],'08b'))
    #print(frame_bytes)
    frame_modified = bytes(frame_bytes)
    #print("D")
    #for i in range(len(frame_bytes)):
        #print(format(frame_modified[i],'08b'))
    #print(frame_modified)
    newAudio =  wave.open('sampleStego.wav', 'wb')
    newAudio.setparams(audio.getparams())
    newAudio.writeframes(frame_modified)
    newAudio.close()
    audio.close()

def decode():
    audio = wave.open("sampleStego.wav", mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    print(frame_bytes)
    string=""
    for i in range(len(frame_bytes)):
        #print(format(frame_bytes[i],'08b'))
        string+=(format(frame_bytes[i],'08b')[-1])
    print(string)
    binaryPayloadFormat = [string[i:i+8]
                           for i in range(0, len(string), 8)]
    payload = ""
    for byte in binaryPayloadFormat:
        payload += chr(int(byte, 2))
        if payload[-5:] == "#####":
            break
    print(payload[:-5])
    audio.close()

encode()
decode()