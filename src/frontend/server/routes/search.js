const express = require('express');

var router = express.Router();

const services = require('../chesse-pb2-js/chesse_backend_api/v1alpha1/chesse_grpc_pb');
const messages = require('../chesse-pb2-js/chesse_backend_api/v1alpha1/chesse_pb');
const pos = require('../chesse-pb2-js/chesse_backend_api/v1alpha1/positions_pb');
const grpc = require('@grpc/grpc-js');

const client = new services.CheSSEBackendServiceClient('localhost:50051', grpc.credentials.createInsecure());

/* GET /search. */
router.get('/', function(req, res, next) {
	console.log(req.query.fen);

	var position = new pos.Position();
	position.setFen(req.query.fen);
	var request = new messages.GetSimilarPositionsRequest();
	request.setPosition(position);

	var positions;

	client.getSimilarPositions(request, function(err, response) {
		var similar_positions_pb = response.getSimilarPositionsList();
		positions = [];
		for (let position_pb of similar_positions_pb) {
			positions.push({
				fen: position_pb.getPosition().getFen(),
				similarity_score: position_pb.getSimilarityScore(),
				stats: {
					nr_games: position_pb.getPositionStats().getNrGames(),
					rating: {
						min: position_pb.getPositionStats().getRatingStats().getMin(),
						avg: position_pb.getPositionStats().getRatingStats().getAvg(),
						max: position_pb.getPositionStats().getRatingStats().getMax(),
					},
					result: {
						white: position_pb.getPositionStats().getResultStats().getWhiteWinPct(),
						draw: position_pb.getPositionStats().getResultStats().getDrawPct(),
						black: position_pb.getPositionStats().getResultStats().getBlackWinPct(),
					}
				}
			});
		}

		console.log(positions);

		res.render('search', { title: 'DUChess', fen: req.query.fen, positions: positions });
  	});
});

module.exports = router;
