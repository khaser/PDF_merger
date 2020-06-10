#!/usr/bin/python3.7

import logging
import random
import zipfile
from flask import Flask, render_template, request, flash, redirect, send_from_directory
import os

UPLOAD_FOLDER = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'tmp')
ALLOWED_EXTENSIONS = {'pdf'}

application = Flask(__name__)
application.secret_key = "abracadabra"
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="> %(asctime)-15s %(levelname)-8s || %(message)s")

@application.route("/")
def index():
    return render_template("index.html")

@application.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
            data.save(os.path.join(path, os.path.split(data.filename)[1]))
    if (cnt == 0):
        return 'no pdf files to merge(need R_LR, R-LA, R-LB substring in file name)'
    os.system('./mergeFolder.py ' + sess)
    mem_clear(path)
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

@application.route('/uploadRecursive', methods=['POST', 'GET'])
def uploadRecursive():
    files = request.files.getlist("file[]")
    sess = "id" + str(random.randint(0, 10**30))
    path = os.path.join(application.config['UPLOAD_FOLDER'], sess)
    cnt = 0
    for data in files:
        if (allowed_file(data.filename)):
            cnt += 1
            file = os.path.join(path, data.filename)
            os.makedirs(os.path.split(file)[0], exist_ok=True)
            data.save(os.path.join(path, data.filename))
    os.system('./mergeRecursive.py ' + sess)
    mem_clear(path)
    zipf = zipfile.ZipFile(os.path.join('result', sess + '.zip'), 'w', zipfile.ZIP_DEFLATED)
    tmp = os.getcwd()
    os.chdir(os.path.join('result', sess))
    zipdir('.', zipf)
    zipf.close()
    os.chdir(tmp)
    return send_from_directory('result', sess + '.zip')

@application.route('/uploadTypes', methods=['POST', 'GET'])
def uploadTypes():
    files = request.files.getlist("file[]")
    sess = "id" + str(random.randint(0, 10**30))
    path = os.path.join(application.config['UPLOAD_FOLDER'], sess)
    os.makedirs(path, exist_ok=True)
    cnt = 0
    for data in files:
        if (allowed_file(data.filename)):
            cnt += 1
            data.save(os.path.join(path, os.path.split(data.filename)[1]))
    if (cnt == 0):
        return 'no pdf files to merge(need R_LR, R-LA, R-LB substring in file name)'
    os.system('./typeCheck.py ' + sess)
    mem_clear(path)
    return send_from_directory('result', sess + '.txt', as_attachment=True)

@application.route('/uploadExcel', methods=['POST', 'GET'])
def uploadExcel():
    files = request.files.getlist("file[]")
    sess = "id" + str(random.randint(0, 10**30))
    path = os.path.join(application.config['UPLOAD_FOLDER'], sess)
    for data in files:
        if (allowed_file(data.filename)):
            file = os.path.join(path, os.path.split(data.filename)[1])
            os.makedirs(os.path.split(file)[0], exist_ok=True)
            data.save(file)
        elif (is_fileExcel(data.filename)):
            file = os.path.join(path, data.filename)
            os.makedirs(path, exist_ok=True)
            data.save(os.path.join(path, 'merge.xlsx'))
    os.system('./mergeExcel.py ' + sess)
    mem_clear(path)
    zipf = zipfile.ZipFile(os.path.join('result', sess + '.zip'), 'w', zipfile.ZIP_DEFLATED)
    tmp = os.getcwd()
    os.chdir(os.path.join('result', sess))
    zipdir('.', zipf)
    zipf.close()
    os.chdir(tmp)
    return send_from_directory('result', sess + '.zip')


def mem_clear(sess):
    for root, dirs, files in os.walk(sess, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(sess)

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def is_fileExcel(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in {'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in application.config['ALLOWED_EXTENSIONS']


def main():
    application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    application.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    application.run(host='0.0.0.0', debug=True, port=80)

if __name__ == "__main__":
    main()
