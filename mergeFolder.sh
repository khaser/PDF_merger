#!/bin/bash
folder=`pwd`
cd $folder/tmp/$1
sid=`echo $1`
echo $sid
cd $folder/tmp/$sid
LR=`ls | awk '/.*R-LR.*\.pdf/{print $0}'`
LA=`ls | awk '/.*R-LA.*\.pdf/{print $0}'`
LB=`ls | awk '/.*R-LB.*\.pdf/{print $0}'`
pdfunite `(echo $LR; echo $LA; echo $LB) | cat` $folder/result/$sid.pdf
