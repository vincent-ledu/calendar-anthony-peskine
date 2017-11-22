var fs = require('fs');
var express = require('express');
var session = require('cookie-session'); // Charge le middleware de sessions
var bodyParser = require('body-parser'); // Charge le middleware de gestion des paramètres
var urlencodedParser = bodyParser.urlencoded({ extended: false });
var morgan = require('morgan'); // Charge le middleware de logging
var favicon = require('serve-favicon'); // Charge le middleware de favicon
var JsonDB = require('node-json-db');
var db = new JsonDB("data/calendar-peskine", true, true);


var app = express();
var data = fs.readFileSync('data/france_final.json', 'utf8');
var jsondata = JSON.parse(data);

app.use(session({ secret: 'calendarsessionsecret' }))

  .use(morgan('combined'))
  .use(express.static(__dirname + '/public'))
  .use(favicon(__dirname + '/public/favicon.ico'))
  .use(function (req, res, next) {
    if (typeof (req.session.todolist) == 'undefined') {
      req.session.todolist = [];
    }
    next();
  });
app.get('/', function (req, res) {
  res.render('index.ejs');
})
app.get('/calendar', function (req, res) {
  res.render('calendar.ejs');
})

app.get('/addresses', function (req, res) {
  // get list of address in a json object
  //res.render('todolist.ejs', {todolist: req.session.todolist});
  try {
    if (req.params.filter != 'undefined') {
      console.log("filter:" + req.params.filter);
    }
    console.log(req.query);
    console.log(req.url);
    
    var daydone = db.getData('/');
    console.log(daydone);
    for (var d in daydone)
    {
      if (d in jsondata)
      {
        jsondata[d] = true;
      }
    }
    //console.log(data);
    res.write(JSON.stringify(jsondata));
    res.end();
  } catch (e) {
    console.log('Error:', e.stack);
  }
})
app.get('/addresses/filter/:filter', function (req, res) {
  // get list of address in a json object
  //res.render('todolist.ejs', {todolist: req.session.todolist});
  try {
    if (req.params.filter != 'undefined')
    {
      var filter = req.params.filter;
      //var data = fs.readFileSync('data/france_final.json', 'utf8');
      
      var result = {};
      var f = filter.split('f');
      for (var i = 0; i < f.length; i++) {
        result[f[i]] = jsondata[f[i]];
      }

      res.write(JSON.stringify(result));
      res.end();
    } else {
      res.write("[]");
      res.end();
    }
  } catch (e) {
    console.log('Error:', e.stack);
    res.write("[]");
    res.end();
  }
})
  .get('/addresses/done/:month_day', function (req, res) {
    // todo : update address to done
    if (req.params.month_day != "undefined") {
      db.push("/" + req.params.month_day, true, true);
    }
    res.redirect('/');
  })
  
  
  .use(function (req, res, next) {
    res.redirect('/');
  });

app.listen(8080, 'localhost');