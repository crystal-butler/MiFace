#!/bin/bash

FILES=/Users/interloper/Desktop/MiFace/MTurk_Results/Test2/trial2_allPairsList/*

for file in $FILES
do
	perl similarity.pl --type lesk --file $file
done
