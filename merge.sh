#!/bin/bash
folder=`pwd`
cd $folder/tmp/$1
sid=`echo $1`
echo $sid
cd $folder/tmp/$sid
pdfunite *.pdf $folder/result/$sid.pdf
