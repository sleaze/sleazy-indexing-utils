#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "usage: $0 [filter-name-or-'all'] [limit-num-pages] [start-page?]" 1>&2
    exit 1
fi

if [ -n "$1" ] && [ "$1" != '*' ] && [ "$1" != 'all' ]; then
    filters=$1
    echo "info: user specified filter(s): $filters" 1>&2
else
    filters='straight shemale gay'
    echo "info: defaulting to all filters: $filters" 1>&2
fi

if [ -n "$3" ]; then
    startPage=$3
    echo "info: user specified starting page: $startPage" 1>&2
fi

if [ -n "$2" ]; then
    if [ -n "$startPage" ]; then
        pageLimit=$(($2 + $startPage))
    else
        pageLimit=$2
    fi
    echo "info: user specified page limit: $pageLimit" 1>&2
else
    pageLimit=100
    echo "info: defaulting page limit: $pageLimit" 1>&2
fi

cd "$(dirname $0)"


for filter in $filters; do
    echo "info: filter=$filter" 1>&2
    if [ -n "$startPage" ]; then
        nextUrl="http://xhamster.com/new/$startPage.html"
        page=$startPage
    else
        nextUrl='http://xhamster.com'
        page=1
    fi
    while [ -n "$nextUrl" ] && [ $page -le $pageLimit ]; do
        echo "info: next url: $nextUrl (page: $page limit: $pageLimit)" 1>&2

        html=$(curl \
            "$nextUrl" \
            --silent \
            -H"User-Agent: $(cat res/ua/chrome24)" \
            -H"Referer: http://xhamster.com/" \
            -H"Origin: http://xhamster.com" \
            -H"Content-Type: application/x-www-form-urlencoded" \
            -H"Host: xhamster.com" \
            -H"Cache-Control: max-age=0" \
            -XPOST \
            -d"content=$filter" | \
            sed 's/</\n</g' | \
            sed "s/^[ \t]\{1,\}//g" | \
            tr "'" '"')

        echo -e "$html" | \
            awk '/<div id="footer">/{flag=0}flag;/New Porn Videos/{flag=1}' | \
            grep 'href="[^"]*movies.*' | \
            sed 's/^.*href *= *"\(https\?:\/\/xhamster.com\)\?\(\/movies[^"]\{1,\}\).*$/http:\/\/xhamster.com\2/g'

        next=$(echo -e "$html" | \
            grep 'href *= *"\(https\?:\/\/xhamster.com\)\?\/new' | \
            grep -i 'next' | \
            sed 's/^.*href *= *"\([^"]\{1,\}\).*$/\1/')

        if [ -z "$next" ]; then
            nextUrl=''
        else
            nextUrl="http://xhamster.com$next"
        fi
        page=$(($page + 1))
    done
done




