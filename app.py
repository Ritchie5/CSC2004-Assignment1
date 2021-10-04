import os
import shutil

from flask import Flask, flash, render_template, request, url_for  # import flask class and relevant libraries
from flask_dropzone import Dropzone  # import flask dropzone
from werkzeug.utils import redirect

basedir = os.path.abspath(os.path.dirname(__file__))  # specify filepath

File_Cover_Object = ""
File_Payload = ""
Cover_Object_Extension = ""
Payload_Extension = ""
Charmander = "static/uploads/charmander.png"

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
app.config['DROPZONE_MAX_FILE_SIZE'] = 2  # Set Max allowed file size to 2mb
app.config['DROPZONE_DEFAULT_MESSAGE'] = "Drop / Click to Upload File"


# Set default message in box

@app.route('/')  # provide Flask an URL on which function to be triggered (root)
def home():
    # indicate which html file to render
    return render_template('encode.html', charmander=Charmander)


@app.route('/encode', methods=['POST', 'GET'])
def encode():
    global file_extension
    global file_name
    if request.method == 'POST':

        try:
            LSB = request.form['LSB']
            print(LSB)
            # Check File Extension & if there's a file
            ext = detect_file_type(file_extension)
            if ext == "":
                flash('Please input a file')

                # CHECK THE FILE EXTENSION AND EXECUTE ACCORDINGLY

            if ext == 'text':
                pass
            if ext == 'img':
                # file = logic(file_name)
                # f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                cover_img = ""
                return render_template('picture.html', filename=file_name, filename1=file_name)
            elif ext == 'audio':
                return render_template('audio.html', filename=file_name, filename1=file_name)
            elif ext == 'video':
                return render_template('video.html', filename=file_name, filename1=file_name)

        except:
            flash("Please input everything in the form")

    return render_template('encode.html', charmander = Charmander)


@app.route('/decode', methods=['POST', 'GET'])
def decode():
    global file_extension
    global file_name
    if request.method == 'POST':

        if request.form['LSB']:
            if request.form.get('Filetype'):
                LSB = request.form['LSB']
                Filetype = request.form.get('Filetype')
                print(Filetype, LSB)
                # Check File Extension & if there's a file
                ext = detect_file_type(file_extension)
                if ext == "":
                    flash('Please input a file')

                # CHECK THE FILE EXTENSION AND EXECUTE ACCORDINGLY

                if ext == 'text':
                    pass
                if ext == 'img':
                    # file = logic(file_name)
                    # f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                    cover_img = ""
                    return render_template('picture.html', filename=file_name, filename1=file_name)
                elif ext == 'audio':
                    return render_template('audio.html', filename=file_name, filename1=file_name)
                elif ext == 'video':
                    return render_template('video.html', filename=file_name, filename1=file_name)

            else:
                flash("Please input everything in the form")

    return render_template('decode.html', charmander=Charmander)


@app.route('/first_upload', methods=['Post'])
def first_upload():
    global file_extension
    global file_name

    if request.method == 'POST':

        # CHECK IF THE FILE AND FORM IS SUBMITTED
        if request.files.get('file'):
            f = request.files.get('file')

            print(os.path.join(app.config['UPLOADED_PATH']))
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
            file_extension = f.filename.split('.')[1]
            file_name = f.filename
            print(file_name)
        return file_name


@app.route('/second_upload', methods=['Post'])
def second_upload():
    global file_extension
    global file_name

    if request.method == 'POST':

        # CHECK IF THE FILE AND FORM IS SUBMITTED
        if request.files.get('file'):
            f = request.files.get('file')
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
            file_extension = f.filename.split('.')[1]
            file_name = f.filename
            print(file_name)
        return file_name


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/display/<filename>')
def display_video(filename):
    # print('display_video filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/display/<filename>')
def display_audio(filename):
    # print('display_video filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


def detect_file_type(ext):
    img_type = ["jpeg", "jpg", "png", "bmp"]
    document = ["word", "txt", "xls"]
    audio = ["mp3", "wav"]
    video = ["mp4"]
    ext = ext.lower()
    if ext in img_type:
        return 'img'
    elif ext in document:
        return 'text'
    elif ext in video:
        return 'audio'
    elif ext in video:
        return 'video'
    else:
        return ""


def logic(file, number_of_lsb):
    # Figure out the type of file for us to upload
    # For The Logic team to fill out
    return None


def read_text_file():
    pass


if __name__ == '__main__':
    app.run(debug=True)
