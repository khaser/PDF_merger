#!/usr/bin/python3.7

from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys
output = PdfFileWriter()
path = os.path.abspath(__file__)
while path[-1] != '/':
    path = path[:-1]
outpath = os.path.join(path, 'result')
sess = sys.argv[1]
path = os.path.join(path, 'tmp', sess)
files = sorted(os.listdir(path))
print(files)
for name in files:
    pdfcur = PdfFileReader(open(os.path.join(path, name), "rb"))
    for i in range(pdfcur.getNumPages()):
        output.addPage(pdfcur.getPage(i))
outputStream = open(os.path.join(outpath, sess) + '.pdf', "wb")
output.write(outputStream)  
outputStream.close()
