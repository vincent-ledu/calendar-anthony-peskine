# Calendar-anthony-peskine

A Google map to inventory all streets/places/squares... with a date in its name.
The map gives locations of such streets/places/squares... 

# Data

Datas have been downloaded from https://bano.openstreetmap.fr/data/ (full.sjson file), then processed with scripts:
* data/get_address_json_v2.sh: Shell script that parse file and extract street with a date in it.
* data/quality_enhance.py: python script that parse street name, attempt to recognize date and add it to dataset (france_final.json)

for example: 
```
cd data/
wget https://bano.openstreetmap.fr/data/full.sjson.gz
gunzip full.sjson.gz
./get_address_json_v2.sh > france_month_piped_grepword.json
## remove last comma at the end of the file
python3 quality_enhance.py france_month_piped_grepword.json france_final.json
sed -i 's/{"done": false, "streets": /test/g' france_final.json
sed -i 's/}]}/}]/g' france_final.json
```

# Requirements

* To run the app:
  * NodeJs (see Installation instructions)
* To use data extractor
  * python binaries (tested with v3.4 and v3.6)
  * bash shell interpreter (linux, macOS, mobaxterm)
  * jq sudo apt-get install jq

# Installation instructions

* Download and install git on your computer : https://git-scm.com/download
* Download and install nodejs : https://nodejs.org/en/download/
* Create your own google api key: https://developers.google.com/maps/documentation/javascript/get-api-key?hl=Fr 
* In file calendar-anthony-peskine/views/index.ejs:
  * Search at the bottom of the file the line with 
  ```javascript
   <script async defer src="https://maps.googleapis.com/maps/api/js?key=<GOOGLE_API_KEY>&callback=initMap">
  ```
  and put your google api key here.
* In a terminal, 
  * type : ```git clone https://github.com/vincent-ledu/calendar-anthony-peskine.git```
  * type : ```cd calendar-anthony-peskine```
  * type : ```npm install```
  * type : ```npm install pm2```
  * type : ```pm2 start index.js```
  * in your favorite browser, go to http://localhost:3001

# Screenshot
![Screenshot](public/screenshot1.jpg)

