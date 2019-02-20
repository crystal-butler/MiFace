#!/bin/bash

FILES=/Users/interloper/Desktop/MiFace/MTurk_Results/Test2/trial2_Scores_results/*

touch trial2_Scores_topLabels
for file in $FILES
do
	head -n 1 $file >> trial2_Scores_topLabels
done