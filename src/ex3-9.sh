#!/bin/sh

search_name="$1"
grep_result=$(grep -i "$search_name" DB.txt)
#검색이 된 경우
if [ -n "$grep_result" ]; then
  echo "$grep_result"
#검색이 되지 않은 경우
else
  echo "검색 결과를 찾을 수 없습니다."
fi
