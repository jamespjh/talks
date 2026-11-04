#!/usr/bin/env python3
"""Put product logos inside Graphviz diagrams, with hover tooltips.

Graphviz can only reference images by path, and an SVG shown through <img>
neither loads those nor shows tooltips. So:

  logos.py prepare OUTDIR
      Write a copy of each logo in ../stored/logos to OUTDIR with an explicit
      size, which dot needs for <IMG SRC="OUTDIR/name.svg"/> in HTML labels.
      Aliases (e.g. myservices -> servicenow) get their own copy.

  logos.py inline FILE.svg
      Replace each <image> dot wrote for those copies with the logo itself,
      inlined, coloured by the node it sits in (CSS below), with a <title>
      so the browser shows the product name on hover. Drop Graphviz's own
      node/edge <title>s, which would otherwise show internal ids on hover.

Embed the result with <object>, not <img>, for the tooltips to work.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGOS = HERE.parent / "stored" / "logos"
SIZE = 34  # px in each sized copy; dot draws it at 3/4 of that in points

# name used in the .dot file -> (logo file, tooltip)
NAMES = {
    "airia": ("airia", "Airia"),
    "claude": ("claude", "Claude apps"),
    "litellm": ("litellm", "LiteLLM"),
    "vllm": ("vllm", "vLLM"),
    "meta": ("meta", "Llama (Meta)"),
    "mistralai": ("mistralai", "Mistral"),
    "qwen": ("qwen", "Qwen"),
    "anthropic": ("anthropic", "Anthropic (Claude)"),
    "openai": ("openai", "OpenAI (GPT)"),
    "googlegemini": ("googlegemini", "Google (Gemini)"),
    "modelcontextprotocol": ("modelcontextprotocol", "Model Context Protocol (MCP)"),
    "jira": ("jira", "Jira"),
    "myservices": ("servicenow", "MyServices (ServiceNow)"),
}
KEEP_COLOURS = {"litellm"}  # multi-colour marks that don't survive recolouring

STYLE = """<style>
  g.node { color: #3c1657; }
  g.node.hl { color: #f5f5f5; }
  g.node.dim { color: #9c88ad; }
  g.node.dim svg.logo-own-colours { opacity: 0.4; }
</style>"""


def logo_svg(name):
    return (LOGOS / f"{NAMES[name][0]}.svg").read_text()


def prepare(outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        svg = logo_svg(name)
        svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
        svg = svg.replace("<svg ", f'<svg width="{SIZE}" height="{SIZE}" ', 1)
        # dot only recognises an SVG image if it starts with an XML declaration
        (out / f"{name}.svg").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + svg)


def inline_logo(name, x, y, w, h):
    svg = logo_svg(name)
    viewbox = re.search(r'viewBox="([^"]+)"', svg).group(1)
    vx, vy, vw, vh = viewbox.split()  # transparent rect over the whole logo, so gaps in it still hover
    inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    if name in KEEP_COLOURS:
        cls, fill = "logo logo-own-colours", ""
    else:
        cls, fill = "logo", ' fill="currentColor"'
        inner = re.sub(r'\sfill="(?!none)[^"]*"', "", inner)
    tooltip = NAMES[name][1]
    return (f'<svg class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{viewbox}"{fill}>'
            f'<title>{tooltip}</title><rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" fill="transparent"/>'
            f"{inner}</svg>")


def inline(path):
    p = Path(path)
    s = p.read_text()

    def repl(m):
        tag = m.group(0)
        name = re.search(r'href="[^"]*/([a-z]+)\.svg"', tag).group(1)
        attr = lambda a: re.search(rf'\s{a}="([^"]+)"', tag).group(1)
        return inline_logo(name, attr("x"), attr("y"), attr("width"), attr("height"))

    s = re.sub(r"<image\b[^>]*/>", repl, s)
    # Graphviz titles the graph and each node and edge with its id; those would pop up on hover
    s = re.sub(r'(<g id="(?:graph|node|edge)\d+" class="(?:graph|node|edge)[^"]*"[^>]*>)\s*<title>.*?</title>', r"\1", s, flags=re.S)
    s = re.sub(r"(<svg\b[^>]*>)", r"\1" + STYLE.replace("\\", r"\\"), s, count=1)
    p.write_text(s)


if __name__ == "__main__":
    cmd, arg = sys.argv[1], sys.argv[2]
    {"prepare": prepare, "inline": inline}[cmd](arg)
