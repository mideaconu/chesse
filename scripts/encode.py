from typing import Callable, Optional, TextIO

import click

from utils import click as click_utils
from utils import encoding
from utils import exception as exc


def run_encoding(
    encoding_fct: Callable,
    fen: str,
    input_file: Optional[TextIO],
    output_file: Optional[click.utils.LazyFile],
    **kwargs,
) -> None:
    """Runs the encoding function on the FEN representation of the chess
    position.

    Optionally reads the FEN representation from `input_file` and/or
    writes the encoding to `output_file`.
    """
    if input_file:
        fen = input_file.readline().strip()

    try:
        encoding = encoding_fct(fen, **kwargs)
    except exc.InvalidFENError as e:
        raise click.BadParameter(f"Encoding error: {e}")

    if output_file:
        output_file.write(encoding + "\n")
        output_file.flush()
    else:
        click.echo(encoding)


@click.group()
@click.version_option("0.1.0")
@click.help_option()
def cli() -> None:
    pass


@cli.command("similarity")
@click.option(
    "--fen",
    cls=click_utils.MutuallyExclusiveOption,
    mutually_exclusive=["input_file"],
    type=str,
    default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -",
    show_default=True,
    help="FEN representation of the chess board to encode.",
)
@click.option(
    "--input-file",
    cls=click_utils.MutuallyExclusiveOption,
    mutually_exclusive=["fen"],
    type=click.File("r"),
    help="File that contains the FEN representation of the chess board to encode. "
    "'-' can be used to read from stdin.",
)
@click.option(
    "--output-file",
    type=click.File("w"),
    help="File that the encoding is written to. '-' can be used to redirect to stdout.",
)
def similarity(
    fen: str,
    input_file: Optional[TextIO],
    output_file: Optional[click.utils.LazyFile],
) -> None:
    """Returns the similarity encoding of a given chess position."""
    run_encoding(encoding.get_similarity_encoding, fen, input_file, output_file)


@cli.command("naive")
@click.option(
    "--fen",
    cls=click_utils.MutuallyExclusiveOption,
    mutually_exclusive=["input_file"],
    type=str,
    default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -",
    show_default=True,
    help="FEN representation of the chess board to encode.",
)
@click.option(
    "--input-file",
    cls=click_utils.MutuallyExclusiveOption,
    mutually_exclusive=["fen"],
    type=click.File("r"),
    help="File that contains the FEN representation of the chess board to encode. "
    "'-' can be used to read from stdin.",
)
@click.option(
    "--output-file",
    type=click.File("w"),
    help="File that the encoding is written to. '-' can be used to redirect to stdout.",
)
def naive(
    fen: str, input_file: Optional[TextIO], output_file: Optional[click.utils.LazyFile]
) -> None:
    """Returns the naive encoding of a given chess position."""
    run_encoding(encoding.get_naive_encoding, fen, input_file, output_file)


@cli.command("activity")
@click.option(
    "--fen",
    cls=click_utils.MutuallyExclusiveOption,
    type=str,
    default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -",
    mutually_exclusive=["input_file"],
    show_default=True,
    help="FEN representation of the chess board to encode.",
)
@click.option(
    "--input-file",
    cls=click_utils.MutuallyExclusiveOption,
    mutually_exclusive=["fen"],
    type=click.File("r"),
    help="File that contains the FEN representation of the chess board to encode. "
    "'-' can be used to read from stdin.",
)
@click.option(
    "--output-file",
    type=click.File("w"),
    help="File that the encoding is written to. '-' can be used to redirect to stdout.",
)
def activity(
    fen: str, input_file: Optional[TextIO], output_file: Optional[click.utils.LazyFile]
) -> None:
    """Returns the activity encoding of a given chess position."""
    run_encoding(encoding.get_activity_encoding, fen, input_file, output_file)


@cli.command("connectivity")
@click.option(
    "--fen",
    cls=click_utils.MutuallyExclusiveOption,
    mutually_exclusive=["input_file"],
    type=str,
    default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -",
    show_default=True,
    help="FEN representation of the chess board to encode.",
)
@click.option(
    "--input-file",
    cls=click_utils.MutuallyExclusiveOption,
    mutually_exclusive=["fen"],
    type=click.File("r"),
    help="File that contains the FEN representation of the chess board to encode. "
    "'-' can be used to read from stdin.",
)
@click.option(
    "--output-file",
    type=click.File("w"),
    help="File that the encoding is written to. '-' can be used to redirect to stdout.",
)
def connectivity(
    fen: str, input_file: Optional[TextIO], output_file: Optional[click.utils.LazyFile]
) -> None:
    """Returns the connectivity encoding of a given chess position."""
    run_encoding(encoding.get_connectivity_encoding, fen, input_file, output_file)
