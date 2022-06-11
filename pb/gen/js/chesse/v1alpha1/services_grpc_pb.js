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

function serialize_chesse_v1alpha1_GetChessGamesRequest(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.GetChessGamesRequest)) {
    throw new Error('Expected argument of type chesse.v1alpha1.GetChessGamesRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_GetChessGamesRequest(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.GetChessGamesRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_v1alpha1_GetChessGamesResponse(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.GetChessGamesResponse)) {
    throw new Error('Expected argument of type chesse.v1alpha1.GetChessGamesResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_GetChessGamesResponse(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.GetChessGamesResponse.deserializeBinary(new Uint8Array(buffer_arg));
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

function serialize_chesse_v1alpha1_GetChessPositionsRequest(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.GetChessPositionsRequest)) {
    throw new Error('Expected argument of type chesse.v1alpha1.GetChessPositionsRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_GetChessPositionsRequest(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.GetChessPositionsRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_chesse_v1alpha1_GetChessPositionsResponse(arg) {
  if (!(arg instanceof chesse_v1alpha1_backend_service_pb.GetChessPositionsResponse)) {
    throw new Error('Expected argument of type chesse.v1alpha1.GetChessPositionsResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_chesse_v1alpha1_GetChessPositionsResponse(buffer_arg) {
  return chesse_v1alpha1_backend_service_pb.GetChessPositionsResponse.deserializeBinary(new Uint8Array(buffer_arg));
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
getChessPositions: {
    path: '/chesse.v1alpha1.BackendService/GetChessPositions',
    requestStream: false,
    responseStream: false,
    requestType: chesse_v1alpha1_backend_service_pb.GetChessPositionsRequest,
    responseType: chesse_v1alpha1_backend_service_pb.GetChessPositionsResponse,
    requestSerialize: serialize_chesse_v1alpha1_GetChessPositionsRequest,
    requestDeserialize: deserialize_chesse_v1alpha1_GetChessPositionsRequest,
    responseSerialize: serialize_chesse_v1alpha1_GetChessPositionsResponse,
    responseDeserialize: deserialize_chesse_v1alpha1_GetChessPositionsResponse,
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
getChessGames: {
    path: '/chesse.v1alpha1.BackendService/GetChessGames',
    requestStream: false,
    responseStream: false,
    requestType: chesse_v1alpha1_backend_service_pb.GetChessGamesRequest,
    responseType: chesse_v1alpha1_backend_service_pb.GetChessGamesResponse,
    requestSerialize: serialize_chesse_v1alpha1_GetChessGamesRequest,
    requestDeserialize: deserialize_chesse_v1alpha1_GetChessGamesRequest,
    responseSerialize: serialize_chesse_v1alpha1_GetChessGamesResponse,
    responseDeserialize: deserialize_chesse_v1alpha1_GetChessGamesResponse,
  },
};

exports.BackendServiceClient = grpc.makeGenericClientConstructor(BackendServiceService);
