#!/usr/bin/env bash


if [ -z "$1" ]; then
    echo 'error: missing required parameter: tag' 1>&2
    echo "usage: $0 [complete_html_starting_tag]" 1>&2
    exit 1
fi

startTag=$(echo "$1" | tr "\t" ' ' | sed 's/<\|>//g')
endTag=$(echo "$startTag" | sed 's/^\([^ ]*\)\( .*\)\+$/\/\1/')

echo $startTag
echo $endTag

echo '---'

#echo '<hi id="5"><hello>inner</hello></hi>' | awk -F'[<>]' -v taga="$startTag" -v tagb="$endTag" '{ i=1; while (i<=NF) { if ($(i)==taga && $(i+2)==tagb) { print $(i+1) }; i++} }' 
# > "${2:-/dev/stdout}"

echo '<HTML><hi id="5"><hello>inner</hello></hi></html>' | awk -F'[<>]' -v taga="$startTag" -v tagb="$endTag" '{ i=1; while (i<=NF) { if ($(i)==taga && $(i+2)==tagb) { print $(i+1) }; i++} }'

