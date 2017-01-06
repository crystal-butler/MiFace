#!/bin/bash

FILES=/Users/body_LAB/Desktop/miface/Trial2/Trial2_weight_comparisons/*

for file in $FILES
do
	column -t $file > temp.txt
	mv temp.txt $file
done