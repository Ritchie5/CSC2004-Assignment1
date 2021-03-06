import numpy as np
import base64
import cv2
import moviepy.video.io.ImageSequenceClip
import re
import os
from moviepy.editor import *
from PIL import Image

# For sorting of Frames
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def getframes(coverobj):                                                                    
    # Splitting of Videos into Frames
    print("\nRetriving frames from video. Please Wait...")
    frames = 0
    video_object = VideoFileClip(coverobj)
    print(coverobj)
    path = os.path.basename(coverobj)
    
    base_filename = os.path.splitext(path)[0]
    directory = "output\\" + base_filename + '_frames\\' # Returns all frames in the video object
    if not os.path.isdir(directory):    # Checks if output Directory Exists, otherwise Create It
        os.makedirs(directory)
    for index, frame in enumerate(video_object.iter_frames()):  # Saving of frames into the directory
        img = Image.fromarray(frame, 'RGB')
        img.save(f'{directory}{index}.png')
        frames += 1
    print("\nTotal number of Frames: ", frames)
    return frames

# to get the object's size, data, file_format
def get_object(file):
    try:
        file_format = os.path.splitext(file)[-1].lower()    # file format
        size = os.path.getsize(file)    # size
        with open(file, 'rb') as datafile:
            data = datafile.read()  # data
    except FileNotFoundError:
        print("\nFile to could not be found! Exiting...")
        quit()
    return data, size, file_format

# from lec slide converting to binary
def to_binary(data):
    # convert string 'data' to binary format
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    # convert bytes 'data' to binary format
    elif isinstance(data, bytes) or isinstance(data,np.ndarray):
        return [format(i, "08b") for i in data]
    # convert int 'data' to binary format
    elif isinstance(data, int) or isinstance(data,np.uint8):
        return ''.join(data, "08b")
    else:
        raise TypeError("Type not supported.")

def to_utf8_bytes(data):
    return bytes(''.join(chr(int(x, 2)) for x in data), encoding='utf8')

# data into base 64
def to_base64(object):
    # convert object into base 64
    encoded_string_payload = base64.b64encode(object[0])
    encoded_fileformat_payload = base64.b64encode(object[2].encode('utf-8'))
    criteria = '#####'.encode('utf8')   # add stopping criteria
    object_base64 = encoded_string_payload + criteria + encoded_fileformat_payload + criteria
    return object_base64

# binary -> b64
def from_base64(data):
    #print(data)1
    decoded_string = to_utf8_bytes(data)
    result = decoded_string.split('#####'.encode('utf8'))
    print(result[0])
    message = base64.b64decode(result[0])
    return message

# Encoding of payload into a single frame
def Encode(payload, coverobj, bitPos, hiddenframe):
    frame_loc = r'output\10_frames' # location of saved frames
    
    # Convert payload into base 64 then into binary
    payload_details = get_object(payload)
    payload_base64 = to_base64(payload_details)
    binary_payload = to_binary(payload_base64)

    # Select the frames for Encoding
    selected_frames = frame_loc +"\\" + str(hiddenframe) + ".png"
    image = cv2.imread(selected_frames) # Open selected frame to read its detail
    
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8  # calculate the maximum bytes to encode

    # Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(payload_details[0]) > n_bytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")

    data_index = 0
    data_len = len(binary_payload)  # Find the length of data that needs to be hidden
    
    # LSB Replacement Algorithm
    for values in image:
        for pixel in values:
            # convert RGB values to binary format
            b, g, r = to_binary(pixel)
            listB=list(b)
            listG=list(g)
            listR=list(r)
            # modify the LSB only if there is still data to store
            for i in range(len(bitPos)):
                if data_index < data_len:
                    # hide the data into least significant bit of red pixel
                    #pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                    listB[bitPos[i]] = binary_payload[data_index]
                    pixel[0] = int("".join(listB), 2)
                    data_index += 1
            for i in range(len(bitPos)):
                if data_index < data_len:
                    # hide the data into least significant bit of green pixel
                    #pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                    listG[bitPos[i]] = binary_payload[data_index]
                    pixel[1] = int("".join(listG), 2)
                    data_index += 1
            for i in range(len(bitPos)):
                if data_index < data_len:
                    # hide the data into least significant bit of  blue pixel
                    #pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                    listR[bitPos[i]] = binary_payload[data_index]
                    pixel[2] = int("".join(listR), 2)
                    data_index += 1
            # Break out of loop once finish encoded the text
            if data_index >= data_len:
                break
        
        # Saving the encoded frames as new frames
        savedframes = frame_loc +"\\" + str(hiddenframe) + ".png"
        cv2.imwrite(savedframes, image)
    
    # Sequence the frames into a video
    image_files = ['output/10_frames/' + img for img in os.listdir("Scripts/output/10_frames") if img.endswith(".png")]
    image_files.sort(key=natural_keys)
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=30)
    clip.write_videofile('steg_video.mp4')
    print("Combining Complete!")

