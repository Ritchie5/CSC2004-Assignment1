import numpy as np
import base64
import glob
import cv2
import os
import re


class LSB:
    # to get object's format, size, data
    def get_object_info(self, file, itype):
        try:
            file_format = os.path.splitext(file)[-1].lower()
            size = os.path.getsize(file)
            name = os.path.basename(file)
            name = name.replace(file_format, '')
        except IOError:
            print('[!] {} file could not be opened.'.format(itype.title()))
        return size, file_format, name

    def get_secret_object(self, file, itype):
        try:
            with open(file, 'rb') as data:
                data = data.read()
        except IOError:
            print('[!] {} file could not be opened.'.format(itype.title()))
        return data

    def write_file(self, file_format, name, text):
        with open('static\decode_output\\' + name + '_secret' + file_format, 'wb') as f:
            f.write(text)

    # ========================================== COVER OBJECT : VIDEO ==========================================
    def get_cover_video(self, file, itype):
        try:
            vidcap = cv2.VideoCapture(file)
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            success, image = vidcap.read()
            count = 1
            # splice video to frames
            while success:
                cv2.imwrite("output/frames/%d.png" % count, image)
                success, image = vidcap.read()
                count += 1
        except IOError:
            print('[!] {} file could not be opened.'.format(itype.title()))
        return fps

    def get_video_image(self, file, itype):
        try:
            data = cv2.imread(file)
        except IOError:
            print('[!] {} file could not be opened.'.format(itype.title()))
        return data

    def save_video_image(self, data, outfile):
        try:
            cv2.imwrite(outfile, data)
        except IOError as e:
            raise IOError('[!] {} file could not be written.'.format(
                outfile) + '\n[!] {}'.format(e))
        except Exception as e:
            raise Exception('[!] Unable to save file.' + '\n[!] {}'.format(e))

    # =============================================== CONVERTING ===============================================
    # convert 'data' to binary format as string
    def to_binary(self, data):
        if isinstance(data, str):
            return ''.join([format(ord(i), "08b") for i in data])
        elif isinstance(data, bytes) or isinstance(data, np.ndarray):
            return [format(i, "08b") for i in data]
        elif isinstance(data, int) or isinstance(data, np.uint8):
            return ''.join(data, "08b")
        else:
            raise TypeError("Type not supported.")

    # convert binary into 'data'
    def to_utf8_bytes(self, data):
        return bytes(''.join(chr(int(x, 2)) for x in data), encoding='utf8')

    # ================================================== SORTING ==================================================
    def numerical_sort(self, value):
        numbers = re.compile(r'(\d+)')
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts

    def file_directory(self):
        files = glob.glob('output/frames/*')
        return files


class Video_Encode(LSB):
    def __init__(self, cover, secret, bits, frame_no):
        print('[*] Encoding... ')

<<<<<<< HEAD
=======
        # check if frame directory is empty
        files = glob.glob('output/frames/*')
        if len(files) == 0:
            print("empty, carry on")
        else:
            print("not empty, deleting all files")
            for f in files:
                os.remove(f)

>>>>>>> fae10efb9505cd451862415b0eedc84fa702c9ad
        self.fps = self.get_cover_video(cover, 'cover')
        self.image = self.get_video_image("output/frames/%d.png" % frame_no, 'image')
        cover_info = self.get_object_info(cover, 'cover')
        cover_size = cover_info[0]
        self.outfile = 'static\encode_output\\' + cover_info[2] + "_copy.avi"
        self.display_outfile = 'static\encode_output\\' + cover_info[2] + "_display" + cover_info[1]

        self.secret = self.get_secret_object(secret, 'secret')
        secret_info = self.get_object_info(secret, 'secret')
        secret_size = secret_info[0]

        self.length = self.file_directory()
        self.frame_size = secret_size

        bit_pos = bits
        self.encode_to_image(secret_size, secret_info, cover_size, bit_pos, frame_no)

        # check if frame directory is empty
        files = glob.glob('output/frames/*')
        if len(files) == 0:
            print("empty, carry on")
        else:
            print("not empty, deleting all files")
            for f in files:
                os.remove(f)

    def __len__(self):
        return len(self.length)

    def __int__(self):
        return self.frame_size

    # b64 -> binary
    def to_base64(self, secret_info):
        encoded_string = base64.b64encode(self.secret)
        encoded_file_format = base64.b64encode(secret_info[1].encode('utf-8'))
        encoded_name = base64.b64encode(secret_info[2].encode('utf-8'))

        criteria = '#####'.encode('utf8')  # add stopping criteria
        result = encoded_string + criteria + \
                 encoded_file_format + criteria + encoded_name + criteria
        result = ''.join(self.to_binary(result))
        return result

    def encode_to_image(self, secret_size, secret_info, cover_size, bit_pos, frame_no):
        data_index = 0

        print("[*] Maximum bytes to encode: ", cover_size)
        if secret_size > cover_size:
            raise ValueError(
                "[!] Insufficient bytes, need bigger image or less data.")

        binary_secret_data = self.to_base64(secret_info)
        data_len = len(binary_secret_data)  # size of data to hide
        for row in self.image:
            for pixel in row:
                # convert RGB values to binary format
                r, g, b = self.to_binary(pixel)
                list_r = list(r)
                list_g = list(g)
                list_b = list(b)
                for i in range(len(bit_pos)):
                    if data_index < data_len:  # modify the least significant bit only if there is still data to store
                        # least significant red pixel bit
                        list_r[bit_pos[i]] = binary_secret_data[data_index]
                        pixel[0] = int("".join(list_r), 2)
                        data_index += 1
                    else:
                        break
                for i in range(len(bit_pos)):
                    if data_index < data_len:
                        # least significant green pixel bit
                        list_g[bit_pos[i]] = binary_secret_data[data_index]
                        pixel[1] = int("".join(list_g), 2)
                        data_index += 1
                    else:
                        break
                for i in range(len(bit_pos)):
                    if data_index < data_len:
                        # least significant blue pixel bit
                        list_b[bit_pos[i]] = binary_secret_data[data_index]
                        pixel[2] = int("".join(list_b), 2)
                        data_index += 1
                    else:
                        break

        self.save_video_image(self.image, "output/frames/%d.png" % frame_no)  # overwrite frame with encoded frame

        # stiches frames to video
        img_array = []

        for filename in sorted(glob.glob("output/frames/*.png"), key=self.numerical_sort):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)

        out = cv2.VideoWriter(self.outfile, cv2.VideoWriter_fourcc(*'RGBA'), self.fps, size)
        display = cv2.VideoWriter(self.display_outfile, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, size)
