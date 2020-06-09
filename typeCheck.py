#!/usr/bin/python3.7

from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys
def getType(point):
    x = point[0]
    y = point[1]
    if x > y:
        x, y = y, x
    d = {'4A0' : [4768,6741,850], '2A0' : [3370,4768,600], 'A0' : [2384, 3370,400], 'A1' : [1684, 2384,300], 'A2' : [1191,1684,200], 'A3' : [842,1191,150], 'A4' : [595,842,100], 'A5' : [420, 595,80], 'A6' : [298, 420,50], 'A7' : [210, 298,45], 'A8' : [147, 210,30],'A9' : [105,147,20], 'A10' : [74 ,105,15]}
    for i in d:
        if (x >= d[i][0] - d[i][2] and x <= d[i][0] + d[i][2]) or (y >= d[i][1] - d[i][2] and y <= d[i][1] + d[i][2]):
            return i
    return 'unknown'

path = os.path.abspath(__file__)
path = os.path.split(path)[0]
sess = sys.argv[1]
outpath = os.path.join(path, 'result', sess + '.txt' )
path = os.path.join(path, 'tmp', sess)
files = os.listdir(path)
original_stdout = sys.stdout
with open(outpath,'w') as f:
    for name in files:
        pdfcur = PdfFileReader(open(os.path.join(path, name), "rb"))
        sys.stdout = f
        print('Document', name, ':')
        d = {'4A0' : [], '2A0' : [], 'A0' : [], 'A1' : [], 'A2' : [], 'A3' : [], 'A4' : [], 'A5' : [], 'A6' : [], 'A7' : [], 'A8' : [],'A9' : [], 'A10' : [], 'unknown' : []}
        for i in range(pdfcur.getNumPages()):
            page = pdfcur.getPage(i)
            point = page.mediaBox.upperRight
            d[getType(point)].append(i + 1)
        noComma = 'kek'
        for i in d:
            if len(d[i]) > 0:
                noComma = i
        for i in d:
            if len(d[i]) == 0:
                continue
            last = d[i][0]
            for j in range(1,len(d[i])):
                if d[i][j] != d[i][j-1] + 1:
                    if last == d[i][j-1]:
                        print(last, end = ', ', sep = '')
                    else:
                        print(last,'-',d[i][j-1], end = ', ', sep = '')
                    last = d[i][j]
            if i == noComma:
                if last == d[i][len(d[i]) - 1]:
                    print(last, '-', i, sep = '')
                else:
                    print(last, '-', d[i][len(d[i]) - 1], '-', i, sep = '')

            else:
                if last == d[i][len(d[i]) - 1]:
                    print(last, '-', i, end = ', ', sep = '')
                    print()
                else:
                    print(last, '-', d[i][len(d[i]) - 1], '-', i, end = ', ', sep = '')
                    print()
sys.stdout = original_stdout
