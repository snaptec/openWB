#!/bin/bash
#echo "tail $1"
ls $1 -l
echo "$(tail -1000 $1)" > $1
