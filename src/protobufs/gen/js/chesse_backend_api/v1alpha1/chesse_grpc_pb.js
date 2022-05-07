// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var chesse_backend_api_v1alpha1_chesse_pb = require('../../chesse_backend_api/v1alpha1/chesse_pb.js');
var chesse_backend_api_v1alpha1_games_pb = require('../../chesse_backend_api/v1alpha1/games_pb.js');
var chesse_backend_api_v1alpha1_positions_pb = require('../../chesse_backend_api/v1alpha1/positions_pb.js');

function serialize_chesse_backend_api_v1alpha1_GetGameRequest(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetGameRequest)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetGameRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetGameRequest(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetGameRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetGameResponse(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetGameResponse)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetGameResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetGameResponse(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetGameResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetGamesRequest(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetGamesRequest)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetGamesRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetGamesRequest(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetGamesRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetGamesResponse(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetGamesResponse)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetGamesResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetGamesResponse(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetGamesResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetSimilarPositionsRequest(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetSimilarPositionsRequest)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetSimilarPositionsRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetSimilarPositionsRequest(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetSimilarPositionsRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetSimilarPositionsResponse(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetSimilarPositionsResponse)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetSimilarPositionsResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetSimilarPositionsResponse(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetSimilarPositionsResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


// CheSSE Backend Service
var CheSSEBackendServiceService = exports.CheSSEBackendServiceService = {
  // Fetch a collection of similar chess positions
getSimilarPositions: {
    path: '/chesse_backend_api.v1alpha1.CheSSEBackendService/GetSimilarPositions',
    requestStream: false,
    responseStream: false,
    requestType: chesse_backend_api_v1alpha1_chesse_pb.GetSimilarPositionsRequest,
    responseType: chesse_backend_api_v1alpha1_chesse_pb.GetSimilarPositionsResponse,
    requestSerialize: serialize_chesse_backend_api_v1alpha1_GetSimilarPositionsRequest,
    requestDeserialize: deserialize_chesse_backend_api_v1alpha1_GetSimilarPositionsRequest,
    responseSerialize: serialize_chesse_backend_api_v1alpha1_GetSimilarPositionsResponse,
    responseDeserialize: deserialize_chesse_backend_api_v1alpha1_GetSimilarPositionsResponse,
  },
  // Fetch a chess game
getGame: {
    path: '/chesse_backend_api.v1alpha1.CheSSEBackendService/GetGame',
    requestStream: false,
    responseStream: false,
    requestType: chesse_backend_api_v1alpha1_chesse_pb.GetGameRequest,
    responseType: chesse_backend_api_v1alpha1_chesse_pb.GetGameResponse,
    requestSerialize: serialize_chesse_backend_api_v1alpha1_GetGameRequest,
    requestDeserialize: deserialize_chesse_backend_api_v1alpha1_GetGameRequest,
    responseSerialize: serialize_chesse_backend_api_v1alpha1_GetGameResponse,
    responseDeserialize: deserialize_chesse_backend_api_v1alpha1_GetGameResponse,
  },
  // Fetch a list of chess games
getGames: {
    path: '/chesse_backend_api.v1alpha1.CheSSEBackendService/GetGames',
    requestStream: false,
    responseStream: false,
    requestType: chesse_backend_api_v1alpha1_chesse_pb.GetGamesRequest,
    responseType: chesse_backend_api_v1alpha1_chesse_pb.GetGamesResponse,
    requestSerialize: serialize_chesse_backend_api_v1alpha1_GetGamesRequest,
    requestDeserialize: deserialize_chesse_backend_api_v1alpha1_GetGamesRequest,
    responseSerialize: serialize_chesse_backend_api_v1alpha1_GetGamesResponse,
    responseDeserialize: deserialize_chesse_backend_api_v1alpha1_GetGamesResponse,
  },
};

exports.CheSSEBackendServiceClient = grpc.makeGenericClientConstructor(CheSSEBackendServiceService);
