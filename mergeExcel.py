#!/usr/bin/python3.7

from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys
import openpyxl

global path
path = os.path.abspath(__file__)
path = os.path.split(path)[0]
sess = sys.argv[1]
outpath = os.path.join(path, 'result', sess)
path = os.path.join(path, 'tmp', sess)

def addPDF(name, stream):
    if (os.path.exists(os.path.join(path, name))):
    	pdfcur = PdfFileReader(open(os.path.join(path, name), "rb"))
    	for i in range(pdfcur.getNumPages()):
  	    stream.addPage(pdfcur.getPage(i))
    else:
        not_found.append(name)

wb = openpyxl.load_workbook(filename = os.path.join(path, 'merge.xlsx'))
sheet = wb[wb.sheetnames[0]]

global not_found
not_found = []

for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    empty_cnt = 0
    d = {}
    cur = "trash"

    for i in range(1, 100500):
        file = sheet.cell(row=i, column=1)
        if (file.value == None):
            empty_cnt += 1;
            continue;
        if (file.font.b == True):
            cur = file.value
            continue;
        file.value = file.value + '.pdf'
        d.setdefault(cur, []).append(file.value) 
        if (empty_cnt > 5):
            break;

    for i in d.items():
        fout, files = i[0], i[1]
        fout = os.path.join(outpath, sheet_name, str(fout))

        output = PdfFileWriter()
        for item in files:
            addPDF(item, output)
    
        os.makedirs(os.path.split(fout)[0], exist_ok=True)
        outputStream = open(fout + '.pdf', "wb")
        output.write(outputStream)
        outputStream.close()

report = open(os.path.join(outpath, "report.txt"), 'w') 
if (len(not_found) != 0):
    print("Мы не нашли след. файлы, но все равно склеили без них:", file = report)
else:
    print("Склейка успешна, все файлы на месте", file = report)
print(*not_found, sep = '\n', file=report)
report.close()
