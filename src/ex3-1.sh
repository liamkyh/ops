#!/bin/sh

count="$1"

for i in $(seq "$count")
do
    echo "hello world"
done

exit 0

