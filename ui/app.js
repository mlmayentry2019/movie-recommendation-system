var express = require('express');
var app = express();
var rp = require('request-promise');
var bodyParser = require("body-parser");

const host = 'localhost';
var userId = ''

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.set('view engine', 'pug');
app.set('views','./views');

app.get('/', async function(req, res) {
   try {
      var response = await rp(`http://${host}:5000/top_trend`);
      obj = JSON.parse(response);
      res.render('index', {name: obj.title});
   } catch(err) {
      console.error(err)
   }
});

app.get('/search', async function(req, res) {
   const movie = req.query.movie
   var options = {}
   if(userId) {
      options = {
         method: 'POST',
         uri: `http://${host}:5000/collaborative`,
         json: true,
         body: {
            userId: userId,
            title: movie
         }
      };
   } else {
      options = {
         method: 'POST',
         uri: `http://${host}:5000/content-based`,
         json: true,
         body: {
         title: movie
         }
      };
   }
   var response = await rp(options);
   console.log(response);
   return res.render('search', {similarMovies: response});
});

app.post('/login', async function(req, res) {
   userId = req.body.userId
   //TODO use forward instead of copy/paste
   try {
      var response = await rp(`http://${host}:5000/top_trend`);
      obj = JSON.parse(response);
      res.render('index', {name: obj.title});
   } catch(err) {
      console.error(err)
   }
});

app.get('/logout', async function(req, res) {
   userId = ''
   //TODO use forward instead of copy/paste
   try {
      var response = await rp(`http://${host}:5000/top_trend`);
      obj = JSON.parse(response);
      res.render('index', {name: obj.title});
   } catch(err) {
      console.error(err)
   }
});

app.listen(3000);