#!/bin/bash

for f in "$1"/*
    do (cat $f; echo) >> $2
done
