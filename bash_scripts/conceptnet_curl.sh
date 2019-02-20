#!/bin/bash

# Hard coded file paths at the time of authoring.
# in="/Users/body_LAB/Documents/MiFace/NLP/Testing/Word_Pair_Lists/FE_Pairs.txt"
# out="/Users/body_LAB/Documents/MiFace/NLP/Testing/Word_Pair_Scores/FE_pairs_conceptnet.txt"

read -p 'Input file path: ' infile
read -p 'Output file path: ' outfile

while read word1 word2; do
        val=$(curl "http://api.conceptnet.io/relatedness?node1=/c/en/$word1&node2=/c/en/$word2" | jq '.value')
        echo "$word1" "$word2" "$val"
        sleep 1
    done < "$infile" > "$outfile"
