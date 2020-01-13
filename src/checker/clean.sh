#!/bin/bash

DIR=`dirname $0`
DIRS=$DIR/${1:-*}


FILTER='tests'
#FILTER=${FILTER/$1/}

find $DIRS -type d ! -name "$FILTER" | xargs -I {} rm -rf {}
find $DIRS -type f -name "*.sorted" -o -name "*.log" -o -name "*.+" -o -name "*.-" | xargs -I {} rm {}
