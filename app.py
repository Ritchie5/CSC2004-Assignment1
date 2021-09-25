import os

from flask import Flask, flash, render_template, request   # import flask class and relevant libraries
from flask_dropzone import Dropzone     # import flask dropzone

basedir = os.path.abspath(os.path.dirname(__file__))    # specify filepath

file_extension = ""

app = Flask(__name__)   # create an instance and initialise the flask
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# configure the setting of the uploaded item
app.config.update(  
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),     # storing of uploaded item into specified filepath
    # Flask-Dropzone config:
    DROPZONE_MAX_FILE_SIZE=1024,  # set max size limit to a large number, here is 1024 MB
    DROPZONE_TIMEOUT=5 * 60 * 1000  # set upload timeout to a large number, here is 5 minutes
)

dropzone = Dropzone(app)

app.config['DROPZONE_MAX_FILES'] = 1        # Set Max amount of file user can input to 1
app.config['DROPZONE_MAX_FILE_SIZE'] = 1    # Set Max allowed file size to 1mb
app.config['DROPZONE_DEFAULT_MESSAGE'] = "Drop file here to upload or Click to select file to upload"
# Set default message in box


@app.route('/')     # provide Flask an URL on which function to be triggered (root)
def home():
    return render_template('home.html')     # indicate which html file to render


@app.route('/', methods=['POST', 'GET'])
def upload():
    global file_extension
    if request.method == 'POST':

        if request.files.get('file'):
            f = request.files.get('file')
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
            file_extension = f.filename.split('.')[1]

        if request.form.get('payload'):
            if request.form.get('LSB'):
                payload = request.form.get('payload')
                LSB = request.form.get('LSB')
                option = request.form.getlist('option')[0]
                ext = detect_file_type(file_extension)

                if ext == "":
                    flash('Please input a file')
                    return render_template('home.html')
                if ext == 'img':
                    return render_template('picture.html')
                elif ext == 'audio':
                    return render_template('audio.html')
                elif ext == 'video':
                    return render_template('video.html')


        return render_template('home.html')


def detect_file_type(ext):
    img_type = ["jpeg", "jpg", "png", "bmp"]
    document = ["word", "txt", "xls"]
    audio_video = ["mp3", "mp4", "wav"]
    if ext.lower() in img_type:
        return 'img'
    elif ext.lower() in document:
        return 'audio'
    elif ext.lower() in audio_video:
        return 'video'
    else:
        return ""


def logic(file, number_of_lsb):
    # Figure out the type of file for us to upload
    # For The Logic team to fill out
    pass


if __name__ == '__main__':
    app.run(debug=True)
