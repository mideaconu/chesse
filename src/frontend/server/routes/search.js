const express = require('express');
const grpc = require('@grpc/grpc-js');

var router = express.Router();

require('dotenv').config()

const services = require("../../chesse/v1alpha1/services_grpc_pb");
const messages = require("../../chesse/v1alpha1/backend_service_pb");

const client = new services.BackendServiceClient(
	`${process.env.BACKEND_SERVER_HOST}:${process.env.BACKEND_SERVER_PORT}`, 
	grpc.ChannelCredentials.createInsecure()
);


/* GET /search. */
router.get('/', function(req, res, next) {
	var request = new messages.GetChessPositionsRequest();
	request.setFenEncoding(req.query.fen);

	var positions;

	client.getChessPositions(request, function(err, response) {
		var positions_pb = response.getPositionsList();

		positions = [];
		for (let position_pb of positions_pb) {
			positions.push({
				fen_encoding: position_pb.getFenEncoding(),
				stats: {
					nr_games: position_pb.getPositionStats().getNrGames(),
					rating: {
						min: position_pb.getPositionStats().getRatingStats().getMin(),
						avg: position_pb.getPositionStats().getRatingStats().getAvg(),
						max: position_pb.getPositionStats().getRatingStats().getMax(),
					},
					result: {
						white_win_pct: position_pb.getPositionStats().getResultStats().getWhiteWinPct(),
						draw_pct: position_pb.getPositionStats().getResultStats().getDrawPct(),
						black_win_pct: position_pb.getPositionStats().getResultStats().getBlackWinPct(),
					}
				}
			});
		}

		res.render('search', { title: 'CheSSE', query_fen_encoding: req.query.fen, positions: positions });
  	});
});

module.exports = router;
