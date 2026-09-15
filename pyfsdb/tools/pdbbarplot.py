"""Plot parts of an FSDB file."""

from __future__ import annotations
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, Namespace
from logging import debug, info, warning, error, critical
import logging
import sys
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame
import pyfsdb
import pyfsdb.graph_utils

# optionally use rich
try:
    from rich import print
    from rich.logging import RichHandler
    from rich.theme import Theme
    from rich.console import Console
except Exception:
    debug("install rich and rich.logging for prettier results")

# optionally use rich_argparse too
help_handler = ArgumentDefaultsHelpFormatter
try:
    from rich_argparse import RichHelpFormatter

    help_handler = RichHelpFormatter
except Exception:
    debug("install rich_argparse.logging for prettier help")


def parse_args() -> Namespace:
    """Parse the command line arguments."""
    parser = ArgumentParser(
        formatter_class=help_handler, description=__doc__, epilog="Example Usage: "
    )

    parser.add_argument(
        "--log-level",
        "--ll",
        default="info",
        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).",
    )

    sub_parser = pyfsdb.graph_utils.parse_args(parser)

    sub_parser.add_argument(
        "-H",
        "--hue-column",
        default=None,
        type=str,
        help="Variable to use for changing hue values, creating multiple bars",
    )

    parser.add_argument(
        "-z",
        "--horizontal",
        action="store_true",
        help="Plot the chart horizontally instead",
    )

    parser.add_argument(
        "input_file", type=FileType("r"), nargs="?", default=sys.stdin, help=""
    )

    parser.add_argument(
        "output_file",
        type=str,
        nargs="?",
        default="plot.png",
        help="Where to save the output PNG file.",
    )

    args = parser.parse_args()
    log_level = args.log_level.upper()
    handlers = []
    datefmt = None
    messagefmt = "%(levelname)-10s:\t%(message)s"

    # see if we're rich
    try:
        handlers.append(
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                console=Console(
                    stderr=True, theme=Theme({"logging.level.success": "green"})
                ),
            )
        )
        datefmt = " "
        messagefmt = "%(message)s"
    except Exception:
        debug("failed to install RichHandler")

    logging.basicConfig(
        level=log_level, format=messagefmt, datefmt=datefmt, handlers=handlers
    )
    return args


def main():
    args = parse_args()

    hue: str | None = None

    sns.set_theme()

    columns = [args.x_column, args.y_column]

    if args.hue_column:
        hue = args.hue_column
        columns.append(args.hue_column)

    df = pyfsdb.Fsdb(file_handle=args.input_file).get_pandas(usecols=columns)

    orientation = "v"
    if args.horizontal:
        orientation = "h"
    axes = sns.barplot(
        df,
        x=args.x_column,
        y=args.y_column,
        hue=hue,
        orient=orientation,
    )

    pyfsdb.graph_utils.set_graph_parameters(axes, args)
    pyfsdb.graph_utils.output_plot(plt, args.output_file, args, orient=orientation)


if __name__ == "__main__":
    main()
