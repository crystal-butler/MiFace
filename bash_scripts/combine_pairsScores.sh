#!/bin/bash

shopt -s nullglob
ARR1=(/Users/interloper/Desktop/MiFace/MTurk_Results/Test2/trial2_allPairsList/*)
ARR1a=("${ARR1[@]##*/}")
ARR2=(/Users/interloper/Desktop/MiFace/MTurk_Results/Test2/trial2_leskScores/*)
ARR2a=("${ARR2[@]##*/}")
DIR=(/Users/interloper/Desktop/MiFace/MTurk_Results/Test2/trial2_pairsScores)

for ((i=0; i<${#ARR1[@]}; i++)); do
	paste "${ARR1[$i]}" "${ARR2[$i]}" > $DIR/${ARR1a[i]}
done 
