from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, Namespace
from matplotlib.axes import Axes
from seaborn.axisgrid import FacetGrid
import seaborn as sns


def parse_args(
    parser: ArgumentParser, sub_group_name: str = "Graph options"
) -> ArgumentParser:
    """Adds graphing specific arguments to the current parser.

    Puts contents in a sub-group unless sub_group_name is None."""

    if sub_group_name:
        parser = parser.add_argument_group(sub_group_name)

    parser.add_argument(
        "-x", "--x-column", default=["x"], type=str, help="X-axis column name to use"
    )

    parser.add_argument(
        "-y",
        "--y-column",
        default="value",
        type=str,
        help="Y-axis column name to use",
    )

    parser.add_argument(
        "--yr",
        "--y-label-rotation",
        "--",
        default=45,
        type=int,
        help="Amount to rotate the Y labels by.",
    )

    parser.add_argument(
        "-t", "--title", default=None, type=str, help="Title to place to the top"
    )

    parser.add_argument(
        "--xlabel", default=None, type=str, help="Text to use for the X axis label"
    )

    parser.add_argument(
        "--ylabel", default=None, type=str, help="Text to use for the Y axis label"
    )

    parser.add_argument(
        "--dpi", default=200, type=int, help="The DPI to use in the resulting image"
    )

    parser.add_argument(
        "--legend-location",
        default=None,
        type=str,
        help="Location of the legend (ul, lr, ...)",
    )

    return parser


def set_graph_parameters(control: Axes | FacetGrid, args: Namespace):
    """Set titles, labels, etc according to arguments passed."""

    keyword_maps = {
        "ul": {"args": ["upper left"], "kwargs": {"bbox_to_anchor": (0.1, 0.9)}},
        "ur": {"args": ["upper right"]},
        "ll": {"args": ["lower left"], "kwargs": {"bbox_to_anchor": (0.1, 0.3)}},
        "lr": {"args": ["lower right"], "kwargs": {"bbox_to_anchor": (0.95, 0.3)}},
        "cl": {"args": ["center left"], "kwargs": {"bbox_to_anchor": (0.1, 0.6)}},
        "cr": {"args": ["center right"], "kwargs": {"bbox_to_anchor": (0.95, 0.6)}},
        "c": {"args": ["center"]},
        "uc": {"args": ["upper center"], "kwargs": {"bbox_to_anchor": (0.5, 0.9)}},
        "lc": {"args": ["lower center"]},
    }

    if args.title:
        control.set(title=args.title)
    if args.xlabel:
        control.set(xlabel=args.xlabel)
    if args.ylabel:
        control.set(ylabel=args.ylabel)

    if args.legend_location:
        # maybe translate the brief name to a full one
        pass_args = args.legend_location
        pass_kwargs = {}
        if args.legend_location in keyword_maps:
            pass_args = keyword_maps[args.legend_location]["args"]
            pass_kwargs = keyword_maps[args.legend_location].get("kwargs", {})
        else:
            pass_args = [args]
        sns.move_legend(control, *pass_args, **pass_kwargs)


def output_plot(plt, output_file, args, orient: str = "v"):
    """Actually save the file and set some other plot defaults."""

    if orient == "h":
        plt.gcf().axes[0].xaxis.get_major_formatter().set_scientific(False)
    else:
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)

    plt.xticks(rotation=args.yr)
    plt.tight_layout()
    plt.savefig(output_file, dpi=args.dpi)
