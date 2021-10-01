import wave #to read wave audio file

#function to encode text in audio
def textEncode(payload, coverObj):
    #open audio and read file
    coverObj = wave.open(coverObj, mode = 'rb')
    #read frame and convert them to byte array
    frame_bytes = bytearray(list(coverObj.readframes(coverObj.getnframes())))

    #append dummy data to fill up rest of the bytes
    payload += int((len(frame_bytes)-(len(payload)*8*8))/8) *'#'
    #convert test to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in payload])))
    # LSB Algorithm
    # Replace LSB of each byte of audio from text
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    #Get modified bytes
    frame_modified = bytes(frame_bytes)

    #write byte to new audio file
    with wave.open("StegoAudio/stego.wav", 'wb') as fd:
        fd.setparams(coverObj.getparams())
        fd.writeframes(frame_modified)

    print("Done encoding! You may retrieve your encoded audio file in StegoAudio")

# function to decode text from audio
def textDecode(stegoObj):
    #open stego audio file
    stegoObj = wave.open(stegoObj, mode='rb')
    #convert audio to byte array
    frame_bytes = bytearray(list(stegoObj.readframes(stegoObj.getnframes())))

    #extract LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    #convert byte array back to string
    payload = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    #remove filler characters
    payload = payload.split("###")[0]

    #retrieve secret message
    output = print("The secret message is: " + payload)
    return output


choice = int(input("\n1.Encode\n2.Decode\nEnter your choice:"))
if choice == 1:
    payload = input("Enter the secret message you want to hide:")
    coverObj = input("Enter the path to the audio file you want to hide the secret message:")
    textEncode(payload, coverObj)
if choice == 2:
    stegoObj = input("Enter the path of the audio file with embedded secret message:")
    textDecode(stegoObj)
else:
    print("Invalid code, please restart the program!")