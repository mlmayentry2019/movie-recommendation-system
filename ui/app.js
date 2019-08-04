var express = require('express');
var app = express();
var rp = require('request-promise');

const host = 'localhost';

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
   console.log(req.query.movie)

   var options = {
      method: 'POST',
      uri: `http://${host}:5000/content-based`,
      json: true,
      body: {
         title: movie
     },
  };

   var response = await rp(options);
   console.log(response);
   return res.render('search', {similarMovies: response});
});

app.listen(3000);