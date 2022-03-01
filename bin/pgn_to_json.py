import base64
import json
import zlib
from typing import Optional, TextIO

import chess.pgn
import click

HEADERS = ["Event", "Site", "Date", "Round", "White", "Black", "Result", "WhiteElo", "BlackElo"]


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
    game_json = {}

    for header in HEADERS:
        if header in game.headers:
            game_json[header.lower()] = game.headers[header]

    node = game
    moves = []
    while node.variations:
        next_node = node.variation(0)
        moves.append(node.board().san(next_node.move))
        node = next_node

    game_json["moves"] = moves

    id_ = "|".join([game_json[header] for header in ["event", "date", "round", "white", "black"]])
    id_zlib = zlib.compress(bytes(id_, encoding="utf-8"))
    id_base64 = base64.b64encode(id_zlib).decode(encoding="utf-8")
    game_json["id"] = id_base64

    output_file.write(json.dumps(game_json))
    output_file.flush()
