#!/bin/bash

for file in *weights.txt
do 
	sed -n '1p' < "$file" > temp.txt
	cut -f1 temp.txt >> good_labels.txt
	rm temp.txt
done
