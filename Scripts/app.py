# Import for GUI
from flask import Flask, flash, render_template, request, url_for  # import flask class and relevant libraries
from flask_dropzone import Dropzone  # import flask dropzone
from werkzeug.utils import redirect
import os

# Import from Group mates
from hash import hash1
from audioSteg import Audio_Encode, Audio_Decode
from imageSteg import Img_Encode, Img_Decode
from speechRecognition import audio_to_text

# Global variables
Filepath_Cover_Object = ""
File_Cover_Object = ""
Cover_Object_Extension = ""

Filepath_Payload = ""
File_Payload = ""
Payload_Extension = ""

Charmander = "static/uploads/charmander.jpg"
Pikachu = "static/uploads/pikachu.png"

# Configure FLASK
app = Flask(__name__)  # create an instance and initialise the flask
app.secret_key = "Charmander"

# configure the setting of the uploaded item
app.config.update(
    UPLOADED_PATH='static\\uploads',  # storing of uploaded item into specified filepath
    # Flask-Dropzone config:
    DROPZONE_MAX_FILE_SIZE=1024,  # set max size limit to a large number, here is 1024 MB
    DROPZONE_TIMEOUT=5 * 60 * 1000  # set upload timeout to a large number, here is 5 minutes
)

dropzone = Dropzone(app)

app.config['DROPZONE_MAX_FILES'] = 1  # Set Max amount of file user can input to 1
app.config['DROPZONE_MAX_FILE_SIZE'] = 100  # Set Max allowed file size to 100mb
app.config['DROPZONE_DEFAULT_MESSAGE'] = "Drop / Click to Upload File"  # Set default message in box


# FLASK Routes
@app.route('/')  # provide Flask an URL on which function to be triggered (root)
def home():
    # indicate which html file to render
    return render_template('encode.html', charmander=Pikachu)


@app.route('/encode', methods=['POST', 'GET'])
def encode():
    global File_Cover_Object
    global Cover_Object_Extension
    global Filepath_Cover_Object
    global File_Payload
    global Payload_Extension

    if request.method == 'POST':

        if request.form.getlist('LSB'):
            LSB_bits = request.form.getlist('LSB')
            LSB_bits = [int(numbers) for numbers in LSB_bits]
            speech_recognition = request.form['speech_recognition']

            # Check File Extension
            ext = detect_file_type(Cover_Object_Extension)
            ext1 = detect_file_type(Payload_Extension)

            # Error checking for correct file format
            if ext == "" or ext1 == "" or ext == "video" or ext == "text":
                flash('Please input correct file format')
                return render_template('encode.html', charmander=Charmander)

            # Error checking if payload file size is too big
            Cover_object_size = os.path.getsize(Filepath_Cover_Object)
            Payload_size = os.path.getsize(Filepath_Payload)
            if Cover_object_size < Payload_size:
                flash('Payload too large for selected cover object')
                return render_template('encode.html', charmander=Charmander)

            if (Cover_object_size / 8) * len(LSB_bits) < Payload_size:
                flash('Payload too large, please add more bit for replacement')
                return render_template('encode.html', charmander=Charmander)

            Hash1 = hash1(Filepath_Cover_Object)
            Hash1 = "Hash: " + Hash1
            Hash2 = hash1(Filepath_Payload)
            Hash2 = "Hash: " + Hash2

            # CHECK THE FILE EXTENSION AND EXECUTE ACCORDINGLY
            # if ext == 'text':
            #  return render_template(
            # 'output.html', Original_Document=File_Cover_Object, Stegoed_Document=File_Cover_Object,
            # charmander=Charmander, Hash1=Hash1, Hash2=Hash2)

            if ext == 'img':
                Img_Encode(Filepath_Cover_Object, Filepath_Payload, LSB_bits)
                Stego_Image = output_filename(File_Cover_Object, "Encode")
                return render_template('output.html', Original_Image=File_Cover_Object, Stegoed_Image=Stego_Image,
                                       charmander=Charmander, Hash1=Hash1, Hash2=Hash2,
                                       Original_Message="Original Image", Stegoed_Message="Stego Image")

            elif ext == 'audio':
                if speech_recognition == 'Yes':
                    try:
                        Filepath_Cover_Object = audio_to_text(Filepath_Cover_Object)

                    except:
                        flash('Speech Recognition failed, File might not have speech')
                        return render_template('encode.html', charmander=Charmander)

                Audio_Encode(Filepath_Cover_Object, Filepath_Payload, LSB_bits)
                Stego_Audio = output_filename(File_Cover_Object, "Encode")
                return render_template('output.html', Original_Audio=File_Cover_Object, Stegoed_Audio=File_Cover_Object,
                                       charmander=Charmander, Hash1=Hash1, Hash2=Hash2,
                                       Original_Message="Original Audio", Stegoed_Message="Stego Audio")

            # elif ext == 'video':
            #    return render_template('output.html', Original_Video=File_Cover_Object, Stegoed_Video=File_Cover_Object,
            #                           charmander=Charmander, Hash1=Hash1, Hash2=Hash2)

        else:
            flash("Please input everything in the form")

    return render_template('encode.html', charmander=Charmander)


