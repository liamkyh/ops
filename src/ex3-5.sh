#!/bin/sh
parameter="$1"
myFunction (){
    echo "함수 안으로 들어왔음"
    fun_parameter="$1"
    list="ls $fun_parameter"
    echo $($list)
}
echo "프로그램을 시작합니다"
myFunction "$parameter"
echo "프로그램을 종료합니다"
exit 0
