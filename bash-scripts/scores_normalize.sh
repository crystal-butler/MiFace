#!/bin/bash

FILES=/Users/interloper/Desktop/MiFace/MTurk_Results/Test2/trial2_Scores_processing/*

for file in $FILES
do
	awk '{$2 /= 400; print}' $file > temp.txt
	mv temp.txt $file
done