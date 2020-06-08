#!/usr/bin/python3.7
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys
def getType(point):
    d = {'4A0' : 4768 * 6741, '2A0' : 3370 * 4768, 'A0' : 2384 * 3370, 'A1' : 1684 * 2384, 'A2' : 1191 * 1684, 'A3' : 842 * 1191, 'A4' : 595 * 842, 'A5' : 420 * 595, 'A6' : 298 * 420, 'A7' : 210 * 298, 'A8' : 147 * 210,'A9' : 105 * 147, 'A10' : 74 * 105}
    attitude = 6741 / 4768
    for i in d:
        if abs((point[0] * point[1]) / d[i] - 1) <= 0.01:
            if abs(float(point[1] / point[0]) - attitude) <= 0.02:
                return 'vertical ' + i
            if abs(float(point[0] / point[1]) - attitude) <= 0.02:
                return 'horizontal ' + i
    return 'unknown'

path = os.path.abspath(__file__)
while path[-1] != '/':
    path = path[:-1]
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
        last = 'kek'
        lastI = -1
        for i in range(pdfcur.getNumPages()):
            page = pdfcur.getPage(i)
            cur = getType(page.mediaBox.upperRight)
            if cur == last:
                continue
            else:
                if lastI != -1:
                    print(lastI + 1, '-', i, 'type is', last)
                last = cur
                lastI = i
        print(lastI + 1, '-', i + 1, 'type is', cur)
        print()
sys.stdout = original_stdout
