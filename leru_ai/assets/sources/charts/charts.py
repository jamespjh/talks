#!/usr/bin/env python3
"""Draw the talk's bar chart as SVG, using only the standard library.

  charts.py OUTDIR

reads fully_open.csv next to this script and writes fully_open.svg to OUTDIR.
Update the CSV (and FRONTIER below) to refresh the numbers; the sources are given
in the chart's footer.
"""
import csv
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
BG, WHITE, MUTED, PURPLE = "#3c1657", "#f5f5f5", "#9c88ad", "#a433ff"
FONT = "Helvetica, Arial, sans-serif"
FRONTIER, FRONTIER_RANGE = 93.2, "MMLU-Pro 90–93"  # Kaggle MMLU-Pro leaderboard, captured 23 Oct 2026
COLOURS = {  # one colour per group, readable on the purple background
    "Chinese open weights": "#ff7a6b",
    "US open weights": "#9ef7b1",
    "European fully open": "#5aa9ff",
    "US fully open": "#9ef7b1",
}


def text(x, y, s, size=16, fill=WHITE, anchor="start", weight="normal", style="normal"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" font-style="{style}">{escape(s)}</text>')


def svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="{BG}"/>'
            + "".join(body) + "</svg>\n")


def fully_open(out):
    rows = list(csv.DictReader(open(HERE / "fully_open.csv")))
    benches = [k for k in rows[0] if k not in ("model", "group")]
    width, left, top, chart_h = 1000, 70, 50, 330
    group_w = (width - left - 20) / len(rows)
    bar_w = group_w * 0.8 / len(benches)
    scale = chart_h / 100
    base = top + chart_h
    body = []
    for v in (0, 25, 50, 75, 100):
        yy = base - v * scale
        body.append(f'<line x1="{left}" y1="{yy}" x2="{width - 20}" y2="{yy}" stroke="#5b3a78" stroke-width="1"/>')
        body.append(text(left - 10, yy + 5, str(v), 13, MUTED, anchor="end"))
    # Closed frontier models exist only post-trained, so they get a reference line, not bars
    fy = base - FRONTIER * scale
    body.append(f'<line x1="{left}" y1="{fy:.1f}" x2="{width - 20}" y2="{fy:.1f}" stroke="{WHITE}" '
                f'stroke-width="2.5" stroke-dasharray="10 6"/>')
    body.append(text(width - 24, fy - 10, f"Closed frontier, post-trained: {FRONTIER_RANGE}", 16,
                     anchor="end", weight="bold"))
    for i, r in enumerate(rows):
        gx = left + i * group_w + group_w * 0.1
        colour = COLOURS[r["group"]]
        for j, b in enumerate(benches):
            v = float(r[b])
            x = gx + j * bar_w
            # first benchmark solid, second outlined, so the pair reads without a colour key
            style = f'fill="{colour}"' if j == 0 else f'fill="{BG}" stroke="{colour}" stroke-width="3"'
            body.append(f'<rect x="{x + 2:.1f}" y="{base - v * scale:.1f}" width="{bar_w - 4:.1f}" '
                        f'height="{v * scale:.1f}" rx="2" {style}/>')
            body.append(text(x + bar_w / 2, base - v * scale - 6, f"{v:g}", 13, anchor="middle"))
        cx = left + i * group_w + group_w / 2
        name, size = r["model"].rsplit(" ", 1)
        body.append(text(cx, base + 24, name, 16, anchor="middle", weight="bold"))
        body.append(text(cx, base + 44, size, 14, anchor="middle"))
        body.append(text(cx, base + 64, r["group"], 13, colour, anchor="middle"))
    ky = base + 100
    body.append(f'<rect x="{left}" y="{ky - 13}" width="16" height="16" fill="{WHITE}"/>')
    body.append(text(left + 24, ky, f"{benches[0]} (filled)", 15))
    body.append(f'<rect x="{left + 220}" y="{ky - 13}" width="16" height="16" fill="{BG}" stroke="{WHITE}" stroke-width="3"/>')
    body.append(text(left + 244, ky, f"{benches[1]}, multilingual (outlined)", 15))
    body.append(text(20, ky + 30, "Bars: base models, % correct. Apertus v1.5 technical report, Table 16 "
                     "(arXiv:2610.15542, Oct 2026), self-reported by the Apertus team", 13, MUTED))
    body.append(text(20, ky + 50, "Dashed line: best closed models on MMLU-Pro after post-training (Gemini 4 Argon 93.2, "
                     "Claude Opus 5 91.7, GPT-6 Astra 89.8), Kaggle leaderboard, Oct 2026", 13, MUTED))
    (out / "fully_open.svg").write_text(svg(width, ky + 64, body))


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    fully_open(out)
