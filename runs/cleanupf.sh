#!/bin/bash
# ls "$1" -l
echo "$(tail -2000 $1)" >"$1"
