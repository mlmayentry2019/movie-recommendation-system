var express = require('express');
var app = express();
var rp = require('request-promise');


app.set('view engine', 'pug');
app.set('views','./views');

app.get('/', async function(req, res) {
   try {
      var response = await rp("http://localhost:5000/top_trend");
      obj = JSON.parse(response);
      res.render('home', {name: obj.title});
   } catch(err) {
      console.error(err)
   }
});

app.listen(3000);