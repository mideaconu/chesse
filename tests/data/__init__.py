import json

from chesse.v1alpha1 import games_pb2, positions_pb2

tmp_dir = "tmp"

backend_test_data_dir = "tests/data/backend"
encoding_test_data_dir = "tests/data/encoding"
es_test_data_dir = f"{backend_test_data_dir}/elasticsearch/responses"

with open(f"{es_test_data_dir}/chess_position_response.json") as chess_position_response:
    chess_position_response_json = json.load(chess_position_response)

with open(f"{es_test_data_dir}/similar_positions_response.json") as similar_positions_response:
    similar_positions_response_json = json.load(similar_positions_response)

with open(f"{es_test_data_dir}/positions_stats_response.json") as positions_stats_response:
    positions_stats_response_json = json.load(positions_stats_response)

with open(f"{es_test_data_dir}/chess_game_response.json") as chess_game_response:
    chess_game_response_json = json.load(chess_game_response)

with open(f"{es_test_data_dir}/chess_games_response.json") as chess_games_response:
    chess_games_response_json = json.load(chess_games_response)

with open(f"{backend_test_data_dir}/chess_position.json") as chess_position:
    chess_position_json = json.load(chess_position)

with open(f"{backend_test_data_dir}/chess_positions.json") as chess_positions:
    chess_positions_json = json.load(chess_positions)

with open(f"{backend_test_data_dir}/chess_game.json") as chess_game:
    chess_game_json = json.load(chess_game)

with open(f"{backend_test_data_dir}/chess_games.json") as chess_games:
    chess_games_json = json.load(chess_games)

chess_position_pb = positions_pb2.ChessPosition(
    fen_encoding=chess_position_json["fen_encoding"],
    position_stats=positions_pb2.ChessPositionStats(
        nr_games=chess_position_json["stats"]["nr_games"],
        rating_stats=positions_pb2.ChessPositionRatingStats(
            min=chess_position_json["stats"]["rating"]["min"],
            avg=chess_position_json["stats"]["rating"]["avg"],
            max=chess_position_json["stats"]["rating"]["max"],
        ),
        result_stats=positions_pb2.ChessPositionResultStats(
            white_win_pct=chess_position_json["stats"]["results"]["white"],
            draw_pct=chess_position_json["stats"]["results"]["draw"],
            black_win_pct=chess_position_json["stats"]["results"]["black"],
        ),
    ),
)

chess_positions_pb = [
    positions_pb2.ChessPosition(
        fen_encoding=position["fen_encoding"],
        position_stats=positions_pb2.ChessPositionStats(
            nr_games=position["stats"]["nr_games"],
            rating_stats=positions_pb2.ChessPositionRatingStats(
                min=position["stats"]["rating"]["min"],
                avg=position["stats"]["rating"]["avg"],
                max=position["stats"]["rating"]["max"],
            ),
            result_stats=positions_pb2.ChessPositionResultStats(
                white_win_pct=position["stats"]["results"]["white"],
                draw_pct=position["stats"]["results"]["draw"],
                black_win_pct=position["stats"]["results"]["black"],
            ),
        ),
    )
    for position in chess_positions_json
]

chess_game_pb = games_pb2.ChessGame(
    id=chess_game_json["id"],
    context=games_pb2.ChessGameContext(
        event=chess_game_json["context"]["event"],
        date=chess_game_json["context"]["date"],
        site=chess_game_json["context"]["site"],
        round=chess_game_json["context"]["round"],
    ),
    white=games_pb2.White(
        name=chess_game_json["white"]["name"], elo=chess_game_json["white"]["elo"]
    ),
    black=games_pb2.Black(
        name=chess_game_json["black"]["name"], elo=chess_game_json["black"]["elo"]
    ),
    result=chess_game_json["result"],
    moves=[
        games_pb2.Move(
            uci=move["uci"],
            san=move["san"],
            fen=move["fen"],
        )
        for move in chess_game_json["moves"]
    ],
)

chess_games_pb = [
    games_pb2.ChessGame(
        id=chess_game_json["id"],
        context=games_pb2.ChessGameContext(
            event=chess_game_json["context"]["event"],
            date=chess_game_json["context"]["date"],
            site=chess_game_json["context"]["site"],
            round=chess_game_json["context"]["round"],
        ),
        white=games_pb2.White(
            name=chess_game_json["white"]["name"], elo=chess_game_json["white"]["elo"]
        ),
        black=games_pb2.Black(
            name=chess_game_json["black"]["name"], elo=chess_game_json["black"]["elo"]
        ),
        result=chess_game_json["result"],
        moves=[
            games_pb2.Move(
                uci=move["uci"],
                san=move["san"],
                fen=move["fen"],
            )
            for move in chess_game_json["moves"]
        ],
    )
    for chess_game_json in chess_games_json
]
