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
	var request = new messages.ListChessPositionsRequest();
	request.setFenEncoding(req.query.fen);
	request.setPageSize(`${process.env.DEFAULT_PAGE_SIZE}`)
	if (typeof req.query.token != "undefined") {
		request.setPageToken(`${req.query.token}`)
	} else {
		request.setPageToken("")
	}

	var positions;

	client.listChessPositions(request, function(err, response) {
		var positionsPb = response.getPositionsList();
		var nextPageToken = response.getNextPageToken();

		positions = [];
		for (let positionPb of positionsPb) {
			positions.push({
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
			});
		}

		res.render('search', { title: 'CheSSE', queryFenEncoding: req.query.fen, positions: positions, nextPageToken: nextPageToken });
  	});
});

module.exports = router;
