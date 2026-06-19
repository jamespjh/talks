"""Command-line entry point for chessboard rendering."""

from __future__ import annotations

import argparse
import sys

from supporting_code.chessboard import render_chessboard_svg


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render a chessboard SVG from a FEN string."
    )
    parser.add_argument("position", help="FEN string describing the position")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    sys.stdout.write(render_chessboard_svg(args.position))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())