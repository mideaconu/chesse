from elasticsearch_dsl.response import Response
from loguru import logger

from utils import exception as exc_utils
from utils.exception import ElasticSearchQueryError, IllegalArgumentError
from utils.typing import JSON


def filter_chess_position_response(chess_position_response: Response) -> JSON:
    """Converts the raw ES response to JSON and filters it so that only
    relevant information in the chess position response is kept.

    Raises:
        ElasticSearchQueryError: If there is an error processing the raw
        response.
    """
    chess_position_raw = chess_position_response.hits[0]

    try:
        chess_position = {
            "fen_encoding": chess_position_raw.position.fen,
            "similarity_encoding": chess_position_raw.position.encoding,
        }
    except AttributeError as e:
        exc_utils.log_and_raise(
            logger,
            ElasticSearchQueryError,
            f"Error processing ElasticSearch response: {e}. "
            f"Raw get chess position response: {chess_position_response}.",
        )

    return chess_position


def filter_chess_position_stats_response(chess_positions_stats_response: Response) -> JSON:
    """Converts the raw ES response to JSON and filters it so that only
    relevant information in the position stats response is kept.

    Raises:
        ElasticSearchQueryError: If there is an error processing the raw
        response.
    """
    try:
        bucket = chess_positions_stats_response.aggregations.category_fen.fen.buckets[0]

        chess_position_stats = {
            "nr_games": bucket.doc_count,
            "rating": {
                "min": int(min(bucket.white.min_elo.value, bucket.black.min_elo.value)),
                "avg": int((bucket.white.avg_elo.value + bucket.black.avg_elo.value) / 2),
                "max": int(max(bucket.white.max_elo.value, bucket.black.max_elo.value)),
            },
            "results": {"white": 0, "draw": 0, "black": 0},
        }

        for side in bucket.results.side_won.buckets:
            win_rate_pct = side.doc_count / chess_position_stats["nr_games"] * 100
            match side.key:
                case 1:
                    chess_position_stats["results"]["white"] = win_rate_pct
                case 0.5:
                    chess_position_stats["results"]["draw"] = win_rate_pct
                case 0:
                    chess_position_stats["results"]["black"] = win_rate_pct
                case _:
                    exc_utils.log_and_raise(
                        logger,
                        IllegalArgumentError,
                        f"Error processing positions stats: illegal winning side: {side['key']}",
                    )
    except AttributeError as e:
        exc_utils.log_and_raise(
            logger,
            ElasticSearchQueryError,
            f"Error processing ElasticSearch response: {e}. "
            f"Raw get chess position stats response: {chess_position_stats}.",
        )

    return chess_position_stats


def filter_chess_positions_response(chess_positions_response: Response) -> JSON:
    """Converts the raw ES response to JSON and filters it so that only
    relevant information in the chess positions response is kept.

    Raises:
        ElasticSearchQueryError: If there is an error processing the raw
        response.
    """
    chess_positions_raw = chess_positions_response.hits

    try:
        chess_positions = [
            {
                "fen_encoding": chess_position.position.fen,
                "similarity_encoding": chess_position.position.encoding,
                "similarity_score": chess_position.meta.score,
            }
            for chess_position in chess_positions_raw
        ]
    except AttributeError as e:
        exc_utils.log_and_raise(
            logger,
            ElasticSearchQueryError,
            f"Error processing ElasticSearch response: {e}. "
            f"Raw get chess position response: {chess_positions_response}.",
        )

    return chess_positions


