var fs = require('fs');
var express = require('express');
var session = require('cookie-session'); // Charge le middleware de sessions
var bodyParser = require('body-parser'); // Charge le middleware de gestion des paramètres
var urlencodedParser = bodyParser.urlencoded({ extended: false });
var morgan = require('morgan'); // Charge le middleware de logging
var favicon = require('serve-favicon'); // Charge le middleware de favicon
var multer  = require('multer')
var JsonDB = require('node-json-db');
var Jimp = require("jimp");

var app = express();

var data_dir = process.env.DATA_DIR || process.env.OPENSHIFT_DATA_DIR || 'data/';
console.log("DATA_DIR: " + data_dir);
var photos_dir = data_dir + "/photos/";
var data = fs.readFileSync(data_dir + '/france_final.json', 'utf8');
var jsondata = JSON.parse(data);
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
  .use(express.static(photos_dir))
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
      jsondata[d] = daydone[d];
    }
    res.write(JSON.stringify(jsondata));
    res.end();
  } catch (e) {
    console.log('Error:', e.stack);
  }
})
app.get('/addresses/filter/:filter', function (req, res) {
  // get list of address in a json object
  try {
    res.contentType('application/json');
    if (req.params.filter != 'undefined')
    {
      var filter = req.params.filter;
      
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
 


  .post('/addresses/done/:month_day', upload.single('imagefile'), function (req, res, next) {
    // todo : handle uploaded picture
    if (req.params.month_day != "undefined" && req.params.idlocation != "undefined") {
      console.log("req.params.idlocation:" + req.params.idlocation)
      var email = req.body.email;
      var filename = req.file.originalname;
      var idlocation = req.params.idlocation;
      var tmp_path = req.file.path;
      var target_filename = req.params.month_day + filename.substr(filename.lastIndexOf('.'));
      var target_thumb_filename = req.params.month_day + "_thumb" + filename.substr(filename.lastIndexOf('.'));
      if (target_thumb_filename.endsWith(".gif"))
        target_thumb_filename += ".jpg";      
      var target_thumb_path = photos_dir + target_thumb_filename;
      var target_path = photos_dir + target_filename;
      var src = fs.createReadStream(tmp_path);
      var dest = fs.createWriteStream(target_path);
      src.pipe(dest);
      
      

      src.on('end', function() { 
        console.log("target_path: "+target_path);
        console.log("target_thumb_path: "+target_thumb_path);
        // open a file called "lenna.png" 
        try {
          Jimp.read(target_path, function (err, image) {
            if (err) throw err;
              target_thumb_filename += ".jpg";
            image.resize(256, 256)            // resize 
                .write(target_thumb_path); // save 
            
          });
          db.push("/" + req.params.month_day, JSON.parse('{"email": "'+email+'", "id":"'+idlocation+
          '", "filename":"'+target_filename+'", "thumbnail":"'+target_thumb_filename+'"}'), true);

        } catch (e) {
          console.log("gasp! Error in saving thumbnails! Error: " + e);
          // redirect to an exlicit error page!
        }
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
var server_port = process.env.PORT || process.env.OPENSHIFT_NODEJS_PORT || 3001;
var server_ip   = process.env.IP   || process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1';
console.log("listening to " + server_ip+":" + server_port);
app.listen(server_port, server_ip);