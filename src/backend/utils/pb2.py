from typing import List, Union

from chesse_backend_api.v1alpha1 import games_pb2, positions_pb2

from utils.exception import IllegalArgumentError
from utils.typing import JSON


def _convert_chess_position_json_to_pb2(chess_position_json: JSON) -> positions_pb2.Position:
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

    return chess_position_pb2


def _convert_chess_positions_json_to_pb2(
    chess_positions_json: JSON,
) -> List[positions_pb2.Position]:
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

    return chess_positions_pb2


def _convert_chess_game_json_to_pb2(chess_game_json: JSON) -> games_pb2.Game:
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

    return chess_game_pb2


def _convert_chess_games_json_to_pb2(chess_games_json: JSON) -> List[games_pb2.Game]:
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

    return chess_games_pb2


def convert_json_to_pb2(
    **kwargs: JSON,
) -> Union[
    positions_pb2.Position, List[positions_pb2.Position], games_pb2.Game, List[games_pb2.Game]
]:
    """Converts JSON objects to pb2. One of the following sets of arguments can
    be passed to the function:

    - (chess_position_json): Returns a chess position pb2 conversion.
    - (chess_positions_json): Returns a list of chess position pb2
    conversions.
    - (chess_game_json): Returns a chess game pb2 conversion.
    - (chess_games_json): Returns a list of chess games pb2 conversions.

    Raises:
        IllegalArgumentError: If the argument passed is not supported.

    Returns:
        Union[positions_pb2.Position, List[positions_pb2.Position],
        games_pb2.Game, List[games_pb2.Game]]: The pb2 conversion of the input
        JSON object.
    """
    match list(kwargs.keys()):
        case ["chess_position_json"]:
            return _convert_chess_position_json_to_pb2(
                chess_position_json=kwargs["chess_position_json"]
            )
        case ["chess_positions_json"]:
            return _convert_chess_positions_json_to_pb2(
                chess_positions_json=kwargs["chess_positions_json"]
            )
        case ["chess_game_json"]:
            return _convert_chess_game_json_to_pb2(chess_game_json=kwargs["chess_game_json"])
        case ["chess_games_json"]:
            return _convert_chess_games_json_to_pb2(chess_games_json=kwargs["chess_games_json"])
        case _:
            raise IllegalArgumentError(
                f"Invalid arguments to function convert_json_to_pb2: {kwargs}."
            )
