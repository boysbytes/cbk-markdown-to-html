#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process a Markdown file, replacing fenced code blocks (``` or ~~~) with
Pygments-highlighted HTML blocks using inline CSS.

- Highlights labelled fences only by default for languages: python, arduino, markdown
  (use --all-languages to highlight any labelled fence)
- Unlabelled fences are left unchanged
- Output remains Markdown with embedded HTML blocks

Examples:
  python highlight_markdown.py --input README.md > README.with-html.md
  python highlight_markdown.py --in-place --input README.md
"""
from __future__ import annotations
import sys
import argparse
import re
from typing import Callable
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from pygments.formatters import HtmlFormatter

DEFAULT_STYLE = "default"
DEFAULT_DIVSTYLES = "border:solid gray;border-width:.0em .0em .0em .8em;padding:.2em .6em;"
DEF_PRE = "margin: 0; font-size: 12pt"
DEF_WRAP = "overflow:auto;width:auto;"
ESSENTIAL = {"python", "arduino", "markdown", "md"}
FENCE_RE = re.compile(r"^(?P<fence>`{3,}|~{3,})(?P<lang>[A-Za-z0-9_+-]*)[ \t]*\n(?P<body>.*?)(?:^\1[ \t]*$)", re.MULTILINE | re.DOTALL)


def _get_lexer(lang: str):
    try:
        return get_lexer_by_name(lang)
    except ClassNotFound:
        if lang.lower() == "arduino":
            return get_lexer_by_name("cpp")
        raise


def _make_formatter(style: str, divstyles: str) -> HtmlFormatter:
    return HtmlFormatter(
        style=style,
        linenos=False,
        noclasses=True,
        cssclass="",
        cssstyles=DEF_WRAP + divstyles,
        prestyles=DEF_PRE,
    )


def _insert_line_numbers(html: str) -> str:
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


def transform_markdown(md: str, formatter: HtmlFormatter, highlight_all: bool, with_linenos: bool) -> str:
    def repl(m: re.Match) -> str:
        fence = m.group("fence")
        lang = (m.group("lang") or "").strip()
        body = m.group("body")
        if not lang:
            return m.group(0)  # keep as-is
        select = highlight_all or (lang.lower() in ESSENTIAL)
        if not select:
            return m.group(0)
        try:
            lexer = _get_lexer(lang)
        except ClassNotFound:
            return m.group(0)
        html = highlight(body, lexer, formatter)
        if with_linenos:
            html = _insert_line_numbers(html)
        return f"\n<!-- highlighted: {lang} -->\n" + html + "\n"

    return FENCE_RE.sub(repl, md)


def main() -> int:
    p = argparse.ArgumentParser(description="Inline-highlight Markdown code fences (HTML blocks emitted)")
    p.add_argument("--input", required=True, help="Path to input Markdown file")
    p.add_argument("--in-place", action="store_true", help="Write changes back to the input file")
    p.add_argument("--style", default=DEFAULT_STYLE, help="Pygments style")
    p.add_argument("--linenos", action="store_true", help="Enable line numbers in code blocks")
    p.add_argument("--divstyles", default=DEFAULT_DIVSTYLES, help="Wrapper CSS for blocks")
    p.add_argument("--all-languages", action="store_true", help="Highlight any labelled fence, not just python/arduino/markdown")

    args = p.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    formatter = _make_formatter(args.style, args.divstyles)
    out = transform_markdown(content, formatter, args.all_languages, args.linenos)

    if args.in_place:
        with open(args.input, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
