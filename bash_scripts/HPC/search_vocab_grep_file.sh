#!/bin/bash

outname=`basename "$1" | cut -f 3-5 -d '-'`
outpath="/scratch/cb2610/Common_Crawl/parallel_output/$outname.out"

grep -Fif <(awk '{print " "$0" "}' $HOME/MiFace/Python/vocab_files/vocab_checked.txt) "$1" >> $outpath	
