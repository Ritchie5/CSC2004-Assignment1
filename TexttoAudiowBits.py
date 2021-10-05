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
    print(payload)
    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in payload])))
    print(bits)
    # Embed according to bits position
    if bitPos == 0:
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 127) | (bit<<7)
    elif bitPos == 1:
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 191) | (bit<<6)
    elif bitPos == 2:
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 223) | (bit<<5)
    elif bitPos == 3:
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 239) | (bit<<4)
    elif bitPos == 4:
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 247) | (bit<<3)
    elif bitPos == 5:
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 251) | (bit<<2)
    elif bitPos == 6:
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 253) | (bit<<1)
    # LSB Algorithm
    # Replace LSB of each byte of audio from text
    elif bitPos == 7:
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit

    # Get modified bytes
    frame_modified = bytes(frame_bytes)

    # Write byte to new audio file
    embedded_file = input("Enter the path you want to save the embedded audio: ")
    with wave.open(embedded_file, 'wb') as fd:
        fd.setparams(coverObj.getparams())
        fd.writeframes(frame_modified)

    print("Done encoding! You may retrieve your encoded audio file in " + embedded_file)

# Function to decode text from audio
def textDecode(stegoObj, bitPos):
    # Open stego audio file
    stegoObj = wave.open(stegoObj, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(stegoObj.readframes(stegoObj.getnframes())))

    if bitPos == 0:
        extracted = [(frame_bytes[i] >> 7) & 1 for i in range(len(frame_bytes))]
    elif bitPos == 1:
        extracted = [(frame_bytes[i] >> 6) & 1 for i in range(len(frame_bytes))]
    elif bitPos == 2:
        extracted = [(frame_bytes[i] >> 5) & 1 for i in range(len(frame_bytes))]
    elif bitPos == 3:
        extracted = [(frame_bytes[i] >> 4) & 1 for i in range(len(frame_bytes))]
    elif bitPos == 4:
        extracted = [(frame_bytes[i] >> 3) & 1 for i in range(len(frame_bytes))]
    elif bitPos == 5:
        extracted = [(frame_bytes[i] >> 2) & 1 for i in range(len(frame_bytes))]
    elif bitPos == 6:
        extracted = [(frame_bytes[i] >> 1) & 1 for i in range(len(frame_bytes))]
    elif bitPos == 7:
        # Extract LSB of each byte
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    # Convert byte array back to string
    payload = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    # Remove filler characters
    payload = payload.split("###")[0]

    # Retrieve secret message
    output = print("The secret message is: " + payload)
    return output


choice = int(input("1.Encode\n2.Decode\nEnter your choice:"))
if choice == 1:
    payload = input("Enter the secret message you want to hide:")
    coverObj = input("Enter the path to the audio file you want to hide the secret message:")
    bitPos = int(input("Enter the bit you want to encode (0-7 with 0 as the msb):"))
    textEncode(payload, coverObj, bitPos)

elif choice == 2:
    stegoObj = input("Enter the path of the audio file with embedded secret message:")
    bitPos = int(input("Enter the bit position in which is was encoded in: "))
    textDecode(stegoObj,bitPos)
else:
    print("Invalid code, please restart the program!")