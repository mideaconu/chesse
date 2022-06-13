from typing import Callable, Optional, TextIO

import click

import encoding


class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        help = kwargs.get("help", "")
        if self.mutually_exclusive:
            ex_str = ", ".join(self.mutually_exclusive)
            kwargs["help"] = help + (
                " NOTE: This argument is mutually exclusive with arguments: [" + ex_str + "]."
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(self.name, ", ".join(self.mutually_exclusive))
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(ctx, opts, args)


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
    except ValueError as e:
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
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["input_file"],
    type=str,
    default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -",
    show_default=True,
    help="FEN representation of the chess board to encode.",
)
@click.option(
    "--input-file",
    cls=MutuallyExclusiveOption,
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
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["input_file"],
    type=str,
    default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -",
    show_default=True,
    help="FEN representation of the chess board to encode.",
)
@click.option(
    "--input-file",
    cls=MutuallyExclusiveOption,
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
    cls=MutuallyExclusiveOption,
    type=str,
    default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -",
    mutually_exclusive=["input_file"],
    show_default=True,
    help="FEN representation of the chess board to encode.",
)
@click.option(
    "--input-file",
    cls=MutuallyExclusiveOption,
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
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["input_file"],
    type=str,
    default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -",
    show_default=True,
    help="FEN representation of the chess board to encode.",
)
@click.option(
    "--input-file",
    cls=MutuallyExclusiveOption,
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
