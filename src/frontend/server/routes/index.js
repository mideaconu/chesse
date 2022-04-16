const express = require('express');
var router = express.Router();

/* GET /. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'CheSSE' });
});

module.exports = router;
