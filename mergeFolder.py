#!/usr/bin/python3.7

from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys
output = PdfFileWriter()
path = os.path.abspath(__file__)
while path[-1] != '/':
    path = path[:-1]
outpath = os.path.join(path,'result')
sess = sys.argv[1]
path = os.path.join(path,'tmp',sess)
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
outputStream = open(os.path.join(outpath, sess) + '.pdf', "wb")
output.write(outputStream)  
outputStream.close()
