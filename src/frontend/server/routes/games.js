const express = require('express');

var router = express.Router();

const services = require('../../../protobufs/gen/js/chesse_backend_api/v1alpha1/chesse_grpc_pb');
const messages = require('../../../protobufs/gen/js/chesse_backend_api/v1alpha1/chesse_pb');
const pos = require('../../../protobufs/gen/js/chesse_backend_api/v1alpha1/positions_pb');
const grpc = require('@grpc/grpc-js');

require('dotenv').config()

const client = new services.CheSSEBackendServiceClient(`localhost:${process.env.BACKEND_API_PORT}`, grpc.ChannelCredentials.createInsecure());

/* GET /games. */
router.get('/', function(req, res, next) {
	console.log(req.query.fen);

	var position = new pos.Position();
	position.setFen(req.query.fen);
	var request = new messages.GetGamesRequest();
	request.setPosition(position);

	var games;
    var stats;

	client.getGames(request, function(err, response) {
		var games_pb = response.getGamesList();
        var stats_pb = response.getStats();
        stats = {
            nr_games: stats_pb.getNrGames(),
            rating: {
                min: stats_pb.getRatingStats().getMin(),
                avg: stats_pb.getRatingStats().getAvg(),
                max: stats_pb.getRatingStats().getMax(),
            },
            result: {
                white: stats_pb.getResultStats().getWhite(),
                draw: stats_pb.getResultStats().getDraw(),
                black: stats_pb.getResultStats().getBlack(),
            }
        };
		games = [];
		for (let game_pb of games_pb) {
			games.push({
				id: game_pb.getId(),
                context: {
                    event: game_pb.getContext().getEvent(),
                    date: game_pb.getContext().getDate(),
                    site: game_pb.getContext().getSite(),
                    round: game_pb.getContext().getRound(),
                },
                white: {
                    name: game_pb.getWhite().getName(),
                    elo: game_pb.getWhite().getElo(),
                },
                black: {
                    name: game_pb.getBlack().getName(),
                    elo: game_pb.getBlack().getElo(),
                },
                result: game_pb.getResult(),
                nr_moves: game_pb.getNrMoves()
			});
		}

        console.log(stats);
		console.log(games);

		res.render('games', { title: 'CheSSE', fen: req.query.fen, stats: stats, games: games });
  	});
});

/* GET /games/{gameId}. */
router.get('/:gameId', function(req, res, next) {
	var request = new messages.GetGameRequest();
	request.setGameId(req.params.gameId);

    var game;

	client.getGame(request, function(err, response) {
		var game_pb = response.getGame();
        game = {
            id: game_pb.getId(),
            context: {
                event: game_pb.getContext().getEvent(),
                date: game_pb.getContext().getDate(),
                site: game_pb.getContext().getSite(),
                round: game_pb.getContext().getRound(),
            },
            white: {
                name: game_pb.getWhite().getName(),
                elo: game_pb.getWhite().getElo(),
            },
            black: {
                name: game_pb.getBlack().getName(),
                elo: game_pb.getBlack().getElo(),
            },
            result: game_pb.getResult(),
            nr_moves: game_pb.getNrMoves()
        };

		console.log(game);

        res.render('game', { title: 'CheSSE', game: game });
  	});
});

module.exports = router;
