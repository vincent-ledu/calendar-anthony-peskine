#!/bin/bash

#declare -a months=("janvier")
declare -a months=("janvier" "février" "mars" "avril" "mai" "juin" "juillet" "août" "septembre" "octobre" "novembre" "décembre")
numbers="0|1|2|3|4|5|6|7|8|9|premier|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente"

echo "["
for month in ${months[@]}; do
	>&2 echo "Processing $month"
	cat full.sjson | grep -i " $month" \
	| awk -F "," 'tolower($3) ~ "0|1|2|3|4|5|6|7|8|9|premier|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt" { print $0 }' \
	| jq '. | "{\"name\":\"\(.name)\", \"city\": \"\(.city)\", \"region\":\"\(.region)\", \"country\":\"France\", \"lat\":\(.lat), \"lon\":\(.lon)}"' \
	|  sed 's/\"{/{/g' | sed 's/\\\"/\"/g' | sed 's/}\"/},/g'
done
#sed -i 's/\"{/{/g' france.json
#sed -i 's/\\\"/\"/g' france.json
#sed -i 's/}\"/},/g' france.json
echo "]"
