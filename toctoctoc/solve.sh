#!/bin/bash

set -x

if [ "$#" -ne 1 ]; then
    HOST=127.0.0.1
else
    HOST=$1
fi

exec 3< <(echo 123123 | nc -q10 $HOST 30000 &)
sleep 1
echo "123123/pwned" | nc -q6 $HOST 30000

for i in 1 2 3; do read <&3 line; echo "$line"; done
