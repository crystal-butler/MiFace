#!/bin/bash

for file in *weights.txt
do 
	sort -k2 -n -r "$file" > temp.txt
	mv temp.txt "$file"
done
