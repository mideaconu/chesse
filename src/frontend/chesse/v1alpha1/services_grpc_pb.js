// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var chesse_v1alpha1_backend_service_pb = require('../../chesse/v1alpha1/backend_service_pb.js');

function serialize_chesse_v1alpha1_GetChessGameRequest(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.GetChessGameRequest)) {
    throw new Error('Expected argument of type chesse.v1alpha1.GetChessGameRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_GetChessGameRequest(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.GetChessGameRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_v1alpha1_GetChessGameResponse(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.GetChessGameResponse)) {
    throw new Error('Expected argument of type chesse.v1alpha1.GetChessGameResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_GetChessGameResponse(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.GetChessGameResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_v1alpha1_GetChessPositionRequest(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.GetChessPositionRequest)) {
    throw new Error('Expected argument of type chesse.v1alpha1.GetChessPositionRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_GetChessPositionRequest(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.GetChessPositionRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_v1alpha1_GetChessPositionResponse(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.GetChessPositionResponse)) {
    throw new Error('Expected argument of type chesse.v1alpha1.GetChessPositionResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_GetChessPositionResponse(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.GetChessPositionResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_v1alpha1_ListChessGamesRequest(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.ListChessGamesRequest)) {
    throw new Error('Expected argument of type chesse.v1alpha1.ListChessGamesRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_ListChessGamesRequest(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.ListChessGamesRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_v1alpha1_ListChessGamesResponse(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.ListChessGamesResponse)) {
    throw new Error('Expected argument of type chesse.v1alpha1.ListChessGamesResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_ListChessGamesResponse(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.ListChessGamesResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_v1alpha1_ListChessPositionsRequest(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.ListChessPositionsRequest)) {
    throw new Error('Expected argument of type chesse.v1alpha1.ListChessPositionsRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_ListChessPositionsRequest(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.ListChessPositionsRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_v1alpha1_ListChessPositionsResponse(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.ListChessPositionsResponse)) {
    throw new Error('Expected argument of type chesse.v1alpha1.ListChessPositionsResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_ListChessPositionsResponse(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.ListChessPositionsResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


// CheSSE Backend Service.
var BackendServiceService = exports.BackendServiceService = {
  // Fetch a chess position.
getChessPosition: {
    path: '/chesse.v1alpha1.BackendService/GetChessPosition',
    requestStream: false,
    responseStream: false,
    requestType: chesse_v1alpha1_backend_service_pb.GetChessPositionRequest,
    responseType: chesse_v1alpha1_backend_service_pb.GetChessPositionResponse,
    requestSerialize: serialize_chesse_v1alpha1_GetChessPositionRequest,
    requestDeserialize: deserialize_chesse_v1alpha1_GetChessPositionRequest,
    responseSerialize: serialize_chesse_v1alpha1_GetChessPositionResponse,
    responseDeserialize: deserialize_chesse_v1alpha1_GetChessPositionResponse,
  },
  // Fetch a list of chess positions.
listChessPositions: {
    path: '/chesse.v1alpha1.BackendService/ListChessPositions',
    requestStream: false,
    responseStream: false,
    requestType: chesse_v1alpha1_backend_service_pb.ListChessPositionsRequest,
    responseType: chesse_v1alpha1_backend_service_pb.ListChessPositionsResponse,
    requestSerialize: serialize_chesse_v1alpha1_ListChessPositionsRequest,
    requestDeserialize: deserialize_chesse_v1alpha1_ListChessPositionsRequest,
    responseSerialize: serialize_chesse_v1alpha1_ListChessPositionsResponse,
    responseDeserialize: deserialize_chesse_v1alpha1_ListChessPositionsResponse,
  },
  // Fetch a chess game.
getChessGame: {
    path: '/chesse.v1alpha1.BackendService/GetChessGame',
    requestStream: false,
    responseStream: false,
    requestType: chesse_v1alpha1_backend_service_pb.GetChessGameRequest,
    responseType: chesse_v1alpha1_backend_service_pb.GetChessGameResponse,
    requestSerialize: serialize_chesse_v1alpha1_GetChessGameRequest,
    requestDeserialize: deserialize_chesse_v1alpha1_GetChessGameRequest,
    responseSerialize: serialize_chesse_v1alpha1_GetChessGameResponse,
    responseDeserialize: deserialize_chesse_v1alpha1_GetChessGameResponse,
  },
  // Fetch a list of chess games.
listChessGames: {
    path: '/chesse.v1alpha1.BackendService/ListChessGames',
    requestStream: false,
    responseStream: false,
    requestType: chesse_v1alpha1_backend_service_pb.ListChessGamesRequest,
    responseType: chesse_v1alpha1_backend_service_pb.ListChessGamesResponse,
    requestSerialize: serialize_chesse_v1alpha1_ListChessGamesRequest,
    requestDeserialize: deserialize_chesse_v1alpha1_ListChessGamesRequest,
    responseSerialize: serialize_chesse_v1alpha1_ListChessGamesResponse,
    responseDeserialize: deserialize_chesse_v1alpha1_ListChessGamesResponse,
  },
};

exports.BackendServiceClient = grpc.makeGenericClientConstructor(BackendServiceService);
