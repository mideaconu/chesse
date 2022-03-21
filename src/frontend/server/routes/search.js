const express = require('express');

var router = express.Router();

const services = require('../duchess-pb2-js/duchess_backend_api/v1alpha1/duchess_grpc_pb');
const messages = require('../duchess-pb2-js/duchess_backend_api/v1alpha1/games_pb');
const grpc = require('@grpc/grpc-js');

const client = new services.DuchessBackendServiceClient('localhost:50051', grpc.credentials.createInsecure());

/* GET /search. */
router.get('/', function(req, res, next) {
	console.log(req.query.fen);

	var request = new messages.GetSimilarGamesRequest();
	request.setPositionFen(req.query.fen);

	var games;

	client.getSimilarGames(request, function(err, response) {
		var games_pb = response.getGamesList();
		games = [];
		for (let game_pb of games_pb) {
			games.push({
				id: game_pb.getId(),
				position_fen: game_pb.getPosition().getFen()
			});
		}

		res.render('search', { title: 'DUChess', fen: req.query.fen, games: games });
  	});
});

module.exports = router;