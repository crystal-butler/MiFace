#!/bin/bash
sed 's/\([^ ]*\).*/\1/' /Users/body_LAB/Desktop/miface/GloVe/eval/python/glove.6B.300d.txt | sed '/^$/d' >> glove.6B.vocab.txt