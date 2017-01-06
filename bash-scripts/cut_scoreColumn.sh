#!/bin/bash

for file in *.txt
do 
	cut -d ' ' -f3 $file > temp.txt
	mv temp.txt $file
done
