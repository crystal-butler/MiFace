#!/bin/bash

FILES=/data/sam676/TrialThree/Trial3_CosineDist_Scores1ColCOPY/*

for file in $FILES
do
	<$file awk '$2 !~ /[a-z]/ {print $1 " "  $2}' > temp1.txt
	mv temp1.txt $file
done