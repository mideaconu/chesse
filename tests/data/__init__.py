import json

from chesse_backend_api.v1alpha1 import games_pb2, positions_pb2

with open("tests/data/chess_position.json") as chess_position:
    chess_position_json = json.load(chess_position)

with open("tests/data/chess_positions.json") as chess_positions:
    chess_positions_json = json.load(chess_positions)

with open("tests/data/chess_game.json") as chess_game:
    chess_game_json = json.load(chess_game)

with open("tests/data/chess_games.json") as chess_games:
    chess_games_json = json.load(chess_games)

chess_position_pb2 = positions_pb2.Position(
    fen_encoding=chess_position_json["fen_encoding"],
    position_stats=positions_pb2.PositionStats(
        nr_games=chess_position_json["stats"]["nr_games"],
        rating_stats=positions_pb2.PositionRatingStats(
            min=chess_position_json["stats"]["rating"]["min"],
            avg=chess_position_json["stats"]["rating"]["avg"],
            max=chess_position_json["stats"]["rating"]["max"],
        ),
        result_stats=positions_pb2.PositionResultStats(
            white_win_pct=chess_position_json["stats"]["results"]["white"],
            draw_pct=chess_position_json["stats"]["results"]["draw"],
            black_win_pct=chess_position_json["stats"]["results"]["black"],
        ),
    ),
)

chess_positions_pb2 = [
    positions_pb2.Position(
        fen_encoding=position["fen_encoding"],
        position_stats=positions_pb2.PositionStats(
            nr_games=position["stats"]["nr_games"],
            rating_stats=positions_pb2.PositionRatingStats(
                min=position["stats"]["rating"]["min"],
                avg=position["stats"]["rating"]["avg"],
                max=position["stats"]["rating"]["max"],
            ),
            result_stats=positions_pb2.PositionResultStats(
                white_win_pct=position["stats"]["results"]["white"],
                draw_pct=position["stats"]["results"]["draw"],
                black_win_pct=position["stats"]["results"]["black"],
            ),
        ),
    )
    for position in chess_positions_json
]

chess_game_pb2 = games_pb2.Game(
    id=chess_game_json["id"],
    context=games_pb2.GameContext(
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

chess_games_pb2 = [
    games_pb2.Game(
        id=chess_game_json["id"],
        context=games_pb2.GameContext(
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
