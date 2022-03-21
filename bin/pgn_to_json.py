import base64
import collections
import json
import zlib
from typing import Any, Dict, Iterable, List, Optional, TextIO

import chess.pgn
import click


# TODO move to utils
def gzip_compress(list: Iterable[str], delimiter: Optional[str] = None) -> str:
    """Compress a list of string values using gzip.

    Args:
        list (Iterable): List of values to compress.
        delimiter (Optional[str], optional): Delimiter for the values in the
            list, before compression. If None, the pipe symbol is used ("|").
            Defaults to None.

    Returns:
        str: Compressed list of values.
    """
    if not delimiter:
        delimiter = "|"

    list_str = delimiter.join(list)
    gzip_list_bytes = zlib.compress(bytes(list_str, encoding="utf-8"))
    gzip_list_str = base64.b64encode(gzip_list_bytes).decode(encoding="utf-8")

    return gzip_list_str


class GameJSONBuilder:
    context_headers = ["Event", "Date", "Round", "Site"]
    identity_headers = ["Event", "Date", "Round", "White", "Black"]

    def __init__(self, game: chess.pgn.Game) -> None:
        self.game = game
        self.game_dict = collections.defaultdict(dict)

    def set_id(self) -> None:
        """Set ID generated from identity fields using data compression
        (gzip)."""
        id_fields = [self.game.headers[header] for header in self.identity_headers]
        id_ = gzip_compress(id_fields)

        self.game_dict["id"] = id_

    def set_context(self) -> None:
        """_summary_"""
        context = {}
        for header in self.context_headers:
            if header in self.game.headers:
                context[header.lower()] = self.game.headers[header]

        self.game_dict["context"] = context

    def set_white(self) -> None:
        """_summary_"""
        white = {}
        white["name"] = self.game.headers["White"]
        white["elo"] = self.game.headers["WhiteElo"]

        self.game_dict["white"] = white

    def set_black(self) -> None:
        """_summary_"""
        black = {}
        black["name"] = self.game.headers["Black"]
        black["elo"] = self.game.headers["BlackElo"]

        self.game_dict["black"] = black

    def set_moves(self) -> None:
        """_summary_"""
        node = self.game
        moves = []
        while node.variations:
            next_node = node.variation(0)
            next_node_move = next_node.move
            moves.append(
                {
                    "uci": next_node_move.uci(),
                    "san": node.board().san(next_node_move),
                    "fen": node.board().fen(),
                }
            )
            node = next_node

        self.game_dict["moves"] = moves

    def get_result(self) -> str:
        """_summary_"""
        return json.dumps(self.game_dict)


@click.version_option("0.1.0")
@click.help_option()
@click.command()
@click.option(
    "--input-file",
    type=click.File("r"),
    help="File that contains the PGN representation of the chess game. "
    "'-' can be used to read from stdin.",
)
@click.option(
    "--output-file",
    type=click.File("w"),
    help="File that the JSON representation is written to. '-' can be used to redirect to stdout.",
)
def cli(
    input_file: Optional[TextIO],
    output_file: Optional[click.utils.LazyFile],
) -> None:
    """Converts a PGN file to JSON."""
    game = chess.pgn.read_game(input_file)
    game_json_builder = GameJSONBuilder(game)

    # TODO separate OTB from online
    game_json_builder.set_id()
    game_json_builder.set_context()
    game_json_builder.set_white()
    game_json_builder.set_black()
    game_json_builder.set_moves()
    game_json = game_json_builder.get_result()

    output_file.write(game_json)
    output_file.flush()
