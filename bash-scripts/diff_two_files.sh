#!/bin/bash

FILES=/Users/body_LAB/Desktop/miface/Trial2/Trial2_weight_comparisons/comparisons/wordPairs/*

for file in $FILES
do
	<$file awk -F ' ' '$1!=$2 {print $1, " ", $2}' > temp1.txt
	mv temp1.txt ../diffs/$file
done