#!/bin/bash

FILES=/Users/body_LAB/Desktop/miface/Trial2/Test2_Cosine/Trial2_Cosine_weightsSorted/*

for file in $FILES
do
	sort -k2 -n -r $file > temp1.txt
	mv temp1.txt $file
done