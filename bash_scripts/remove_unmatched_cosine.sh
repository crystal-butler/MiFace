#!/bin/bash

FILES=/Users/body_LAB/Desktop/miface/Trial2/Test2_Cosine/Trial2_Cosine_scoresOnly/*

for file in $FILES
do
	<$file awk '$2 !~ /[a-z]/ {print $1 " "  $2}' > temp1.txt
	mv temp1.txt $file
done