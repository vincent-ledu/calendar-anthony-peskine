#!/bin/bash

METHOD="PIPED"

declare -a arrmonths=("janvier" "février" "mars" "avril" "mai" "juin" "juillet" "août" "septembre" "octobre" "novembre" "décembre")
months="janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre"
numbers="0|1|2|3|4|5|6|7|8|9|premier|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente"

echo "["
if [ "$METHOD" == "UNPIPED" ]; then
	>&2 echo "UNPIPED METHOD"
	for month in "${arrmonths[@]}"; do
		>&2 echo "Processing $month"
#		cat full.sjson | awk -F "," 'tolower($3) ~ "janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre" { print $0 }' \
		cat full.sjson | grep -iw "$month" \
		| grep -vi "maison" \
		| awk -F "," 'tolower($3) ~ "0|1|2|3|4|5|6|7|8|9|premier|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente" { print $0 }' \
		| jq '. | "{\"name\":\"\(.name)\", \"city\": \"\(.city)\", \"region\":\"\(.region)\", \"country\":\"France\", \"lat\":\(.lat), \"lon\":\(.lon)}"' \
		|  sed 's/\"{/{/g' | sed 's/\\\"/\"/g' | sed 's/}\"/},/g'
	done
else
	>&2 echo "PIPED METHOD"
#	cat full.sjson | awk -F "," 'tolower($3) ~ "janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre" { print $0 }' \
	cat full.sjson | grep -iw "$months" \
		| grep -vi "maison" \
		| awk -F "," 'tolower($3) ~ "0|1|2|3|4|5|6|7|8|9|premier|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente" { print $0 }' \
		| jq '. | "{\"name\":\"\(.name)\", \"city\": \"\(.city)\", \"region\":\"\(.region)\", \"country\":\"France\", \"lat\":\(.lat), \"lon\":\(.lon)}"' \
		|  sed 's/\"{/{/g' | sed 's/\\\"/\"/g' | sed 's/}\"/},/g'
fi

echo "]"
