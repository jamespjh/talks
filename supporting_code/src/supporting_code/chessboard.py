"""Render chess positions as SVG."""


def render_chessboard_svg(position_description: str) -> str:
    """Render a chess position description to an SVG string.

    The position description is expected to be a FEN string.
    """

    import chess
    import chess.svg

    board = chess.Board(position_description)
    return str(chess.svg.board(board=board))