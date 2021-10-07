import math
import numpy as np
import base64
import cv2
import moviepy.video.io.ImageSequenceClip
import re
from moviepy.editor import *
from PIL import Image

# For sorting of Frames
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def getframes(coverobj):                                                                     # hardcoding of video (require fixing)
    # Splitting of Videos into Frames
    print("\nRetriving frames from video. Please Wait...")
    frames = 0
    video_object = VideoFileClip("10.mp4")
    base_filename = os.path.splitext(os.path.basename("10.mp4"))[0]
    directory = "output\\" + base_filename + '_frames\\' # Returns all frames in the video object
    if not os.path.isdir(directory):# Checks if output Directory Exists, otherwise Create It
        os.makedirs(directory)
    for index, frame in enumerate(video_object.iter_frames()):
        img = Image.fromarray(frame, 'RGB')
        img.save(f'{directory}{index}.png')
        frames += 1
    print("\nTotal number of Frames: ", frames)

# to get the object's size, data, file_format
def get_object(file):
    try:
        file_format = os.path.splitext(file)[-1].lower()
        size = os.path.getsize(file)
        with open(file, 'rb') as datafile:
            data = datafile.read()
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

# to modify the selected frames with input data 
def encoder (selected_newframe, encodetext, bits):
    w = selected_newframe.size[0]
    (x, y) = (0, 0) # width and height
 
    for pixel in modifyPixel(selected_newframe.getdata(), encodetext, bits):   # modify the pixel in the frame with the data
        selected_newframe.putpixel((x, y), pixel)    # Putting modified pixels in the new image
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


# Pixels modified according to encode data
def modifyPixel(pixel, encodetext, bitPos):
    datalist = to_binary(encodetext)  # Convert encoding data into 8-bit binary ASCII
    data_len = len(datalist)  # Find the length of data that needs to be hidden
    
    imagedata = iter(pixel)
    data_index = 0

    for i in range(data_len):
        # Extracts 3 pixels at a time
        pixel = [value for value in imagedata.__next__()[:3] + imagedata.__next__()[:3] + imagedata.__next__()[:3]]

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
                listB[bitPos[i]] = datalist[data_index]
                pixel[0] = int("".join(listB), 2)
                data_index += 1
        for i in range(len(bitPos)):
            if data_index < data_len:
                # hide the data into least significant bit of green pixel
                #pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                listG[bitPos[i]] = datalist[data_index]
                pixel[1] = int("".join(listG), 2)
                data_index += 1
        for i in range(len(bitPos)):
            if data_index < data_len:
                # hide the data into least significant bit of  blue pixel
                #pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                listR[bitPos[i]] = datalist[data_index]
                pixel[2] = int("".join(listR), 2)
                data_index += 1
        # Break out of loop once finish encoded the text
        if data_index >= data_len:
            break

# Encoding of payload into different frames of coverobj
def Encode(payload, coverobj, bitPos):
    getframes(coverobj)
    frame_loc = r'C:\Users\ivanc\Cyber Security Fundamentals\CSC2004-Assignment1\output\10_frames' # location of saved frames
    
    while True:
        try:
            print("Please Enter Start and End Frame where Data will be Hidden At")
            start = int(input("Start Frame: "))
            end = int(input("End Frame: "))
            if start < end:
                break
            else:
                print("\nStarting Frame must be larger than ending Frame! Please try again...")
        except ValueError:
            print("\nInteger expected! Please try again...")

    # Convert payload into base 64 then into binary
    payload_details = get_object(payload)
    payload_data = payload_details[0]
    payload_base64 = to_base64(payload_details)
    binary_payload_data = to_binary(payload_base64)
    payload_len = len(binary_payload_data)

    # Manipulate the Selected Frames (1) Determine the amt of data per frame (2) Duplicate the image
    data_len = len(binary_payload_data)  # Find the length of data that needs to be hidden
    toBeAmendedFrame = end - start + 1  # Find the total Frames to be amended
    datapoints = math.ceil(len(payload_data) / toBeAmendedFrame) # Calculation of the Data distribution per Frame
    counter = start
    for num in range(0, len(payload_data), datapoints): # Partition of the payload byte data based on the datapoints 
        selected_frames = frame_loc +"\\" + str(counter) + ".png"
        encodetext = payload_data[num:num+datapoints] # Copy the newly distributed byte data into a variable
        print ("encoded: ", len(encodetext))
        try:
            image = Image.open(selected_frames, 'r') # Open the selected frames for reading; Parameter has to be r, otherwise ValueError will occu
        except FileNotFoundError:
            print("\n%d.png not found! Exiting..." % counter)
            quit()
        selected_newframe = image.copy() # Duplicate the Selected Frames for manipulation
        encoder(selected_newframe, encodetext, bitPos) # encode each selected frame with the partitioned text data
        new_img_name = selected_frames # Frame Number
        selected_newframe.save(new_img_name, str(new_img_name.split(".")[1].upper())) # Save as New Frame
        counter += 1

    #save the frames and save it as video
    image_files = ['output/10_frames/'+ img for img in os.listdir("output/10_frames") if img.endswith(".png")]
    image_files.sort(key=natural_keys)
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=30)
    clip.write_videofile('steg_video.mp4')
    print("Combining Complete!")


def main():
    # Menu
    print("1: (Encode) Hide Text into Video")
    print("2: (Decode) Recover Text from Video")
    try:
        # User Selection
        start_step = int(input("\nSelect the Program to Run: "))

        if start_step == 1:
            print("Starting Program...\n")
            print("=== Hide Data in Frames ===")
            payload = r'C:\Users\ivanc\Cyber Security Fundamentals\CSC2004-Assignment1\Text\Text.txt' #input("Input payload to Hide (inc. extension): ")
            bits = int(input("Number of bits to replace: "))
            bitPos=[]
            for i in range(bits):
                bitPosInput = int(input("Enter bit position # "+ str(i+1)+" to replace(0-7): "))
                bitPos.append(bitPosInput)
            bitPos.sort()
            coverobj = r'C:\Users\ivanc\Cyber Security Fundamentals\CSC2004-Assignment1\10.mp4'#input("Input Cover Object file (inc. extension): ")
            Encode(payload, coverobj, bitPos)

        elif start_step == 2:
            print("Starting Program...\n")
            print("=== Recover Data in Frames ===")
            pass

        else:
            print("\nInvalid Input! Exiting...\n")
            quit()
    except ValueError:
        print("Non-Integer Input Entered. Exiting...\n")
    except KeyboardInterrupt:
	    print("\nUser canceled, exiting...")
	    quit()

if __name__ == '__main__':
    main()
