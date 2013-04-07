#!/usr/bin/env bash

cd "$(dirname $0)"

username=$1

if [ -n "$2" ]; then
    # e.g. "photo"
    typeOfContent=$2
else
    typeOfContent='video'
fi

# new or favorite?
if [ -n "$3" ]; then
    # e.g. "new"
    newOrFavorite=$3
else
    newOrFavorite='favorite'
fi

numPages=$( \
    curl -s "http://xhamster.com/user/$typeOfContent/$username/$newOrFavorite-1.html" \
        -H"User-Agent: $(cat res/ua/chrome24)" \
        -H"Referer: http://xhamster.com/" \
        -H"Origin: http://xhamster.com" \
        -H"Host: xhamster.com" | \
    tr "'" '"' | \
    sed 's/</\n</g' | \
    sed "s/^[ \t]\{1,\}//g" | \
    grep -i "$newOrFavorite" | \
    grep -B2 -i 'last' | \
    head -n2 | \
    tail -n1 | \
    grep -o '[0-9]\{1,\}$'
)

if [ -z "$numPages" ]; then
    # They probably only have 1 page..or the scraper is broken.
    numPages=1
fi

if [ -z "$numPages" ]; then
    echo "error: unable to find number of pages for user '$username'" 1>&2
    exit 1
fi

i=1
while [ $i -le $numPages ]; do
    echo "Page $i / $numPages" 1>&2
    #urls=$(echo -e "$urls\n" && curl -s "http://xhamster.com/user/$typeOfContent/$username/$newOrFavorite-$i.html" | sed 's/</\n</g' | grep 'href="/\(movies\|photos\)/' | sed 's/^.*href="\([^"]\{1,\}\).*/http:\/\/xhamster.com\1/g')
    echo -e "$( \
        curl -s "http://xhamster.com/user/$typeOfContent/$username/$newOrFavorite-$i.html" \
            -H"User-Agent: $(cat res/ua/chrome24)" \
            -H"Referer: http://xhamster.com/" \
            -H"Origin: http://xhamster.com" \
            -H"Host: xhamster.com" | \
        tr "'" '"' | \
        sed 's/</\n</g' | \
        sed "s/^[ \t]\{1,\}//g" | \
        grep 'href=".*/\(movies\|photos\)/.\{1,\}' | \
        sed 's/^.*href="\(https\?:\/\/xhamster\.com\)\?\([^"]\{1,\}\).*/http:\/\/xhamster.com\2/g' | \
        grep '^.*\(movies\|photos\)/.\{2,\}' | \
        grep -v '^\(.*#\|.*\/rankings\/.*\)$' \
    )"
    i=$(($i + 1))
done

#echo -e "$urls" > urls.txt
#echo "$urls"

