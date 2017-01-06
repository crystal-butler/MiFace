#!/bin/bash
# meant to be run from CLI within folder with first set of files for pasting

for i in *
do 
	paste ${i} /Users/body_LAB/Desktop/miface/Trial2/Test2_Cosine/Trial2_Cosine_weightsSorted/${i} > ${i}.leskXcosine.txt
done