@app.route('/decode', methods=['POST', 'GET'])
def decode():
    global File_Cover_Object
    global Cover_Object_Extension

    if request.method == 'POST':

        if request.form.getlist('LSB'):
            LSB = request.form.getlist('LSB')
            LSB = [int(numbers) for numbers in LSB]
            # Check File Extension & if there's a file
            ext = detect_file_type(Cover_Object_Extension)
            if ext == "":
                flash('Please input a file')
                return render_template('encode.html', charmander=Charmander)

            # Get Secret
            if ext == 'img':
                print("IMG decoding")
                print(File_Cover_Object, LSB)
                Decode_file = Img_Decode(Filepath_Cover_Object, LSB)

            elif ext == 'audio':
                Decode_file = Audio_Decode(Filepath_Cover_Object, LSB)

            Decode_file = str(Decode_file)
            temp = Decode_file
            temp = temp.split(".")[1]
            ext = detect_file_type(temp)

            # Displaying Secret
            if ext == 'txt':
                return render_template('output.html', Original_Document=Decode_file, charmander=Pikachu, twenty=1,
                                       Original_Message="Hidden Text")
            if ext == 'img':
                return render_template('output.html', Original_Image=Decode_file, charmander=Pikachu, forty=1,
                                       Original_Message="Hidden Image")
            if ext == 'audio':
                return render_template('output.html', Original_Audio=Decode_file, charmander=Pikachu, sixty=1,
                                       Original_Message="Hidden Audio")
            if ext == 'video':
                return render_template('output.html', Original_Video=Decode_file, charmander=Pikachu, twenty=1,
                                       Original_Message="Hidden Video")

        else:
            flash("Please input everything in the form")

    return render_template('decode.html', charmander=Pikachu)


# First Dropzone action route
@app.route('/first_upload', methods=['Post'])
def first_upload():
    global File_Cover_Object
    global Cover_Object_Extension
    global Filepath_Cover_Object

    if request.method == 'POST':

        # SAVE FILE THAT IS SUBMITTED
        if request.files.get('file'):
            # GET File
            f = request.files.get('file')

            # File Info
            Filepath_Cover_Object = os.path.join(app.config['UPLOADED_PATH'], f.filename)
            File_Cover_Object = f.filename
            Cover_Object_Extension = f.filename.split('.')[1]

            # Check for correct input
            temp = detect_file_type(Cover_Object_Extension)
            if temp == "" or temp == "text" or temp == "video":
                flash("Cover object is an Incorrect File Type ")
                return render_template('encode.html', charmander=Charmander)

            # Save File
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        return File_Cover_Object


# Second Dropzone action route
@app.route('/second_upload', methods=['Post'])
def second_upload():
    global File_Payload
    global Payload_Extension
    global Filepath_Payload

    if request.method == 'POST':

        # SAVE FILE THAT IS SUBMITTED
        if request.files.get('file'):
            # GET File
            f = request.files.get('file')

            # File Info
            Filepath_Payload = os.path.join(
                app.config['UPLOADED_PATH'], f.filename)
            File_Payload = f.filename
            Payload_Extension = f.filename.split('.')[1]

            # Check for correct input
            temp = detect_file_type(Payload_Extension)
            if temp == "":
                flash("Payload is an Incorrect File Type ")
                return render_template('encode.html', charmander=Charmander)

            # Save File
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        return File_Cover_Object


# Third Dropzone action route
@app.route('/third_upload', methods=['Post'])
def third_upload():
    global File_Cover_Object
    global Cover_Object_Extension
    global Filepath_Cover_Object

    if request.method == 'POST':
        print("something1")
        # SAVE FILE THAT IS SUBMITTED
        if request.files.get('file'):
            # GET File
            f = request.files.get('file')

            # File Info
            Filepath_Cover_Object = os.path.join(
                app.config['UPLOADED_PATH'], f.filename)
            File_Cover_Object = f.filename
            Cover_Object_Extension = f.filename.split('.')[1]
            print("Something happened")
            print(Filepath_Cover_Object)

            # Check for correct input
            temp = detect_file_type(Cover_Object_Extension)
            if temp == "" or temp == "text" or temp == "video":
                flash("Cover object is an Incorrect File Type ")
                return render_template('decode.html', charmander=Pikachu)

            # Save File
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        return File_Cover_Object


# Display File
@app.route('/display/<filename>')
def display(filename):
    print('display_image filename: ' + filename)
    if "copy" in filename:
        return redirect(url_for('static', filename='encode_output/' + filename), code=301)
    if "secret" in filename:
        return redirect(url_for('static', filename='decode_output/' + filename), code=301)

    else:
        return redirect(url_for('static', filename='uploads/' + filename), code=301)


# Check Output Filename
def output_filename(filename, output):
    filename = filename.split(".")
    if output == "Encode":
        filename = filename[0] + "_copy." + filename[1]
    else:
        filename = filename[0] + "_secret." + filename[1]
    return filename


def detect_file_type(ext):
    img_type = ["jpeg", "jpg", "png", "bmp"]
    document = ["word", "txt", "xls", "pdf"]
    audio = ["mp3", "wav"]
    video = ["mp4"]
    ext = ext.lower()
    if ext in img_type:
        return 'img'
    elif ext in document:
        return 'text'
    elif ext in audio:
        return 'audio'
    elif ext in video:
        return 'video'
    else:
        return ""


if __name__ == '__main__':
    app.run(debug=True)
