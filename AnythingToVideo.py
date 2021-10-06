import math
import numpy as np
import base64
import cv2
from moviepy.editor import *
from PIL import Image


# Splitting of Videos into Frames
def get_frames(coverobj):
    frames = 0
    video_object = VideoFileClip("10.mp4")
    base_filename = os.path.splitext(os.path.basename("10.mp4"))[0]
    # Returns all frames in the video object
    directory = "output\\" + base_filename + '_frames\\'
    if not os.path.isdir(directory):# Checks if output Directory Exists, otherwise Create It
        os.makedirs(directory)
    for index, frame in enumerate(video_object.iter_frames()):
        img = Image.fromarray(frame, 'RGB')
        img.save(f'{directory}{index}.png')
        frames += 1
    print("\nTotal number of Frames: ", frames)


class LSB:
    # to get the object's size, data, file_format
    def get_object(self, file, itype):
        try:
            file_format = os.path.splitext(file)[-1].lower()
            size = os.path.getsize(file)
            with open(file, 'rb') as datafile:
                data = datafile.read()
        except FileNotFoundError:
            print("\nFile to could not be found! Exiting...")
            quit()
        return data, size, file_format

    # Setting of bits to be manipulated (0 - 5)
    def set_bits(self, bits):
        self.bits = int(bits)
        if not 0 <= self.bits <= 5:
            raise ValueError('[!] Number of bits needs to be between 0 - 5.')
    
    # from lec slide
    def to_binary(self, data):
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

    def to_utf8_bytes(self, data):
        return bytes(''.join(chr(int(x, 2)) for x in data), encoding='utf8')


class Encode(LSB):
    def __init__(self, payload, coverobj, bits, frame_start, frame_end, frame_loc):
        print('[*] LSB Encoding with bits = {}'.format(bits))
        self.set_bits(bits) 
        self.start = frame_start
        self.end = frame_end
        self.payload = self.get_object(payload, 'payload') # payload details
        payload_data = self.payload[0]
        payload_size = self.payload[1]
        self.coverobj = self.get_object(coverobj, 'coverobj') # coverobj details
        coverobj_data = self.payload[0]
        coverobj_size = self.coverobj[1]
        self.frame_loc = frame_loc
        self.steg(payload_data, payload_size, coverobj_data, coverobj_size, self.start, self.end, self.frame_loc)
    
    # data into base 64 into binary
    def to_base64(self):
        # convert payload data into base 64
        encoded_string_payload = base64.b64encode(self.payload[0])
        encoded_fileformat_payload = base64.b64encode(self.payload[2].encode('utf-8'))
        # convert cover object data into base 64
        encoded_string_coverobj = base64.b64encode(self.coverobj[0])
        encoded_fileformat_coverobj = base64.b64encode(self.coverobj[2].encode('utf-8'))
        
        criteria = '#####'.encode('utf8')   # add stopping criteria
        result_payload = encoded_string_payload + criteria + encoded_fileformat_payload + criteria
        result_coverobj = encoded_string_coverobj + criteria + encoded_fileformat_coverobj + criteria
        
        # convert base 64 into binary for payload and coverobj
        binary_payload = ''.join(self.to_binary(result_payload))
        binary_coverobj = ''.join(self.to_binary(result_coverobj))
        return binary_payload, binary_coverobj

    def steg(self, payload_data, payload_size, coverobj_data, coverobj_size, start, end, frame_loc):
        print("[*] Maximum bytes to encode: ", coverobj_size)
        if payload_size > coverobj_size:
            raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
        
        binary_data = self.to_base64()
        binary_payload_data = binary_data[0]
        binary_coverobj_data = binary_data[1]

        toBeAmendedFrame = end - start + 1
        datapoints = math.ceil(len(payload_data) / toBeAmendedFrame) # Calculation of the Data distribution per Frame
        print(datapoints)
        counter = start
        print("Performing Steganography...")        
        for num in range(0, len(payload_data), datapoints): # Partition of the payload data based on the datapoints 
            selected_frames = frame_loc +"\\" + str(counter) + ".png"
            encodetext = payload_data[num:num+datapoints] # Copy the newly distributed data into a variable
            try:
                image = Image.open(selected_frames, 'r') # Open the selected frames for reading; Parameter has to be r, otherwise ValueError will occu
            except FileNotFoundError:
                print("\n%d.png not found! Exiting..." % counter)
                quit()
            newimage = image.copy() # Duplicate the Selected Frames for manipulation

            #LSB Algo here





            new_img_name = selected_frames # Frame Number
            newimage.save(new_img_name, str(new_img_name.split(".")[1].upper())) # Save as New Frame
            counter += 1
        

        #save the frames and save it as video
        images = [img for img in os.listdir("output/10_frames") if img.endswith(".png")]
        frame = cv2.imread(os.path.join("output/10_frames", images[10]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter("steg_video.avi", 0, 1, (width,height))

        for image in images:
            video.write(cv2.imread(os.path.join("output", image)))

        cv2.destroyAllWindows()
        video.release()

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
            payload = input("Input payload to Hide (inc. extension): ")
            bits = int(input("Bits to replace (0 to 5): "))
            coverobj = input("Input Cover Object file (inc. extension): ")
            get_frames(coverobj)
            while True:
                try:
                    print("Please Enter Start and End Frame where Data will be Hidden At")
                    frame_start = int(input("Start Frame: "))
                    frame_end = int(input("End Frame: "))
                    if frame_start < frame_end:
                        break
                    else:
                        print("\nStarting Frame must be larger than ending Frame! Please try again...")
                except ValueError:
                    print("\nInteger expected! Please try again...")
            frame_location = input("Frames Location: ")
            Encode(payload, coverobj, bits, frame_start, frame_end, frame_location)

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
