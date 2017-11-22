# calendar-anthony-peskine

A map to follow calendar activity.

# Installation instructions

* Download and install git on your computer : https://git-scm.com/download
* Download and install nodejs : https://nodejs.org/en/download/
* Create your own google api key: https://developers.google.com/maps/documentation/javascript/get-api-key?hl=Fr 
* In file calendar-anthony-peskine/views/index.ejs:
  * Search at the bottom of the file the line with 
  ```javascript
   <script async defer src="https://maps.googleapis.com/maps/api/js?key={your google api key here}&callback=initMap">
  ```
  and put your google api key here.
* In a terminal, 
  * type : ```git clone https://github.com/vincent-ledu/calendar-anthony-peskine.git```
  * type : ```cd calendar-anthony-peskine```
  * type : ```npm install```
  * type : ```npm install pm2```
  * type : ```pm2 start index.js```
  * in your favorite browser, go to http://localhost:8080

# Screenshot
![Screenshot](public/screenshot1.jpg)
