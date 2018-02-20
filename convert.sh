#!/bin/bash
# Converts from twecoll output to one accepted by tweeter.py
# example usage: ./convert.sh horse/Horse_ebooks.txt > horse/Horse_ebooks.csv
awk 'BEGIN{print "date|text"} {$7 = "|" $7; print $0}' $1

