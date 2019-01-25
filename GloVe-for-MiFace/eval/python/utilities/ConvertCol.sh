#!/bin/bash

FILES=/data/sam676/TrialThree/Trial3_CosineDist_ScoresCOPY/*

for file in $FILES
do
 awk '{printf "%-20s %s\n", $1,$3}' $file > temp.txt 
 awk '{printf "%-20s %s\n", $2,$3}' $file >> temp.txt 
 mv temp.txt $file 
done

