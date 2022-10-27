from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from db import db_init, db
from models import Txt
import os
from io import BytesIO

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/database1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_init(app)

def convertToBinaryData(filenamepath):
    with open(filenamepath, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filenamepath):
    mode = 'ab' if os.path.exists(filenamepath) else 'wb'
    with open(filenamepath, mode) as file:
        origData = file.write(data)
    return origData

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    all_uploaded_files = ""

    if request.method == 'POST':
        f = request.files['the_file']
        fileName= secure_filename(f.filename)
        fileNamePath= f"c:/FullStackDevelopment/9_file_upload_via_flask/upload_folder/{fileName}"
        f.save(fileNamePath)
        convertedBinaryFile = convertToBinaryData(fileNamePath)
        print(convertedBinaryFile)
        uploadConvertedBinaryFile = Txt(my_blob=convertedBinaryFile, name=fileName)
        db.session.add(uploadConvertedBinaryFile)
        db.session.commit()

    if request.method == 'GET':
        all_uploaded_files = Txt.query.all()
        for file in all_uploaded_files:
            fileName= file.name
            fileNamePath= f"c:/FullStackDevelopment/9_file_upload_via_flask/download_folder/{fileName}"
            origData = write_file(file.my_blob, fileNamePath)

    return render_template('index.html', uploaded_files = all_uploaded_files)

if __name__ == '__main__':
    app.run()