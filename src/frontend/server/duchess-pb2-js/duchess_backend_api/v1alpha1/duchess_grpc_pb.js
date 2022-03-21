// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var duchess_backend_api_v1alpha1_games_pb = require('./games_pb.js');

function serialize_duchess_backend_api_v1alpha1_GetSimilarGamesRequest(arg) {
  if (!(arg instanceof duchess_backend_api_v1alpha1_games_pb.GetSimilarGamesRequest)) {
    throw new Error('Expected argument of type duchess_backend_api.v1alpha1.GetSimilarGamesRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_duchess_backend_api_v1alpha1_GetSimilarGamesRequest(buffer_arg) {
  return duchess_backend_api_v1alpha1_games_pb.GetSimilarGamesRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_duchess_backend_api_v1alpha1_GetSimilarGamesResponse(arg) {
  if (!(arg instanceof duchess_backend_api_v1alpha1_games_pb.GetSimilarGamesResponse)) {
    throw new Error('Expected argument of type duchess_backend_api.v1alpha1.GetSimilarGamesResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_duchess_backend_api_v1alpha1_GetSimilarGamesResponse(buffer_arg) {
  return duchess_backend_api_v1alpha1_games_pb.GetSimilarGamesResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


// Duchess Backend Service
var DuchessBackendServiceService = exports.DuchessBackendServiceService = {
  // Fetch a collection of games
getSimilarGames: {
    path: '/duchess_backend_api.v1alpha1.DuchessBackendService/GetSimilarGames',
    requestStream: false,
    responseStream: false,
    requestType: duchess_backend_api_v1alpha1_games_pb.GetSimilarGamesRequest,
    responseType: duchess_backend_api_v1alpha1_games_pb.GetSimilarGamesResponse,
    requestSerialize: serialize_duchess_backend_api_v1alpha1_GetSimilarGamesRequest,
    requestDeserialize: deserialize_duchess_backend_api_v1alpha1_GetSimilarGamesRequest,
    responseSerialize: serialize_duchess_backend_api_v1alpha1_GetSimilarGamesResponse,
    responseDeserialize: deserialize_duchess_backend_api_v1alpha1_GetSimilarGamesResponse,
  },
};

exports.DuchessBackendServiceClient = grpc.makeGenericClientConstructor(DuchessBackendServiceService);
