var fs = require('fs');
var express = require('express');
var session = require('cookie-session'); // Charge le middleware de sessions
var bodyParser = require('body-parser'); // Charge le middleware de gestion des paramètres
var urlencodedParser = bodyParser.urlencoded({ extended: false });
var morgan = require('morgan'); // Charge le middleware de logging
var favicon = require('serve-favicon'); // Charge le middleware de favicon

var app = express();
app.use(session({secret: 'calendarsessionsecret'}))

  .use(morgan('combined')) 
  .use(express.static(__dirname + '/public')) 
  .use(favicon(__dirname + '/public/favicon.ico'))
  .use(function(req, res, next) {
    if (typeof(req.session.todolist) == 'undefined') {
      req.session.todolist = [];
    }
    next();
  });
app.get('/', function(req, res) {
  res.render('index.ejs');
})

app.get('/addresses', function(req, res) {
  // get list of address in a json object
  //res.render('todolist.ejs', {todolist: req.session.todolist});
  try {  
    var data = fs.readFileSync('data/france.json', 'utf8');
    console.log(data);    
    res.write(data);
    res.end()
  } catch(e) {
    console.log('Error:', e.stack);
  }
})

  .post('/addresses/add', urlencodedParser, function(reqfranceres) {
    // todo : add a new address
    res.redirect('/');
  })
  .get('/addresses/delete/:id', function(req, res) {
    // delete an address
    if (req.params.id != 'undefined' && !isNaN(req.params.id)) {
      ;//req.session.todolist.splice(req.params.id, 1);
    }
    res.redirect('/');
  })
  .use(function(req, res, next){
    res.redirect('/');
  });

app.listen(8080, 'localhost');