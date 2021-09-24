import os

from flask import Flask, render_template, request   # import flask class and relevant libraries
from flask_dropzone import Dropzone     # import flask dropzone

basedir = os.path.abspath(os.path.dirname(__file__))    # specify filepath

app = Flask(__name__)   # create an instance and initialise the flask

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

@app.route('/picture', methods=['POST', 'GET']) # direct Flask to another URL, setting flask to be able to get and post
def picture():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        return render_template('output.html')
    return render_template('picture.html')    # indicate which html file to render

@app.route('/video', methods=['POST', 'GET'])
def video():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        return render_template('output.html')
    return render_template('video.html')    # indicate which html file to render

@app.route('/audio', methods=['POST', 'GET'])
def audio():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        return render_template('output.html')
    return render_template('audio.html')    # indicate which html file to render

def lsb_type(file, number_of_lsb):
    # Figure out the type of file for us to upload
    # For The Logic team to fill out
    pass


if __name__ == '__main__':
    app.run(debug=True)
