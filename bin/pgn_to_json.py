import collections
import json
from typing import Optional, TextIO

import chess.pgn
import click

from utils import compress, numeric


class GameJSONBuilder:
    identity_headers = ["Event", "Date", "Time", "Round", "White", "Black"]

    def __init__(self, game: chess.pgn.Game) -> None:
        self.game = game
        self.game_dict = collections.defaultdict(dict)

    def set_id(self) -> None:
        """Set ID generated from identity fields using data compression
        (gzip)."""
        id_fields = [self.game.headers[header] for header in self.identity_headers]
        id_ = compress.gzip_compress("|".join(id_fields))

        self.game_dict["id"] = id_

    def set_context(self) -> None:
        """Set fields that define the context of the game, i.e. event, date,
        round, and site.

        Fields are grouped under the 'context' group field.
        """
        context = {}
        for header in ["Event", "Date", "Site"]:
            if header in self.game.headers:
                context[header.lower()] = self.game.headers[header]

        context["round"] = (
            float(self.game.headers["Round"])
            if numeric.is_float(self.game.headers["Round"])
            else None
        )

        self.game_dict["context"] = context

    def set_white(self) -> None:
        """Set fields that define the side with the white pieces, i.e. name and
        elo.

        Fields are grouped under the 'white' group field.
        """
        white = {}
        white["name"] = self.game.headers["White"]
        white["elo"] = (
            int(self.game.headers["WhiteElo"])
            if numeric.is_int(self.game.headers["WhiteElo"])
            else None
        )

        self.game_dict["white"] = white

    def set_black(self) -> None:
        """Set fields that define the side with the black pieces, i.e. name and
        elo.

        Fields are grouped under the 'black' group field.
        """
        black = {}
        black["name"] = self.game.headers["Black"]
        black["elo"] = (
            int(self.game.headers["BlackElo"])
            if numeric.is_int(self.game.headers["BlackElo"])
            else None
        )

        self.game_dict["black"] = black

    def set_result(self) -> None:
        """Set the result of the game: 1 if white won, 0.5 for draw, 0 if black
        won, and None if the result is invalid."""
        if self.game.headers["Result"] == "1-0":
            self.game_dict["result"] = 1
        elif self.game.headers["Result"] == "1/2-1/2":
            self.game_dict["result"] = 0.5
        elif self.game.headers["Result"] == "0-1":
            self.game_dict["result"] = 0
        else:
            self.game_dict["result"] = None

    def set_moves(self) -> None:
        """Set the list of moves in the game.

        For each move the following representations are used: uci, san,
        and fen.
        """
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
        """Retrieve the result upon constructing the game object."""
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
    game_json_builder.set_result()
    game_json_builder.set_moves()
    game_json = game_json_builder.get_result()

    output_file.write(game_json)
    output_file.flush()
