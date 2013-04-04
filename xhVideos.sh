#!/usr/bin/env bash

if [ -z "$1" ]; then
    filters='gay straight shemale'
    echo "Defaulting to all filters: $filters"
else
    filters=$1
    echo "User specified filters: $filters"
fi

cd "$(dirname $0)"

for filter in $filters; do
    echo "filter=$filter"
    curl --silent 'http://xhamster.com' \
        -H"User-Agent: $(cat res/ua/chrome24)" \
        -H"Referer: http://xhamster.com/" \
        -H"Origin: http://xhamster.com" \
        -H"Content-Type: application/x-www-form-urlencoded" \
        -H"Host: xhamster.com" \
        -H"Cache-Control: max-age=0" \
        -XPOST \
        -d"content=$filter" | \
        awk '/<div id="footer">/{flag=0}flag;/New Porn Videos/{flag=1}' | \
        sed "s/^[ \t]\{1,\}//g" | \
        grep 'href="' | \
        sed 's/^.*href="\(\/movies[^"]\{1,\}\).*/http:\/\/xhamster.com\1/g'
done