# Decoding of payload into a single frame
def Decode(encodedvideo, bitPos, hiddenframe):
    # location of saved frames
    frame_loc = r'output\steg_video_frames' 
    selected_frames = frame_loc +"\\" + str(hiddenframe) + ".png"
    image = cv2.imread(selected_frames) # Open selected frame to read its detai
    binary_data = ""

    for values in image:
        for pixel in values:
            b, g, r = to_binary(pixel)  # convert the red,green and blue values into binary format
            #binary_data += b[-1]  # extracting data from the least significant bit of red pixel
            #binary_data += g[-1]  # extracting data from the least significant bit of green pixel
            #binary_data += r[-1]  # extracting data from the least significant bit of blue pixel
            for i in range(len(bitPos)):
                binary_data += b[bitPos[i]]
            for i in range(len(bitPos)):
                binary_data += g[bitPos[i]]
            for i in range(len(bitPos)):
                binary_data += r[bitPos[i]]
    # split by 8-bits
    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]

    #print(all_bytes)
    message = from_base64(all_bytes) 
    

    with open("Text\secret_decodemessage.txt", "w", encoding="utf-8") as f:
        f.write(message)

def main():
    # Menu
    frames = 0
    print("1: (Encode) Hide Text into Video")
    print("2: (Decode) Recover Text from Video")
    try:
        # User Selection
        start_step = int(input("\nSelect the Program to Run: "))

        if start_step == 1:
            print("Starting Program...\n")
            print("=== Hide Data in Frames ===")
            payload = input("Input payload to Hide (with extension): ")
            bits = int(input("Number of bits to replace: "))
            bitPos=[]
            for i in range(bits):
                bitPosInput = int(input("Enter bit position # "+ str(i+1)+" to replace(0-7): "))
                bitPos.append(bitPosInput)
            bitPos.sort()
            coverobj = input("Input Cover Object file (with extension): ")
            frames = getframes(coverobj)
            # Select the frames to be used
            while True:
                try:
                    print("Please Select the Frame that the Data will be Hidden At")
                    hiddenframe = int(input("Frame Number: "))
                    if hiddenframe < frames:
                        break
                    else:
                        print("\nPlease Select a Frame within the range! Please try again...")
                except ValueError:
                    print("\nInteger expected! Please try again...")
            
            Encode(payload, coverobj, bitPos, hiddenframe)

        elif start_step == 2:
            print("Starting Program...\n")
            print("=== Recover Data in Frames ===")
            encodedvideo = input("Enter the saved encoded Video (with extension):")
            frames = getframes(encodedvideo)
            print("Enter in key to decode\n")
            bits=int(input("Enter number of bits replaced: "))
            bitPos=[]
            for i in range(bits):
                bitPosInput=int(input("Enter bit position #"+ str(i+1)+" replaced(0-7): "))
                bitPos.append(bitPosInput)
            bitPos.sort()
            # Select the frames to be used
            while True:
                try:
                    print("Please Select the Frame that the Data had been Hidden At")
                    hiddenframe = int(input("Frame Number: "))
                    if hiddenframe < frames:
                        break
                    else:
                        print("\nPlease Select a Frame within the range! Please try again...")
                except ValueError:
                    print("\nInteger expected! Please try again...")
            
            Decode(encodedvideo, bitPos, hiddenframe)

        else:
            print("\nInvalid Input! Exiting...\n")
            quit()

    except KeyboardInterrupt:
	    print("\nUser canceled, exiting...")
	    quit()

if __name__ == '__main__':
    main()
