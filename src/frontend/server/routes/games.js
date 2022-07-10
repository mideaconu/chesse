const express = require('express');
const grpc = require('@grpc/grpc-js');

var router = express.Router();

require('dotenv').config()

const services = require("../../chesse/v1alpha1/services_grpc_pb");
const messages = require("../../chesse/v1alpha1/backend_service_pb");
const pos = require("../../chesse/v1alpha1/positions_pb");

const client = new services.BackendServiceClient(
    `${process.env.BACKEND_SERVER_HOST}:${process.env.BACKEND_SERVER_PORT}`, 
    grpc.ChannelCredentials.createInsecure()
);


/* GET /games. */
router.get('/', function(req, res, next) {
	var request = new messages.ListChessGamesRequest();
	request.setFenEncoding(req.query.fen);
	request.setPageSize(50)//(`${process.env.DEFAULT_PAGE_SIZE}`)
	if (typeof req.query.token != "undefined") {
		request.setPageToken(`${req.query.token}`)
	} else {
		request.setPageToken("")
	}

	var games = [];
    client.listChessGames(request, function(err, response) {
        if (err) {
            // TODO
        } else {
            var gamesPb = response.getGamesList();
            var nextPageToken = response.getNextPageToken();
            for (let gamePb of gamesPb) {
                games.push({
                    id: gamePb.getId(),
                    context: {
                        event: gamePb.getContext().getEvent(),
                        date: gamePb.getContext().getDate(),
                        site: gamePb.getContext().getSite(),
                        round: gamePb.getContext().getRound(),
                    },
                    white: {
                        name: gamePb.getWhite().getName(),
                        elo: gamePb.getWhite().getElo(),
                    },
                    black: {
                        name: gamePb.getBlack().getName(),
                        elo: gamePb.getBlack().getElo(),
                    },
                    moves: gamePb.getMovesList().map(
                        move => { 
                            return { uci: move.getUci(), san: move.getSan(), fen: move.getFen() };
                        }
                    ),
                    result: gamePb.getResult(),
                });
            }
            res.locals.games = games
            res.locals.nextPageToken = nextPageToken
            next();
		}
  	});
}, (req, res) => {
    var request = new messages.GetChessPositionRequest();
    request.setFenEncoding(req.query.fen);

    var position;
    client.getChessPosition(request, function(err, response) {
        if (err) {
            // TODO
        } else {
            var positionPb = response.getPosition();
            console.log(positionPb.getFenEncoding());
            position = {
                fenEncoding: positionPb.getFenEncoding(),
                stats: {
                    nrGames: positionPb.getPositionStats().getNrGames(),
                    rating: {
                        min: positionPb.getPositionStats().getRatingStats().getMin(),
                        avg: positionPb.getPositionStats().getRatingStats().getAvg(),
                        max: positionPb.getPositionStats().getRatingStats().getMax(),
                    },
                    result: {
                        whiteWinPct: positionPb.getPositionStats().getResultStats().getWhiteWinPct(),
                        drawPct: positionPb.getPositionStats().getResultStats().getDrawPct(),
                        blackWinPct: positionPb.getPositionStats().getResultStats().getBlackWinPct(),
                    }
                }
            };
        }
        res.render('games', { title: 'CheSSE', position: position, games: res.locals.games, nextPageToken: res.locals.nextPageToken });
    });
});

/* GET /games/{gameId}. */
router.get('/:gameId', function(req, res) {
	var request = new messages.GetChessGameRequest();
	request.setGameId(req.params.gameId);

    var game;
	client.getChessGame(request, function(err, response) {
		var gamePb = response.getGame();
        game = {
            id: gamePb.getId(),
            context: {
                event: gamePb.getContext().getEvent(),
                date: gamePb.getContext().getDate(),
                site: gamePb.getContext().getSite(),
                round: gamePb.getContext().getRound(),
            },
            white: {
                name: gamePb.getWhite().getName(),
                elo: gamePb.getWhite().getElo(),
            },
            black: {
                name: gamePb.getBlack().getName(),
                elo: gamePb.getBlack().getElo(),
            },
            moves: gamePb.getMovesList().map(
                move => { 
                    return { uci: move.getUci(), san: move.getSan(), fen: move.getFen() };
                }
            ),
            result: gamePb.getResult()
        };

        res.render('game', { title: 'CheSSE', game: game });
    });
});

module.exports = router;
