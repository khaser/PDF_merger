#!/usr/bin/python3.7

import logging
import random
from flask import Flask, render_template, request, flash, redirect, send_from_directory
import os

UPLOAD_FOLDER = '/home/khaser/Documents/Work/PDF_merger/tmp' 
ALLOWED_EXTENSIONS = {'pdf'}

application = Flask(__name__)
application.secret_key = "abracadabra"
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="> %(asctime)-15s %(levelname)-8s || %(message)s")

def secure_filename(name, sess):
    salt = sess + 'abac@#!DSAaba'
    name = name.replace(' ', salt)
    return name.rsplit('/', 1)[1]

@application.route("/")
def index():
    return render_template("index.html")

@application.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@application.route("/delete.png")
def delete():
    return send_from_directory(os.path.join(application.root_path, 'static'), 'delete.png')

@application.route("/templates/jquery.js")
def jquery():
    return render_template("jquery.js")

@application.route("/templates/jquery-ui.js")
def jqueryui():
    return render_template("jquery-ui.js")

@application.route("/templates/sortable.js")
def sortable():
    return render_template("sortable.js")

@application.route("/templates/dnd.js")
def dnd():
    return render_template("dnd.js")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in application.config['ALLOWED_EXTENSIONS']

@application.route('/uploadFolder', methods=['POST', 'GET'])
def uploadFolder():
    files = request.files.getlist("file[]")
    sess = "id" + str(random.randint(0, 10**30))
    path = os.path.join(application.config['UPLOAD_FOLDER'], sess)
    os.makedirs(path, exist_ok=True)
    cnt = 0
    for data in files:
        if (allowed_file(data.filename)):
            cnt += 1
            data.save(os.path.join(path, secure_filename(data.filename, sess)))
    if (cnt == 0):
        return 'no pdf files to merge(need R_LR, R-LA, R-LB substring in file name)'
    os.system('./mergeFolder.sh ' + sess)
    return send_from_directory('result', sess + '.pdf')

@application.route('/upload', methods=['POST', 'GET'])
def upload():
    files = request.files.getlist("files[]")
    sess = "id" + str(random.randint(0, 10**30))
    path = os.path.join(application.config['UPLOAD_FOLDER'], sess)
    os.makedirs(path, exist_ok=True)
    cnt = 0
    for data in files:
        cnt += 1
        s = str(cnt).zfill(7)
        data.save(os.path.join(path, s + ".pdf"))
    os.system('./merge.py ' + sess)
    mem_clear(path)
    return send_from_directory('result', sess + '.pdf')

def mem_clear(sess):
    for root, dirs, files in os.walk(sess, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(sess)

def main():
    application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    application.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    application.run(host='0.0.0.0', debug=True, port=80)

if __name__ == "__main__":
    main()
