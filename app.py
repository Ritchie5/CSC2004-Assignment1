import os

from flask import Flask, render_template, request
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_MAX_FILE_SIZE=1024,  # set max size limit to a large number, here is 1024 MB
    DROPZONE_TIMEOUT=5 * 60 * 1000  # set upload timeout to a large number, here is 5 minutes
)yvc

dropzone = Dropzone(app)

app.config['DROPZONE_MAX_FILES'] = 1        # Set Max amount of file user can input to 1
app.config['DROPZONE_MAX_FILE_SIZE'] = 1    # Set Max allowed file size to 1mb
app.config['DROPZONE_DEFAULT_MESSAGE'] = "Drop files here to upload or Click to select file to upload"
# Set default message in box


@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        return render_template('output.html')
    return render_template('index.html')


def lsb_type(file, number_of_lsb):
    # Figure out the type of file for us to upload
    # For The Logic team to fill out
    pass


if __name__ == '__main__':
    app.run(debug=True)