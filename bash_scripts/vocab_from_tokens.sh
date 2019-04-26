#!/bin/bash

cat "$1" | tr " " "\n" > /tmp/temp.txt
sort /tmp/temp.txt | uniq > $2
rm /tmp/temp.txt
