#!/bin/sh
file_name="$1"

if [ -e "$file_name" ]; then
    echo "파일 '$file_name'이  이미 존재합니다"
else
    mkdir "$file_name"
fi

cd "$file_name"
for i in 0 1 2 3 4
do
    touch "file"$i".txt"
done
#파일을 생성한 이후에 for반복문을 이용하여 file0~4.txt를 압축하고
tar -cvf "$file_name".tar file0.txt file1.txt file2.txt file3.txt file4.txt
echo  "$file_name.tar"
#그안에 새로운 파일을 만든 다음에 그 파일에 전에 압축했던 것을 내가 원하는 폴더 위치에 압축풀기를 했다.
mkdir "$file_name"
cd "$file_name"
tar -xvf ~/git/src/"$file_name"/"$file_name".tar -C ~/git/src/"$file_name"/"$file_name"
