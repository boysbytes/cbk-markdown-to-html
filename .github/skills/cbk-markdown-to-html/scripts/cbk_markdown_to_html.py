#!/usr/bin/env python3
"""
cbk_markdown_to_html.py — Convert Markdown to HTML for Chumbaka LMS.

Transforms applied in order:
  1. <h3> → <details><summary> collapsible sections
  2. Emoji <blockquote> → styled <table class="emoji-blockquote">
  3. Nested <ol> inside <li> → type="a"
  4. <br> spacing around <table> elements
  5. (optional) 3 <br> tags after each non-last first-level <ol> <li>

Dependencies:
  pip install markdown beautifulsoup4

Usage:
  python cbk_markdown_to_html.py input.md [output.html] [--no-list-spacing] [--border-radius]

Import as module:
  from cbk_markdown_to_html import convert
  html = convert(markdown_text)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import markdown as _md_lib
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    sys.exit(
        "Missing dependencies. Run:  pip install markdown beautifulsoup4"
    )

# Matches leading Unicode emoji sequences (Python surrogate-free ranges).
# Covers: supplementary plane emoji, misc symbols, variation selectors, ZWJ, keycap.
_EMOJI_RE = re.compile(
    r"^([\U0001F300-\U0001FFFF\u231A-\u32FF\u2600-\u27BF\uFE0F\u200D\u20E3]+)\s*"
)


# ---------------------------------------------------------------------------
# Transform steps
# ---------------------------------------------------------------------------

def _h3_to_collapsible(container: Tag, soup: BeautifulSoup, border_radius: bool) -> None:
    """Replace each top-level <h3> and its following siblings with <details>."""
    while True:
        h3 = container.find("h3", recursive=False)
        if not h3:
            break

        summary = soup.new_tag("summary")
        style = "padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;"
        if border_radius:
            style += "border-radius:10px;"
        summary["style"] = style

        strong = soup.new_tag("strong")
        for node in list(h3.contents):
            node.extract()
            strong.append(node)
        summary.append(strong)

        details = soup.new_tag("details")
        details.append(summary)

        # Collect all consecutive siblings until the next top-level <h3>
        sibling = h3.next_sibling
        while sibling:
            if isinstance(sibling, Tag) and sibling.name == "h3":
                break
            nxt = sibling.next_sibling
            sibling.extract()
            details.append(sibling)
            sibling = nxt

        h3.replace_with(details)


def _emoji_blockquote_to_table(container: Tag, soup: BeautifulSoup) -> None:
    """Convert emoji-prefixed <blockquote> elements to styled callout tables."""
    for blockquote in container.find_all("blockquote"):
        first_child = blockquote.find()  # first element child
        if not first_child:
            continue

        raw = first_child.decode_contents().strip()
        m = _EMOJI_RE.match(raw)
        if not m:
            continue

        emoji = m.group(1)
        remaining_html = raw[m.end():].strip()

        # --- Build table ---
        table = soup.new_tag("table")
        table["style"] = "border-style:none;width:560px;background-color:#ffe5b4;"
        table["border"] = "0"
        table["cellpadding"] = "20"
        # class="emoji-blockquote" required by advanced-spacing getElementType
        table["class"] = "emoji-blockquote"

        tbody = soup.new_tag("tbody")
        tr = soup.new_tag("tr")

        # TD 1 — emoji icon
        td1 = soup.new_tag("td")
        td1["style"] = "width:70.9062px;vertical-align:middle;"
        h3_tag = soup.new_tag("h3")
        h3_tag["style"] = "font-size:48px;margin:0;"
        span = soup.new_tag("span")
        span["style"] = "font-size:48px;"
        span.string = emoji
        h3_tag.append(span)
        td1.append(h3_tag)

        # TD 2 — remaining text and subsequent blockquote children
        td2 = soup.new_tag("td")
        td2["style"] = "width:488.094px;vertical-align:middle;"

        if remaining_html:
            # Parse remaining inline HTML into a <p>
            p_doc = BeautifulSoup(f"<p>{remaining_html}</p>", "html.parser")
            td2.append(p_doc.find("p"))

        # Move subsequent element siblings of first_child into td2
        sib = first_child.find_next_sibling()
        while sib:
            nxt = sib.find_next_sibling()
            sib.extract()
            td2.append(sib)
            sib = nxt

        tr.append(td1)
        tr.append(td2)
        tbody.append(tr)
        table.append(tbody)

        blockquote.replace_with(table)


def _nested_ol_to_alpha(container: Tag) -> None:
    """Set type="a" on ordered lists that are direct children of <li>."""
    for ol in container.find_all("ol"):
        if ol.parent and ol.parent.name == "li":
            attr = ol.get("type", "").strip().lower()
            if not attr or attr == "1":
                ol["type"] = "a"


def _add_table_spacing(container: Tag, soup: BeautifulSoup) -> None:
    """Ensure at least one <br> before and after each <table>."""
    for table in container.find_all("table"):
        # --- Before ---
        # Walk backwards; if a <br> is found before any non-empty content → skip.
        needs_before = True
        prev = table.previous_sibling
        while prev:
            if isinstance(prev, Tag) and prev.name == "br":
                needs_before = False
                break
            if isinstance(prev, Tag) or (
                isinstance(prev, NavigableString) and prev.strip()
            ):
                break  # non-empty, non-br content found → insert <br>
            prev = prev.previous_sibling
        if needs_before:
            table.insert_before(soup.new_tag("br"))

        # --- After ---
        # Count consecutive <br> tags immediately following.
        br_count = 0
        nxt = table.next_sibling
        while nxt and isinstance(nxt, Tag) and nxt.name == "br":
            br_count += 1
            nxt = nxt.next_sibling
        for _ in range(max(0, 1 - br_count)):
            table.insert_after(soup.new_tag("br"))


def _add_list_spacing(container: Tag, soup: BeautifulSoup) -> None:
    """Add 3 <br> tags at the end of each non-last first-level <li> in <ol>."""
    for ol in container.find_all("ol"):
        # Skip nested lists (parent is an <li>)
        if ol.parent and ol.parent.name == "li":
            continue

        items = [c for c in ol.children if isinstance(c, Tag) and c.name == "li"]
        for li in items[:-1]:  # every item except the last
            # Count trailing <br> tags already present
            br_count = 0
            node = li.contents[-1] if li.contents else None
            while node:
                if isinstance(node, Tag) and node.name == "br":
                    br_count += 1
                    node = node.previous_sibling
                elif isinstance(node, NavigableString) and not node.strip():
                    node = node.previous_sibling
                else:
                    break
            for _ in range(max(0, 3 - br_count)):
                li.append(soup.new_tag("br"))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def convert(
    markdown_text: str,
    add_list_spacing: bool = True,
    border_radius: bool = False,
) -> str:
    """Convert a Markdown string to Chumbaka LMS HTML.

    Parameters
    ----------
    markdown_text:
        Source Markdown content.
    add_list_spacing:
        If True (default), append 3 <br> tags after each non-last first-level
        ordered list item.
    border_radius:
        If True, add ``border-radius:10px;`` to collapsible section summaries.

    Returns
    -------
    str
        HTML string ready to paste into Chumbaka LMS.
    """
    converter = _md_lib.Markdown(extensions=["tables", "fenced_code"])
    raw_html = converter.convert(markdown_text)

    # Wrap in a root element for reliable top-level child iteration
    soup = BeautifulSoup(f"<div id='cbk-root'>{raw_html}</div>", "html.parser")
    container = soup.find("div", id="cbk-root")

    _h3_to_collapsible(container, soup, border_radius)
    _emoji_blockquote_to_table(container, soup)
    _nested_ol_to_alpha(container)
    _add_table_spacing(container, soup)
    if add_list_spacing:
        _add_list_spacing(container, soup)

    return container.decode_contents()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Markdown to HTML for Chumbaka LMS.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cbk_markdown_to_html.py lesson.md output.html\n"
            "  python cbk_markdown_to_html.py lesson.md --no-list-spacing\n"
            "  python cbk_markdown_to_html.py lesson.md output.html --border-radius\n"
        ),
    )
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument(
        "output", nargs="?", help="Output HTML file (omit to print to stdout)"
    )
    parser.add_argument(
        "--no-list-spacing",
        action="store_true",
        help="Disable 3-line spacing after first-level numbered list items",
    )
    parser.add_argument(
        "--border-radius",
        action="store_true",
        help="Add rounded corners (border-radius:10px) to collapsible section headers",
    )
    args = parser.parse_args()

    src = Path(args.input)
    if not src.is_file():
        sys.exit(f"File not found: {src}")

    html = convert(
        src.read_text(encoding="utf-8"),
        add_list_spacing=not args.no_list_spacing,
        border_radius=args.border_radius,
    )

    if args.output:
        Path(args.output).write_text(html, encoding="utf-8")
        print(f"Saved to {args.output}")
    else:
        sys.stdout.write(html)


if __name__ == "__main__":
    main()
