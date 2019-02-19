#!/bin/bash

for file in /data/sam676/TrialOne/TESTFOLDER/*
do
	python distance2.py --vocab_file=glove.6B.vocab.txt --vectors_file=glove.6B.300d.txt < $file > $file.out.txt

done