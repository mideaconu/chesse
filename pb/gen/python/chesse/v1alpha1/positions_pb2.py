# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chesse/v1alpha1/positions.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1f\x63hesse/v1alpha1/positions.proto\x12\x0f\x63hesse.v1alpha1"P\n\x18\x43hessPositionRatingStats\x12\x10\n\x03min\x18\x01 \x01(\x05R\x03min\x12\x10\n\x03\x61vg\x18\x02 \x01(\x05R\x03\x61vg\x12\x10\n\x03max\x18\x03 \x01(\x05R\x03max"}\n\x18\x43hessPositionResultStats\x12"\n\rwhite_win_pct\x18\x01 \x01(\x02R\x0bwhiteWinPct\x12\x19\n\x08\x64raw_pct\x18\x02 \x01(\x02R\x07\x64rawPct\x12"\n\rblack_win_pct\x18\x03 \x01(\x02R\x0b\x62lackWinPct"\xcb\x01\n\x12\x43hessPositionStats\x12\x19\n\x08nr_games\x18\x01 \x01(\x05R\x07nrGames\x12L\n\x0crating_stats\x18\x02 \x01(\x0b\x32).chesse.v1alpha1.ChessPositionRatingStatsR\x0bratingStats\x12L\n\x0cresult_stats\x18\x03 \x01(\x0b\x32).chesse.v1alpha1.ChessPositionResultStatsR\x0bresultStats"~\n\rChessPosition\x12!\n\x0c\x66\x65n_encoding\x18\x01 \x01(\tR\x0b\x66\x65nEncoding\x12J\n\x0eposition_stats\x18\x02 \x01(\x0b\x32#.chesse.v1alpha1.ChessPositionStatsR\rpositionStatsb\x06proto3'
)


_CHESSPOSITIONRATINGSTATS = DESCRIPTOR.message_types_by_name["ChessPositionRatingStats"]
_CHESSPOSITIONRESULTSTATS = DESCRIPTOR.message_types_by_name["ChessPositionResultStats"]
_CHESSPOSITIONSTATS = DESCRIPTOR.message_types_by_name["ChessPositionStats"]
_CHESSPOSITION = DESCRIPTOR.message_types_by_name["ChessPosition"]
ChessPositionRatingStats = _reflection.GeneratedProtocolMessageType(
    "ChessPositionRatingStats",
    (_message.Message,),
    {
        "DESCRIPTOR": _CHESSPOSITIONRATINGSTATS,
        "__module__": "chesse.v1alpha1.positions_pb2"
        # @@protoc_insertion_point(class_scope:chesse.v1alpha1.ChessPositionRatingStats)
    },
)
_sym_db.RegisterMessage(ChessPositionRatingStats)

ChessPositionResultStats = _reflection.GeneratedProtocolMessageType(
    "ChessPositionResultStats",
    (_message.Message,),
    {
        "DESCRIPTOR": _CHESSPOSITIONRESULTSTATS,
        "__module__": "chesse.v1alpha1.positions_pb2"
        # @@protoc_insertion_point(class_scope:chesse.v1alpha1.ChessPositionResultStats)
    },
)
_sym_db.RegisterMessage(ChessPositionResultStats)

ChessPositionStats = _reflection.GeneratedProtocolMessageType(
    "ChessPositionStats",
    (_message.Message,),
    {
        "DESCRIPTOR": _CHESSPOSITIONSTATS,
        "__module__": "chesse.v1alpha1.positions_pb2"
        # @@protoc_insertion_point(class_scope:chesse.v1alpha1.ChessPositionStats)
    },
)
_sym_db.RegisterMessage(ChessPositionStats)

ChessPosition = _reflection.GeneratedProtocolMessageType(
    "ChessPosition",
    (_message.Message,),
    {
        "DESCRIPTOR": _CHESSPOSITION,
        "__module__": "chesse.v1alpha1.positions_pb2"
        # @@protoc_insertion_point(class_scope:chesse.v1alpha1.ChessPosition)
    },
)
_sym_db.RegisterMessage(ChessPosition)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _CHESSPOSITIONRATINGSTATS._serialized_start = 52
    _CHESSPOSITIONRATINGSTATS._serialized_end = 132
    _CHESSPOSITIONRESULTSTATS._serialized_start = 134
    _CHESSPOSITIONRESULTSTATS._serialized_end = 259
    _CHESSPOSITIONSTATS._serialized_start = 262
    _CHESSPOSITIONSTATS._serialized_end = 465
    _CHESSPOSITION._serialized_start = 467
    _CHESSPOSITION._serialized_end = 593
# @@protoc_insertion_point(module_scope)
