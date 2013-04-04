#!/usr/bin/env bash

username=$1

if [ -n "$2" ]; then
    type=$2
else
    type="favorite"
fi

numPages=$(curl -s "http://xhamster.com/user/video/$username/$type-1.html" | sed 's/</\n</g' | grep -i "$type" | grep -i 'next' -B1 | tail -n2 | head -n1 | sed 's/^<.*>//')
if [ -z $(echo "$numPages" | grep -o '[0-9]\{1,\}') ]; then
    # They probably only have 1 page.
    numPages=1
fi

if [ -z "$numPages" ]; then
    echo "error: unable to find number of pages for user '$username'" 1>&2
    exit 1
fi

i=1
while [ $i -le $numPages ]; do
    echo "Page $i / $numPages"
    urls=$(echo -e "$urls\n" && curl -s "http://xhamster.com/user/video/$username/$type-$i.html" | sed 's/</\n</g' | grep 'href="/movies/' | sed 's/^.*href="\([^"]\{1,\}\).*/http:\/\/xhamster.com\1/g')
    i=$(($i + 1))
done

echo -e "$urls" > urls.txt
echo "$urls"

