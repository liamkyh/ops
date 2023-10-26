#!/bin/sh
f_number=$1
s_number=$3
operator=$2
if [ "$operator" = "+" ]
then
    op_number=`expr $f_number + $s_number`
    echo $op_number
else
    op_number=`expr $f_number - $s_number`
    echo $op_number
fi
exit 0