<<<<<<< HEAD

=======
        
>>>>>>> fae10efb9505cd451862415b0eedc84fa702c9ad
        for i in range(len(img_array)):
            out.write(img_array[i])
            display.write(img_array[i])
        out.release()
        display.release()


class Video_Decode(LSB):
    def __init__(self, steg, bits, frame_no):
        print('[*] Decoding... ')
<<<<<<< HEAD

        steg_info = self.get_object_info(steg, 'info')
        steg_name = 'static\encode_output\\' + steg_info[2].replace('_display', '_copy') + '.avi'

=======

        # check if frame directory is empty
        files = glob.glob('output/frames/*')
        if len(files) == 0:
            print("empty, carry on")
        else:
            print("not empty, deleting all files")
            for f in files:
                os.remove(f)

        steg_info = self.get_object_info(steg, 'info')
        steg_name = 'static\encode_output\\' + steg_info[2].replace('_display', '_copy') + '.avi'
        
>>>>>>> fae10efb9505cd451862415b0eedc84fa702c9ad
        self.fps = self.get_cover_video(steg_name, 'cover')
        self.steg = self.get_video_image("output/frames/%d.png" % frame_no, 'steg')
        bit_pos = bits
        self.file_format = self.decode_from_image(bit_pos)

        # check if frame directory is empty
        files = glob.glob('output/frames/*')
        if len(files) == 0:
            print("empty, carry on")
        else:
            print("not empty, deleting all files")
            for f in files:
                os.remove(f)

    def __str__(self):
        return str(self.file_format)

    # binary -> b64
    def from_base64(self, data):
        decoded_string = self.to_utf8_bytes(data)
        result = decoded_string.split('#####'.encode('utf8'))
        message = base64.b64decode(result[0])
        file_format = base64.b64decode(result[1])
        name = base64.b64decode(result[2])
        return message, file_format, name

    def decode_from_image(self, bit_pos):
        binary_data = ""
        for row in self.steg:
            for pixel in row:
                r, g, b = self.to_binary(pixel)
                for i in range(len(bit_pos)):
                    binary_data += r[bit_pos[i]]
                for i in range(len(bit_pos)):
                    binary_data += g[bit_pos[i]]
                for i in range(len(bit_pos)):
                    binary_data += b[bit_pos[i]]

        # split by 8 bits
        extracted_bin = [binary_data[i: i + 8]
                         for i in range(0, len(binary_data), 8)]

        message = self.from_base64(extracted_bin)[0]
        file_format = self.from_base64(extracted_bin)[1].decode("utf-8")
        name = self.from_base64(extracted_bin)[2].decode("utf-8")
        self.write_file(file_format, name, message)

        return name + file_format


def main():
    payload = input("Enter payload file: ")
    input_videoname = input("Enter in video name for encoding: ")

    bits = int(input("Bits to replace? "))
    bit_pos = []
    for i in range(bits):
        bitPosInput = int(input("Enter bit position #" + str(i + 1) + " to replace (0 - 7) : "))
        bit_pos.append(bitPosInput)
    bit_pos.sort()

    frame_no = int(input("Frame #: "))

    video = Video_Encode(input_videoname, payload, bit_pos, frame_no)

    print(video.__len__())
    print(video.__int__())

    output_videoname = input("Enter in video name for decoding: ")

    Video_Decode(output_videoname, bit_pos, frame_no)


if __name__ == '__main__':
    main()
