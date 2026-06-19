from supporting_code import __version__
from supporting_code.chessboard import render_chessboard_svg
from supporting_code.cli import main


def test_package_imports():
    assert __version__ == "0.1.0"


def test_render_chessboard_svg_generates_svg_markup():
    fen = "8/8/8/8/8/8/8/8 w - - 0 1"
    svg = render_chessboard_svg(fen)

    assert "<svg" in svg
    assert "</svg>" in svg


def test_main_renders_svg_from_position(capsys):
    fen = "8/8/8/8/8/8/8/8 w - - 0 1"
    exit_code = main([fen])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "<svg" in output
    assert "</svg>" in output