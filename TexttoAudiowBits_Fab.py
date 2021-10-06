# This code allows to hide secret text in audio file using bits replacement.
# The user is allow to choose any bits he want to hide (eg hide in LSB choose 7, msb choose 0 and so on)
import wave #to read wave audio file

# Function to encode text in audio
def textEncode(payload, coverObj, bitPos):
    # Open audio and read file
    coverObj = wave.open(coverObj, mode = 'rb')
    # Read frame and convert them to byte array
    frame_bytes = bytearray(list(coverObj.readframes(coverObj.getnframes())))

    # Raise error if audio file is too small
    if len(payload) > len(frame_bytes) :
        raise ValueError("Error encounter insufficient bytes, need shorter text or bigger audio file")

    # Append dummy data to fill up rest of the bytes
    payload += int((len(frame_bytes)-(len(payload)*8*8))/8) *'#'
    #print(payload)
    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in payload])))
    #print(bits)
    # Embed according to bits position
    for i, bit in enumerate(bits):
        for x in range(len(bitPos)):
            print("Replacing bit: "+str(bitPos[x])+" of "+format(frame_bytes[i],'08b')+" with "+str(bits[i]))
            if bitPos[x] == 0:
                frame_bytes[i] = (frame_bytes[i] & 127) | (bit<<7)
            elif bitPos[x] == 1:
                frame_bytes[i] = (frame_bytes[i] & 191) | (bit<<6)
            elif bitPos[x] == 2:
                frame_bytes[i] = (frame_bytes[i] & 223) | (bit<<5)
            elif bitPos[x] == 3:
                frame_bytes[i] = (frame_bytes[i] & 239) | (bit<<4)
            elif bitPos[x] == 4:
                frame_bytes[i] = (frame_bytes[i] & 247) | (bit<<3)
            elif bitPos[x] == 5:
                frame_bytes[i] = (frame_bytes[i] & 251) | (bit<<2)
            elif bitPos[x] == 6:
                frame_bytes[i] = (frame_bytes[i] & 253) | (bit<<1)
            elif bitPos[x] == 7:
                frame_bytes[i] = (frame_bytes[i] & 254) | bit
            print(format(frame_bytes[i],'08b'))

    # Get modified bytes
    frame_modified = bytes(frame_bytes)

    # Write byte to new audio file
    with wave.open("Audio\EncodedAudio.wav", 'wb') as fd:
        fd.setparams(coverObj.getparams())
        fd.writeframes(frame_modified)

    print("Done encoding! You may retrieve your encoded audio file in Audio\EncodedAudio.wav")

# Function to decode text from audio
def textDecode(stegoObj, bitPos):
    # Open stego audio file
    stegoObj = wave.open(stegoObj, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(stegoObj.readframes(stegoObj.getnframes())))
    extracted=''
    for i in range(len(frame_bytes)):
        for x in range(len(bitPos)):
            if bitPos[x] == 0:
                #print((frame_bytes[i] >> 7) & 1)
                extracted += str((frame_bytes[i] >> 7) & 1)
            elif bitPos[x] == 1:
                extracted += str((frame_bytes[i] >> 6) & 1)
            elif bitPos[x] == 2:
                extracted += str((frame_bytes[i] >> 5) & 1)
            elif bitPos[x] == 3:
                extracted += str((frame_bytes[i] >> 4) & 1)
            elif bitPos[x] == 4:
                extracted += str((frame_bytes[i] >> 3) & 1)
            elif bitPos[x] == 5:
                extracted += str((frame_bytes[i] >> 2) & 1)
            elif bitPos[x] == 6:
                extracted += str((frame_bytes[i] >> 1) & 1)
            elif bitPos[x] == 7:
                extracted += str(frame_bytes[i] & 1)
    #print(extracted)
    # Convert byte array back to string
    payload = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    # Remove filler characters
    payload = payload.split("###")[0]

    # Retrieve secret message
    output = print("The secret message is: " + payload)
    file =  open(r"Text\messageOutput.txt", "w")
    file.write(payload)
    return output


choice = int(input("1.Encode\n2.Decode\nEnter your choice:"))
if choice == 1:
    payload = input("Enter the path of the .txt you want to hide:")
    payload = open(payload, "r")
    payload = payload.read()
    coverObj = input("Enter the path to the audio file you want to hide the secret message:")
    #bitPos = int(input("Enter the bit you want to encode (0-7 with 0 as the msb):"))
    bits = int(input("Bits to replace?\n"))
    bitPos=[]
    for i in range(bits):
        bitPosInput = int(input("Enter bit position #"+ str(i+1)+" to replace(0-7) :\n"))
        bitPos.append(bitPosInput)
    bitPos.sort()
    textEncode(payload, coverObj, bitPos)

elif choice == 2:
    stegoObj = input("Enter the path of the audio file with embedded secret message:")
    # bitPos = int(input("Enter the bit position in which is was encoded in: "))
    bits = int(input("Bits to replace?\n"))
    bitPos=[]
    for i in range(bits):
        bitPosInput = int(input("Enter bit position #"+ str(i+1)+" to replace(0-7) :\n"))
        bitPos.append(bitPosInput)
    bitPos.sort()
    textDecode(stegoObj,bitPos)
else:
    print("Invalid code, please restart the program!")