#!/usr/bin/python3.7

import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter

global sess, root
sess = sys.argv[1]
root = os.getcwd()
os.chdir(os.path.join('tmp', sess))

def merge_dir(path):
    output = PdfFileWriter()
    outpath = os.path.join(root, 'result', sess, path)
    files = os.listdir(path)
    for name in files:
        if 'R-LR' in name:
            pdfcur = PdfFileReader(open(os.path.join(path, name), "rb"))
            for i in range(pdfcur.getNumPages()):
                output.addPage(pdfcur.getPage(i))
    for name in files:
        if 'R-LA' in name:
            pdfcur = PdfFileReader(open(os.path.join(path, name), "rb"))
            for i in range(pdfcur.getNumPages()):
                output.addPage(pdfcur.getPage(i))
    for name in files:
        if 'R-LB' in name:
            pdfcur = PdfFileReader(open(os.path.join(path, name), "rb"))
            for i in range(pdfcur.getNumPages()):
                output.addPage(pdfcur.getPage(i))
    outputStream = open(outpath + '.pdf', "wb")
    output.write(outputStream)  
    outputStream.close()



for i in os.walk('.'):
    path = os.path.normpath(i[0])
    folders = i[1]
    files = [file for file in i[2] if file.endswith('.pdf')]
    if (len(folders) > 0):
        new_folder = os.path.join(root, 'result', sess, path)
        os.makedirs(new_folder, exist_ok=True)
    if (len(files) > 0):
        merge_dir(path)

