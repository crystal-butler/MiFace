#!/bin/bash

FILES=/data/sam676/TrialTwo/Trial2_CosineDist_ScoresSingleColCOPY/*

for file in $FILES
do
	sort -k1 -n -r $file > temp.txt
	mv temp.txt $file
done