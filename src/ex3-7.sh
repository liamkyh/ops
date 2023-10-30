#!/bin/sh
file_name="$1"

if [ -e "$file_name" ]; then
    echo "파일 '$file_name'이 이미 존재합니다."
else
    mkdir "$file_name"
fi

cd "$file_name"
for i in 0 1 2 3 4
do
    touch "file"$i".txt"
    mkdir "file"$i""
    cd "file"$i""
    ln -s ~/git/src/"$file_name"/"file"$i".txt" ~/git/src/"$file_name"/"file"$i""/"file"$i".txt"
    cd "-"
done
