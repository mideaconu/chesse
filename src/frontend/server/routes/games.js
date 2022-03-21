const express = require('express');
var router = express.Router();

/* GET /games. */
router.get('/', function(req, res, next) {
  res.render('games', { title: 'DUChess', id: req.query.id });
});

module.exports = router;
