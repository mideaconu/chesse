# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: duchess_backend_api/v1alpha1/duchess.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from duchess_backend_api.v1alpha1 import (
    games_pb2 as duchess__backend__api_dot_v1alpha1_dot_games__pb2,
)

DESCRIPTOR = _descriptor.FileDescriptor(
    name="duchess_backend_api/v1alpha1/duchess.proto",
    package="duchess_backend_api.v1alpha1",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b"\n*duchess_backend_api/v1alpha1/duchess.proto\x12\x1c\x64uchess_backend_api.v1alpha1\x1a(duchess_backend_api/v1alpha1/games.proto2\x97\x01\n\x15\x44uchessBackendService\x12~\n\x0fGetSimilarGames\x12\x34.duchess_backend_api.v1alpha1.GetSimilarGamesRequest\x1a\x35.duchess_backend_api.v1alpha1.GetSimilarGamesResponseb\x06proto3",
    dependencies=[
        duchess__backend__api_dot_v1alpha1_dot_games__pb2.DESCRIPTOR,
    ],
)


_sym_db.RegisterFileDescriptor(DESCRIPTOR)


_DUCHESSBACKENDSERVICE = _descriptor.ServiceDescriptor(
    name="DuchessBackendService",
    full_name="duchess_backend_api.v1alpha1.DuchessBackendService",
    file=DESCRIPTOR,
    index=0,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_start=119,
    serialized_end=270,
    methods=[
        _descriptor.MethodDescriptor(
            name="GetSimilarGames",
            full_name="duchess_backend_api.v1alpha1.DuchessBackendService.GetSimilarGames",
            index=0,
            containing_service=None,
            input_type=duchess__backend__api_dot_v1alpha1_dot_games__pb2._GETSIMILARGAMESREQUEST,
            output_type=duchess__backend__api_dot_v1alpha1_dot_games__pb2._GETSIMILARGAMESRESPONSE,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_DUCHESSBACKENDSERVICE)

DESCRIPTOR.services_by_name["DuchessBackendService"] = _DUCHESSBACKENDSERVICE

# @@protoc_insertion_point(module_scope)