#!/bin/bash
folder=`pwd`
cd $1
sid=`echo $1 | cut -d '/' -f 2`
echo $sid
pdfunite `ls | awk '/.*R-LR|R-LA|R-LB.*\.pdf/{print $0}'` $folder/result/$sid.pdf
