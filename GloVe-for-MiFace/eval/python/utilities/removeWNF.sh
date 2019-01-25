#!/bin/bash

FILES=/data/sam676/TrialThree/Trial3_CosineDist_ScoresCOPY/*

for file in $FILES
do
	if [["$2" == 
 awk '{$2}' $file > temp.txt 
 mv temp.txt $file 
done