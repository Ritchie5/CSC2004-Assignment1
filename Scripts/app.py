from hash import hash1
from audioSteg import Audio_Encode
from imageSteg import Img_Encode
import speechRecognition

import os
import shutil

from flask import Flask, flash, render_template, request, url_for  # import flask class and relevant libraries
from flask_dropzone import Dropzone  # import flask dropzone
from werkzeug.utils import redirect

basedir = os.path.abspath(os.path.dirname(__file__))  # specify filepath

Filepath_Cover_Object = ""
File_Cover_Object = ""
Cover_Object_Extension = ""

Filepath_Payload = ""
File_Payload = ""
Payload_Extension = ""

Charmander = "static/uploads/charmander.jpg"
Pikachu = "static/uploads/pikachu.png"

app = Flask(__name__)  # create an instance and initialise the flask
app.secret_key = "Charmander"

# configure the setting of the uploaded item
app.config.update(
    UPLOADED_PATH='static/uploads',  # storing of uploaded item into specified filepath
    # Flask-Dropzone config:
    DROPZONE_MAX_FILE_SIZE=1024,  # set max size limit to a large number, here is 1024 MB
    DROPZONE_TIMEOUT=5 * 60 * 1000  # set upload timeout to a large number, here is 5 minutes
)

dropzone = Dropzone(app)

app.config['DROPZONE_MAX_FILES'] = 1  # Set Max amount of file user can input to 1
app.config['DROPZONE_MAX_FILE_SIZE'] = 10  # Set Max allowed file size to 2mb
app.config['DROPZONE_DEFAULT_MESSAGE'] = "Drop / Click to Upload File"


# Set default message in box

@app.route('/')  # provide Flask an URL on which function to be triggered (root)
def home():
    # indicate which html file to render
    return render_template('encode.html', charmander=Pikachu)


@app.route('/encode', methods=['POST', 'GET'])
def encode():
    global File_Cover_Object
    global Cover_Object_Extension
    global File_Payload
    global Payload_Extension

    if request.method == 'POST':

        if request.form.getlist('LSB'):
            LSB_bits = request.form.getlist('LSB')
            LSB_bits = [int(numbers) for numbers in LSB_bits]

            # Check File Extension
            ext = detect_file_type(Cover_Object_Extension)
            ext1 = detect_file_type(Payload_Extension)

            # Check if Cover object and Payload is given
            if ext == "" or ext1 == "":
                flash('Please input a file')
                return render_template('encode.html', charmander=Charmander)

            Hash1 = hash1(Filepath_Cover_Object)
            Hash1 = "Hash: " + Hash1
            Hash2 = hash1(Filepath_Payload)
            Hash2 = "Hash: " + Hash2

            # CHECK THE FILE EXTENSION AND EXECUTE ACCORDINGLY
            if ext == 'text':
                return render_template('output.html', Original_Document=File_Cover_Object,
                                       Stegoed_Document=File_Cover_Object, charmander=Charmander, Hash1=Hash1, Hash2=Hash2)

            if ext == 'img':
                Img_Encode(Filepath_Cover_Object, Filepath_Payload, LSB_bits)
                Stego_Image = output_filename(File_Cover_Object, "Encode")
                return render_template('output.html', Original_Image=File_Cover_Object, Stegoed_Image=Stego_Image,
                                       charmander=Charmander, Hash1=Hash1, Hash2=Hash2)

            elif ext == 'audio':
                Audio_Encode(Filepath_Cover_Object, Filepath_Payload, LSB_bits)
                Stego_Audio = output_filename(File_Cover_Object, "Encode")
                return render_template('output.html', Original_Audio=File_Cover_Object, Stegoed_Audio=File_Cover_Object,
                                       charmander=Charmander, Hash1=Hash1, Hash2=Hash2)
            elif ext == 'video':
                return render_template('output.html', Original_Video=File_Cover_Object, Stegoed_Video=File_Cover_Object,
                                       charmander=Charmander, Hash1=Hash1, Hash2=Hash2)



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
            ext1 = detect_file_type(Payload_Extension)
            flash('Please input a file')

            # CHECK THE FILE EXTENSION AND EXECUTE ACCORDINGLY

            if ext == 'text':
                return render_template('output.html', Original_Document=File_Cover_Object,
                                       Stegoed_Document=File_Cover_Object, Payload=File_Payload, charmander=Charmander)
            if ext == 'img':
                # file = logic(file_name)
                # f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))

                return render_template('output.html', Original_Image=File_Cover_Object, Stegoed_Image=File_Cover_Object,
                                       Payload=File_Payload, charmander=Charmander)
            elif ext == 'video':
                return render_template('output.html', Original_Video=File_Cover_Object, Stegoed_Video=File_Cover_Object,
                                       Payload=File_Payload, charmander=Charmander)
            elif ext == 'audio':
                return render_template('output.html', Original_Audio=File_Cover_Object, Stegoed_Audio=File_Cover_Object,
                                       Payload=File_Payload, charmander=Charmander)
        else:
            flash("Please input everything in the form")

    return render_template('decode.html', charmander=Pikachu)


@app.route('/first_upload', methods=['Post'])
def first_upload():
    global File_Cover_Object
    global Cover_Object_Extension
    global Filepath_Cover_Object

    if request.method == 'POST':

        # CHECK IF THE FILE AND FORM IS SUBMITTED
        if request.files.get('file'):
            f = request.files.get('file')

            print(os.path.join(app.config['UPLOADED_PATH']))
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
            Filepath_Cover_Object = os.path.join(app.config['UPLOADED_PATH'], f.filename)
            File_Cover_Object = f.filename
            Cover_Object_Extension = f.filename.split('.')[1]
            print(File_Cover_Object)
        return File_Cover_Object


@app.route('/second_upload', methods=['Post'])
def second_upload():
    global File_Payload
    global Payload_Extension
    global Filepath_Payload

    if request.method == 'POST':

        # CHECK IF THE FILE AND FORM IS SUBMITTED
        if request.files.get('file'):
            f = request.files.get('file')
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
            Filepath_Payload = os.path.join(app.config['UPLOADED_PATH'], f.filename)
            File_Payload = f.filename
            Payload_Extension = f.filename.split('.')[1]
            print(File_Payload)
        return File_Payload


@app.route('/display/<filename>')
def display(filename):
    print('display_image filename: ' + filename)
    if "copy" in filename:
        return redirect(url_for('static', filename='encode_output/' + filename), code=301)
    if "secret" in filename:
        return redirect(url_for('static', filename='decode_output/' + filename), code=301)

    else:
        return redirect(url_for('static', filename='uploads/' + filename), code=301)


def display(filename):
    print('display_image filename: ' + filename)

    return redirect(url_for('static', filename='uploads/' + filename), code=301)


def output_filename(filename, output):
    filename = filename.split(".")
    if output == "Encode":
        filename = filename[0] + "_copy." + filename[1]
    else:
        filename = filename[0] + "_secret_message." + filename[1]
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


def logic(file, number_of_lsb):
    # Figure out the type of file for us to upload
    # For The Logic team to fill out
    return None


if __name__ == '__main__':
    app.run(debug=True)
