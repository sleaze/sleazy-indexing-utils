#!/usr/bin/env bash

inFile=$1

if ! [ -r "$inFile" ]; then
    echo 'error: invalid or unreadable input file specifiied' 1>&2
    echo "usage: ./$0 [input-file]" 1>&2
    exit 1
fi

cd $(dirname $0)

if ! [ -d 'gals' ]; then
    mkdir 'gals'
fi

if ! [ -d 'gals' ]; then
    echo 'error: unable to create directory "gals"' 1>&2
    exit 1
fi

data=$(cat "$inFile")

cd gals

export IFS=$'\n'
for line in $data; do
    if [ -n "$(echo $line | grep -o '^http:\/\/')" ]; then
        echo "Getting $line"
        wget -erobots=off -m -k -l1 --accept='*htm*,*jpg,*jpeg' --referer="$line" "$line"
    fi
done

