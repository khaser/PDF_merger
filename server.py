#!/usr/bin/python3.7

import asyncio
import logging
import random
from flask import Flask, render_template, request, flash, redirect, send_from_directory
import os

UPLOAD_FOLDER = '/home/khaser/Documents/Work/PDF_merger/tmp' 
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.secret_key = "abracadabra"
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="> %(asctime)-15s %(levelname)-8s || %(message)s")

def secure_filename(name, sess):
    salt = sess + 'abac@#!DSAaba'
    name = name.replace(' ', salt)
    return name.rsplit('/', 1)[1]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/templates/jquery.js")
def jquery():
    return render_template("jquery.js")

@app.route("/templates/jquery-ui.js")
def jqueryui():
    return render_template("jquery-ui.js")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    files = request.files.getlist("file[]")
    sess = "id" + str(random.randint(0, 10**30))
    path = os.path.join(app.config['UPLOAD_FOLDER'], sess)
    os.makedirs(path, exist_ok=True)
    cnt = 0
    for data in files:
        if (allowed_file(data.filename)):
            cnt += 1
            data.save(os.path.join(path, secure_filename(data.filename, sess)))
    if (cnt == 0):
        return 'no pdf files to merge(need R_LR, R-LA, R-LB substring in file name)'
    os.system('./solver.sh ' + sess)
    return send_from_directory('result', sess + '.pdf')


def main():
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.run(host='0.0.0.0', debug=True, port=80)

if __name__ == "__main__":
    main()
