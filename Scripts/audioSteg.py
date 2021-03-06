import numpy as np
import base64
import wave
import os


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

    # ======================================= COVER OBJECT : AUDIO (WAV) =======================================
    def get_cover_audio(self, file, itype):
        try:
            obj = wave.open(file, mode="rb")
            data = bytearray(list(obj.readframes(obj.getnframes())))  # convert to byte data
        except IOError:
            print('[!] {} file could not be opened.'.format(itype.title()))
        return obj, data

    def save_cover_audio(self, data, outfile, ori_cover_obj):
        try:
            new_audio = wave.open(outfile, 'wb')
            new_audio.setparams(ori_cover_obj.getparams())
            new_audio.writeframes(data)
            new_audio.close()
            ori_cover_obj.close()
        except IOError as e:
            raise IOError('[!] {} file could not be written.'.format(outfile) + '\n[!] {}'.format(e))
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


class Audio_Encode(LSB):
    def __init__(self, cover, secret, bits):
        print('[*] Encoding... ')
        self.cover = self.get_cover_audio(cover, 'cover')[1]
        ori_cover_obj = self.get_cover_audio(cover, 'cover')[0]
        cover_info = self.get_object_info(cover, 'cover')
        cover_size = cover_info[0]
        self.outfile = 'static\encode_output\\' + cover_info[2] + "_copy" + cover_info[1]

        self.secret = self.get_secret_object(secret, 'secret')
        secret_info = self.get_object_info(secret, 'secret')
        secret_size = secret_info[0]

        bit_pos = bits
        self.encode_to_audio(secret_size, secret_info, cover_size, ori_cover_obj, bit_pos)

    # b64 -> binary
    def to_base64(self, secret_info):
        encoded_string = base64.b64encode(self.secret)
        encoded_file_format = base64.b64encode(secret_info[1].encode('utf-8'))
        encoded_name = base64.b64encode(secret_info[2].encode('utf-8'))

        criteria = '#####'.encode('utf8')  # add stopping criteria
        result = encoded_string + criteria + encoded_file_format + criteria + encoded_name + criteria
        result = ''.join(self.to_binary(result))
        return result

    def encode_to_audio(self, secret_size, secret_info, cover_size, ori_cover_obj, bit_pos):
        data_index = 0

        print("[*] Maximum bytes to encode: ", cover_size)
        if secret_size > cover_size:
            raise ValueError("[!] Insufficient bytes, need bigger image or less data.")

        binary_secret_data = self.to_base64(secret_info)
        data_len = len(binary_secret_data)  # size of data to hide

        for i in range(len(self.cover)):
            list_bytes = list(format(self.cover[i], '08b'))
            for x in range(len(bit_pos)):
                if data_index < data_len:
                    list_bytes[bit_pos[x]] = binary_secret_data[data_index]
                    self.cover[i] = int("".join(list_bytes), 2)
                    data_index += 1
                if data_index >= len(binary_secret_data):
                    break

        self.save_cover_audio(self.cover, self.outfile, ori_cover_obj)


class Audio_Decode(LSB):
    def __init__(self, steg, bits):
        print('[*] Decoding... ')
        self.steg = self.get_cover_audio(steg, 'steg')[1]
        bit_pos = bits
        self.file_format = self.decode_from_audio(bit_pos)

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

    def decode_from_audio(self, bit_pos):
        binary_data = ""
        for i in range(len(self.steg)):
            for x in range(len(bit_pos)):
                binary_data += (format(self.steg[i], '08b')[bit_pos[x]])

        # split by 8 bits
        extracted_bin = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]

        message = self.from_base64(extracted_bin)[0]
        file_format = self.from_base64(extracted_bin)[1].decode("utf-8")
        name = self.from_base64(extracted_bin)[2].decode("utf-8")
        self.write_file(file_format, name, message)

        return name + file_format


def main():
    payload = input("Enter payload file: ")
    cover_audio = input("Enter audio file: ")

    bits = int(input("Bits to replace? "))
    bit_pos = []
    for i in range(bits):
        bitPosInput = int(input("Enter bit position #" + str(i + 1) + " to replace (0 - 7) : "))
        bit_pos.append(bitPosInput)
    bit_pos.sort()

    Audio_Encode(cover_audio, payload, bit_pos)

    steg_audio = input("Enter steg audio name: ")

    Audio_Decode(steg_audio, bit_pos)


if __name__ == '__main__':
    main()