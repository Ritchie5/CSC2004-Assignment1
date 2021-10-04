from PIL import Image
import numpy as np
import base64
import os

class LSB:
    def set_bits(self, bits):
        self.bits = int(bits)
        if not 0 <= self.bits <= 5:
            raise ValueError('[!] Number of bits needs to be between 0 - 5.')
    
    # to get secret message object's format, size, data 
    def get_secret_object(self, file, itype):
        try:
            file_format = os.path.splitext(file)[-1].lower()
            size = os.path.getsize(file)
            with open(file, 'rb') as data:
                data = data.read()
        except IOError:
            print('[!] {} file could not be opened.'.format(itype.title()))
        return data, size, file_format
        
    def get_cover_object(self, file, itype):
        try:
            size = os.path.getsize(file)
            data = Image.open(file)
        except IOError:
            print('[!] {} file could not be opened.'.format(itype.title()))
        return data, size
    
    # image for now!!
    def save_cover_image(self, data, outfile):
        try:
            data.save(outfile)
        except IOError as e:
            raise IOError('[!] {} file could not be written.'.format(outfile) + '\n[!] {}'.format(e))
        except Exception as e:
            raise Exception('[!] Unable to save file.' + '\n[!] {}'.format(e))
    
    def write_file(self, file_format, text):
        with open('secret_message' + file_format, 'wb') as f:
            f.write(text)

    def to_binary(self, data):
        # convert 'data' to binary format as string
        if isinstance(data, str):
            return ''.join([format(ord(i), "08b") for i in data])
        elif isinstance(data, bytes) or isinstance(data,np.ndarray):
            return [format(i, "08b") for i in data]
        elif isinstance(data, int) or isinstance(data,np.uint8):
            return ''.join(data, "08b")
        else:
            raise TypeError("Type not supported.")

    def to_utf8_bytes(self, data):
        return bytes(''.join(chr(int(x, 2)) for x in data), encoding='utf8')
    
    def modify_bits(self, selected_bits, pixel, payload_bit):
        mask = 1 << selected_bits
        right_most = pixel & (mask - 1)
        result = right_most | (payload_bit << selected_bits)
        return result

    def extract_bits(self, selected_bits, pixel):
        mask = 1 >> selected_bits
        result = pixel & (mask - 1)
        result = f"{result:0{selected_bits}b}"
        return result
        
class Encode(LSB):
    def __init__(self, cover, secret, bits, outfile):
        print('[*] LSB Encoding with bits = {}'.format(bits))
        self.set_bits(bits)
        self.outfile = outfile
        self.cover = self.get_cover_object(cover, 'cover')
        self.secret = self.get_secret_object(secret, 'secret')
        secret_size = self.secret[1]
        cover_size = self.cover[1]
        self.encode_to_image(secret_size, cover_size)

    # b64 -> binary
    def to_base64(self):
        encoded_string = base64.b64encode(self.secret[0])
        encoded_file_format = base64.b64encode(self.secret[2].encode('utf-8'))
        
        criteria = '#####'.encode('utf8') # add stopping criteria
        result = encoded_string + criteria + encoded_file_format + criteria
        #print(len(result.split('#####'.encode('utf8'))))
        result = ''.join(self.to_binary(result))
        #print(result)
        return result

    def encode_to_image(self, secret_size, cover_size):
        data_index = 0

        print("[*] Maximum bytes to encode: ", cover_size)
        if secret_size > cover_size:
            raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
        print("[*] Encoding data...")

        binary_secret_data = self.to_base64()
        with self.cover[0] as img:
            width, height = img.size
            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(img.getpixel((x, y)))
                    #RGB
                    for n in range(0, 3):
                        if(data_index < len(binary_secret_data)):
                            #pixel[n] = self.modify_bits(self.bits, pixel[n], int(binary_secret_data[data_index]))
                            pixel[n] = pixel[n] & ~1 | int(binary_secret_data[data_index])
                            data_index += 1
                    img.putpixel((x, y), tuple(pixel))
            
            self.save_cover_image(img, self.outfile)

class Decode(LSB):
    def __init__(self, steg, bits):
        print('[*] LSB Decoding with bits = {}'.format(bits))
        self.set_bits(bits)
        self.steg = self.get_cover_object(steg, 'steg')
        self.decode_from_image()
    
    # binary -> b64
    def from_base64(self, data):
        split_binary = [data[i:i+8] for i in range(0,len(data),8)]
        decoded_string = self.to_utf8_bytes(split_binary)
        result = decoded_string.split('#####'.encode('utf8'))
        message = base64.b64decode(result[0])
        file_format = base64.b64decode(result[1])
        return message, file_format

    def decode_from_image(self):
        extracted_bin = []
        with self.steg[0] as img:
            width, height = img.size
            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(img.getpixel((x, y)))
                    for n in range(0, 3):
                        #bits = self.extract_bits(self.bits, pixel[n])
                        #extracted_bin.append(bits)
                        extracted_bin.append(pixel[n] & 1)
        
        data = "".join([str(x) for x in extracted_bin])
        message = self.from_base64(data)[0]
        file_format = self.from_base64(data)[1].decode("utf-8")
        self.write_file(file_format, message)

def main():
    
    payload = input("Enter payload file: ")
    image = input("Enter image file: ")
    steg_image = input("Enter steg image name: ")
    number = input("Enter the bit: ")

    Encode(image, payload, number, steg_image)
    Decode(steg_image, number)

if __name__ == '__main__':
    main()
