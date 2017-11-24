var fs = require('fs');
var express = require('express');
var session = require('cookie-session'); // Charge le middleware de sessions
var bodyParser = require('body-parser'); // Charge le middleware de gestion des paramètres
var urlencodedParser = bodyParser.urlencoded({ extended: false });
var morgan = require('morgan'); // Charge le middleware de logging
var favicon = require('serve-favicon'); // Charge le middleware de favicon
var multer  = require('multer')
var JsonDB = require('node-json-db');


var app = express();
var data = fs.readFileSync('data/france_final.json', 'utf8');
var jsondata = JSON.parse(data);

var data_dir = process.env.OPENSHIFT_DATA_DIR || '../data/';
var photos_dir = data_dir + "/photos/";
console.log("process.env.OPENSHIFT_DATA_DIR: "+process.env.OPENSHIFT_DATA_DIR);
console.log("DATA_DIR: " + data_dir);
var upload = multer({ dest: photos_dir })

var db;
try {
  db = new JsonDB(data_dir + "/calendar-peskine", true, true);
} catch (e) {
  console.log(e);
  db = new JsonDB("data/calendar-peskine", true, true);
}

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
  res.contentType('application/json');
  try {
    if (req.params.filter != 'undefined') {
      console.log("filter:" + req.params.filter);
    }
    
    var daydone = db.getData('/');
    for (var d in daydone)
    {
      if (d in jsondata)
      {
        jsondata[d] = true;
      }
    }
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
    res.contentType('application/json');
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

  .post('/addresses/done/:month_day', upload.single('file'), function (req, res, next) {
    // todo : handle uploaded picture
    if (req.params.month_day != "undefined") {
      var email = req.body.email;
      var tmp_path = req.file.path;
      var target_path = photos_dir + req.params.month_day + req.file.originalname;
      var src = fs.createReadStream(tmp_path);
      var dest = fs.createWriteStream(target_path);
      console.log("email: " + email);      
      src.pipe(dest);
      src.on('end', function() { 
        db.push("/" + req.params.month_day, email, true);
        res.redirect('/'); 
      });
      //src.on('error', function(err) { res.render('error'); });
    } else {
      res.redirect('/');
    }
    res.redirect('/');
  })
  
  
  .use(function (req, res, next) {
    res.redirect('/');
  });

var server_port = process.env.PORT || process.env.OPENSHIFT_NODEJS_PORT || 8080;
var server_ip   = process.env.IP   || process.env.OPENSHIFT_NODEJS_IP || '0.0.0.0';
app.listen(server_port, server_ip);