def filter_chess_positions_stats_response(chess_positions_stats_response: Response) -> JSON:
    """Converts the raw ES response to JSON and filters it so that only
    relevant information in the positions stats response is kept.

    Raises:
        ElasticSearchQueryError: If there is an error processing the raw
        response.
    """
    chess_positions_stats = {}

    try:
        for bucket in chess_positions_stats_response.aggregations.category_fen.fen.buckets:
            fen = bucket.key.partition(" ")[0]

            chess_positions_stats[fen] = {
                "nr_games": bucket.doc_count,
                "rating": {
                    "min": int(min(bucket.white.min_elo.value, bucket.black.min_elo.value)),
                    "avg": int((bucket.white.avg_elo.value + bucket.black.avg_elo.value) / 2),
                    "max": int(max(bucket.white.max_elo.value, bucket.black.max_elo.value)),
                },
                "results": {"white": 0, "draw": 0, "black": 0},
            }

            for side in bucket.results.side_won.buckets:
                match side.key:
                    case 1:
                        chess_positions_stats[fen]["results"]["white"] = (
                            side.doc_count / chess_positions_stats[fen]["nr_games"] * 100
                        )
                    case 0.5:
                        chess_positions_stats[fen]["results"]["draw"] = (
                            side.doc_count / chess_positions_stats[fen]["nr_games"] * 100
                        )
                    case 0:
                        chess_positions_stats[fen]["results"]["black"] = (
                            side.doc_count / chess_positions_stats[fen]["nr_games"] * 100
                        )
                    case _:
                        exc_utils.log_and_raise(
                            logger,
                            IllegalArgumentError,
                            f"Error processing positions stats: illegal winning side: {side['key']}",
                        )
    except Exception as e:
        exc_utils.log_and_raise(
            logger,
            ElasticSearchQueryError,
            f"Error processing ElasticSearch response: {e}. "
            f"Raw get chess position response: {chess_positions_stats_response}.",
        )

    return chess_positions_stats


def filter_chess_game_response(chess_game_response: Response) -> JSON:
    """Converts the raw ES response to JSON and filters it so that only
    relevant information in the game response is kept.

    Raises:
        ElasticSearchQueryError: If there is an error processing the raw
        response.
    """
    chess_game_raw = chess_game_response.hits[0]

    try:
        chess_game = {
            "id": chess_game_raw.id,
            "context": {
                "event": chess_game_raw.context.event,
                "date": chess_game_raw.context.date,
                "site": chess_game_raw.context.site,
                "round": chess_game_raw.context.round,
            },
            "white": {
                "name": chess_game_raw.white.name,
                "elo": chess_game_raw.white.elo,
            },
            "black": {
                "name": chess_game_raw.black.name,
                "elo": chess_game_raw.black.elo,
            },
            "moves": [
                {
                    "uci": move.uci,
                    "san": move.san,
                    "fen": move.fen,
                }
                for move in chess_game_raw.moves
            ],
            "result": chess_game_raw.result,
        }
    except AttributeError as e:
        exc_utils.log_and_raise(
            logger,
            ElasticSearchQueryError,
            f"Error processing ElasticSearch response: {e}. "
            f"Raw get chess game response: {chess_game_response}.",
        )

    return chess_game


def filter_chess_games_response(chess_games_response: Response) -> JSON:
    """Converts the raw ES response to JSON and filters it so that only
    relevant information in the games response is kept.

    Raises:
        ElasticSearchQueryError: If there is an error processing the raw
        response.
    """
    chess_games_raw = chess_games_response.hits

    try:
        chess_games = [
            {
                "id": chess_game_raw.id,
                "context": {
                    "event": chess_game_raw.context.event,
                    "date": chess_game_raw.context.date,
                    "site": chess_game_raw.context.site,
                    "round": chess_game_raw.context.round,
                },
                "white": {
                    "name": chess_game_raw.white.name,
                    "elo": chess_game_raw.white.elo,
                },
                "black": {
                    "name": chess_game_raw.black.name,
                    "elo": chess_game_raw.black.elo,
                },
                "moves": [
                    {
                        "uci": move.uci,
                        "san": move.san,
                        "fen": move.fen,
                    }
                    for move in chess_game_raw.moves
                ],
                "result": chess_game_raw.result,
            }
            for chess_game_raw in chess_games_raw
        ]
    except AttributeError as e:
        exc_utils.log_and_raise(
            logger,
            ElasticSearchQueryError,
            f"Error processing ElasticSearch response: {e}. "
            f"Raw get chess game response: {chess_games_response}.",
        )

    return chess_games
