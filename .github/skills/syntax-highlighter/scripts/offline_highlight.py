#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Offline single-snippet highlighter using Pygments with inline CSS.

Examples:
  echo "print('hi')" | python offline_highlight.py --lexer python
  python offline_highlight.py --lexer arduino --input sketch.ino > sketch.html
"""
from __future__ import annotations
import sys
import argparse
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from pygments.formatters import HtmlFormatter

DEFAULT_STYLE = "default"
DEFAULT_DIVSTYLES = "border:solid gray;border-width:.0em .0em .0em .8em;padding:.2em .6em;"
DEF_PRE = "margin: 0; font-size: 12pt"
DEF_WRAP = "overflow:auto;width:auto;"


def _get_lexer(lang: str, **options):
    try:
        return get_lexer_by_name(lang, **options)
    except ClassNotFound:
        if lang.lower() == "arduino":
            # Fallback to CPP if Arduino lexer unavailable
            return get_lexer_by_name("cpp", **options)
        raise


essential_langs = ["python", "arduino", "markdown"]


def read_input(path: str | None) -> str:
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def main() -> int:
    p = argparse.ArgumentParser(description="Offline snippet highlighter (HTML out)")
    p.add_argument("--lexer", required=True, help=f"Lexer name (e.g., {', '.join(essential_langs)})")
    p.add_argument("--input", help="Path to input file (defaults to stdin)")
    p.add_argument("--style", default=DEFAULT_STYLE, help="Pygments style (default)")
    p.add_argument("--linenos", action="store_true", help="Enable line numbers")
    p.add_argument("--divstyles", default=DEFAULT_DIVSTYLES, help="Wrapper CSS")

    args = p.parse_args()

    code = read_input(args.input)

    formatter = HtmlFormatter(
        style=args.style,
        linenos=False,  # handled manually to match hilite.me behavior
        noclasses=True,
        cssclass="",
        cssstyles=DEF_WRAP + args.divstyles,
        prestyles=DEF_PRE,
    )

    html = highlight(code, _get_lexer(args.lexer), formatter)

    if args.linenos:
        # Simple line number inserter compatible with <pre> blocks
        html = _insert_line_numbers(html)

    sys.stdout.write("<!-- HTML generated offline using Pygments -->" + html)
    return 0


def _insert_line_numbers(html: str) -> str:
    import re
    m = re.search(r"(<pre[^>]*>)(.*?)(</pre>)", html, re.DOTALL)
    if not m:
        return html
    pre_open, pre, pre_close = m.group(1), m.group(2), m.group(3)
    html = html.replace(pre_close, "</pre></td></tr></table>")
    numbers = range(1, pre.count("\n") + 1)
    fmt = "%" + str(len(str(numbers[-1]))) + "i"
    lines = "\n".join(fmt % i for i in numbers)
    html = html.replace(pre_open, '<table><tr><td>' + pre_open + lines + '</pre></td><td>' + pre_open)
    return html


if __name__ == "__main__":
    raise SystemExit(main())
