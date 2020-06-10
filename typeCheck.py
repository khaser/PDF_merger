#!/usr/bin/python3.7

from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys
d1 = {'A0' : [2384, 3370,200], 'A1' : [1684, 2384,150], 'A2' : [1191,1684,120], 'A3' : [842,1191,95], 'A4' : [595,842,70], 'A5' : [420, 595,60], 'A6' : [298, 420,50], 'A7' : [210, 298,40], 'A8' : [147, 210,28],'A9' : [105,147,27], 'A10' : [74 ,105,23]}
d = {'A0' : [2384, 3370,200], 'A1' : [1684, 2384,150], 'A2' : [1191,1684,120], 'A3' : [842,1191,95], 'A4' : [595,842,70], 'A5' : [420, 595,60], 'A6' : [298, 420,50], 'A7' : [210, 298,40], 'A8' : [147, 210,28],'A9' : [105,147,27], 'A10' : [74 ,105,23]}
def getType(point):
    x = point[0]
    y = point[1]
    if x > y:
        x, y = y, x
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
for i in d1:
    if 'x' in i:
        continue
    for cnt in range(2,6):
        d[i + 'x' + str(cnt)] = [d[i][0] * cnt, d[i][1] * cnt, d[i][2]]

with open(outpath,'w') as f:
    for name in files:
        pdfcur = PdfFileReader(open(os.path.join(path, name), "rb"))
        sys.stdout = f
        print('Document', name, ':')
        d2 = {'A0' : [], 'A1' : [], 'A2' : [], 'A3' : [], 'A4' : [], 'A5' : [], 'A6' : [], 'A7' : [], 'A8' : [],'A9' : [], 'A10' : [], 'unknown' : []}
        for i in d1:
            if 'x' in i:
                continue
            for cnt in range(2,6):
                d2[i + 'x' + str(cnt)] = []
        for i in range(pdfcur.getNumPages()):
            page = pdfcur.getPage(i)
            point = page.mediaBox.upperRight
            d2[getType(point)].append(i + 1)
        noComma = 'kek'
        for i in d2:
            if len(d2[i]) > 0:
                noComma = i
        for i in d2:
            if len(d2[i]) == 0:
                continue
            last = d2[i][0]
            for j in range(1,len(d2[i])):
                if d2[i][j] != d2[i][j-1] + 1:
                    if last == d2[i][j-1]:
                        print(last, end = ', ', sep = '')
                    else:
                        print(last,'-',d2[i][j-1], end = ', ', sep = '')
                    last = d2[i][j]
            if i == noComma:
                if last == d2[i][len(d2[i]) - 1]:
                    print(last, '-', i, sep = '')
                else:
                    print(last, '-', d2[i][len(d2[i]) - 1], '-', i, sep = '')

            else:
                if last == d2[i][len(d2[i]) - 1]:
                    print(last, '-', i, end = ',', sep = '')
                    print()
                else:
                    print(last, '-', d2[i][len(d2[i]) - 1], '-', i, end = ',', sep = '')
                    print()
sys.stdout = original_stdout
