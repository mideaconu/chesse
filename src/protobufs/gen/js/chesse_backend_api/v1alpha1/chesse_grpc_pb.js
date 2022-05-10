// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var chesse_backend_api_v1alpha1_chesse_pb = require('../../chesse_backend_api/v1alpha1/chesse_pb.js');
var chesse_backend_api_v1alpha1_games_pb = require('../../chesse_backend_api/v1alpha1/games_pb.js');
var chesse_backend_api_v1alpha1_positions_pb = require('../../chesse_backend_api/v1alpha1/positions_pb.js');

function serialize_chesse_backend_api_v1alpha1_GetChessGameRequest(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetChessGameRequest)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetChessGameRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetChessGameRequest(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetChessGameRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetChessGameResponse(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetChessGameResponse)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetChessGameResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetChessGameResponse(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetChessGameResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetChessGamesRequest(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetChessGamesRequest)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetChessGamesRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetChessGamesRequest(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetChessGamesRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetChessGamesResponse(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetChessGamesResponse)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetChessGamesResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetChessGamesResponse(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetChessGamesResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetChessPositionRequest(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionRequest)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetChessPositionRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetChessPositionRequest(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetChessPositionResponse(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionResponse)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetChessPositionResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetChessPositionResponse(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetChessPositionsRequest(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionsRequest)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetChessPositionsRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetChessPositionsRequest(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionsRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_backend_api_v1alpha1_GetChessPositionsResponse(arg) {
  if (!(arg instanceof chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionsResponse)) {
    throw new Error('Expected argument of type chesse_backend_api.v1alpha1.GetChessPositionsResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_backend_api_v1alpha1_GetChessPositionsResponse(buffer_arg) {
  return chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionsResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


// CheSSE Backend Service.
var CheSSEBackendServiceService = exports.CheSSEBackendServiceService = {
  // Fetch a chess position.
getChessPosition: {
    path: '/chesse_backend_api.v1alpha1.CheSSEBackendService/GetChessPosition',
    requestStream: false,
    responseStream: false,
    requestType: chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionRequest,
    responseType: chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionResponse,
    requestSerialize: serialize_chesse_backend_api_v1alpha1_GetChessPositionRequest,
    requestDeserialize: deserialize_chesse_backend_api_v1alpha1_GetChessPositionRequest,
    responseSerialize: serialize_chesse_backend_api_v1alpha1_GetChessPositionResponse,
    responseDeserialize: deserialize_chesse_backend_api_v1alpha1_GetChessPositionResponse,
  },
  // Fetch a list of chess positions.
getChessPositions: {
    path: '/chesse_backend_api.v1alpha1.CheSSEBackendService/GetChessPositions',
    requestStream: false,
    responseStream: false,
    requestType: chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionsRequest,
    responseType: chesse_backend_api_v1alpha1_chesse_pb.GetChessPositionsResponse,
    requestSerialize: serialize_chesse_backend_api_v1alpha1_GetChessPositionsRequest,
    requestDeserialize: deserialize_chesse_backend_api_v1alpha1_GetChessPositionsRequest,
    responseSerialize: serialize_chesse_backend_api_v1alpha1_GetChessPositionsResponse,
    responseDeserialize: deserialize_chesse_backend_api_v1alpha1_GetChessPositionsResponse,
  },
  // Fetch a chess game.
getChessGame: {
    path: '/chesse_backend_api.v1alpha1.CheSSEBackendService/GetChessGame',
    requestStream: false,
    responseStream: false,
    requestType: chesse_backend_api_v1alpha1_chesse_pb.GetChessGameRequest,
    responseType: chesse_backend_api_v1alpha1_chesse_pb.GetChessGameResponse,
    requestSerialize: serialize_chesse_backend_api_v1alpha1_GetChessGameRequest,
    requestDeserialize: deserialize_chesse_backend_api_v1alpha1_GetChessGameRequest,
    responseSerialize: serialize_chesse_backend_api_v1alpha1_GetChessGameResponse,
    responseDeserialize: deserialize_chesse_backend_api_v1alpha1_GetChessGameResponse,
  },
  // Fetch a list of chess games.
getChessGames: {
    path: '/chesse_backend_api.v1alpha1.CheSSEBackendService/GetChessGames',
    requestStream: false,
    responseStream: false,
    requestType: chesse_backend_api_v1alpha1_chesse_pb.GetChessGamesRequest,
    responseType: chesse_backend_api_v1alpha1_chesse_pb.GetChessGamesResponse,
    requestSerialize: serialize_chesse_backend_api_v1alpha1_GetChessGamesRequest,
    requestDeserialize: deserialize_chesse_backend_api_v1alpha1_GetChessGamesRequest,
    responseSerialize: serialize_chesse_backend_api_v1alpha1_GetChessGamesResponse,
    responseDeserialize: deserialize_chesse_backend_api_v1alpha1_GetChessGamesResponse,
  },
};

exports.CheSSEBackendServiceClient = grpc.makeGenericClientConstructor(CheSSEBackendServiceService);
