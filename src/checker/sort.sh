#!/bin/bash

target=${1:-tests}

cd "$(dirname "$0")/$target"

for i in *.a *.u
do
    if [ $i -nt $i.sorted ]
        then
        echo "Creating $i.sorted from $i"
        sort $i > $i.sorted
    fi
done
