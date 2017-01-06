#!/bin/bash

FILES=/Users/interloper/Desktop/MiFace/MTurk_Results/Test2/trial2_Scores_processing/*

for file in $FILES
do
	grep -v "WordNet" $file > temp && mv temp $file
done
