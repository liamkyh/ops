#!/bin/sh
weight=$1
height=$2
BMI=$(echo "$weight * 10000 / ($height * $height)" | bc)
#echo "안녕하세요"
#echo "$BMI"
#전체 주석을 쳐보고 각문장 당 주석을 풀어보면서 값을 출력시켜본다.

if [ $( echo "$BMI >= 18.5" | bc) -eq 1 ] && [ $BMI -lt 23 ]
then
    echo "정상 체중입니다."
elif [ $( echo "$BMI < 18.5" | bc) -eq 1 ]
then
    echo "저체중입니다."
else
    echo "과체중입니다."
fi
exit 0
