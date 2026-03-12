#!/usr/bin/env python3
"""
cbk_markdown_to_html.py — Convert Markdown to HTML for Chumbaka LMS.

Pre-processing steps (before markdown parsing):
  0a. Strip YAML front matter (--- delimited block at start of file)
  0b. Convert indented/blockquote-prefixed fenced code blocks to raw HTML <pre><code>.
      Handles three variants: 4+-space-indented, blockquote-prefixed (> ```),
      and combined (4+-space-indented blockquote, e.g. inside a list item).
  0c. Separate consecutive blockquote blocks with an HTML comment so the
      parser produces separate <blockquote> elements instead of merging them.
  0d. Insert a blank blockquote line between a non-list blockquote line and an
      immediately following list line so parser creates <p> + <ul> not merged <p>.
  0e. Insert a blank line between a plain continuation line and a bullet-list line
      inside list-item content (4+-space-indented) so parser creates <p> + <ul>.

Transforms applied in order (after markdown parsing):
  1. <h3> → <details><summary> collapsible sections
  2. Emoji <blockquote> → styled <table class="emoji-blockquote">
  2b. Non-emoji <blockquote> → bordered <table> with nested list structure
  3. Nested <ol> inside <li> → type="a"
  4a. Add border="1" and border-collapse styling to plain markdown <table> elements
  4b. <br> spacing around <table> elements
  5. (optional) 3 <br> tags after each non-last first-level <ol> <li>
  6. 3 <br> between consecutive <details> elements
  7. 2 <br> appended at end of last <details> element

Dependencies:
  pip install markdown beautifulsoup4

Usage:
  python cbk_markdown_to_html.py input.md              # writes input.html
  python cbk_markdown_to_html.py input.md output.html  # explicit output path
  python cbk_markdown_to_html.py input.md --no-list-spacing
  python cbk_markdown_to_html.py input.md --border-radius

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
        "Missing dependencies. Run:  pip install markdown beautifulsoup4 pygments"
    )

try:
    from pygments import highlight as _pygments_highlight
    from pygments.lexers import get_lexer_by_name as _get_lexer_by_name
    from pygments.util import ClassNotFound as _ClassNotFound
    from pygments.formatters import HtmlFormatter as _HtmlFormatter
    _PYGMENTS_AVAILABLE = True
except ImportError:
    _PYGMENTS_AVAILABLE = False

# Syntax highlighting constants (mirrors the syntax-highlighter skill defaults)
_SYN_STYLE = "default"
_SYN_DIVSTYLES = "border:solid gray;border-width:.0em .0em .0em .8em;padding:.2em .6em;"
_SYN_PRE = "margin: 0; font-size: 12pt"
_SYN_WRAP = "overflow:auto;width:auto;"
# Languages to highlight; anything not in this set is left as plain <pre><code>
_SYN_HIGHLIGHT_LANGS = {"python", "arduino", "cpp", "markdown", "md"}
# Languages whose code blocks are intentionally left unstyled (plain monospace)
_SYN_SKIP_LANGS = {"text"}

# Matches leading Unicode emoji sequences (Python surrogate-free ranges).
# Covers: supplementary plane emoji, misc symbols, variation selectors, ZWJ, keycap.
_EMOJI_RE = re.compile(
    r"^([\U0001F300-\U0001FFFF\u231A-\u32FF\u2600-\u27BF\uFE0F\u200D\u20E3]+)\s*"
)


# ---------------------------------------------------------------------------
# Pre-processing helpers
# ---------------------------------------------------------------------------

def _strip_front_matter(text: str) -> str:
    """Strip YAML front matter (delimited by --- lines) from the start of a markdown string."""
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.DOTALL)
    if m:
        return text[m.end():]
    return text


def _separate_consecutive_blockquotes(text: str) -> str:
    """Insert a separator between adjacent blockquote blocks to prevent the parser
    from merging them into a single <blockquote> element.

    Two consecutive groups of '>' prefixed lines separated by blank lines
    will be given an HTML comment separator so Python's markdown library
    creates two distinct <blockquote> elements.
    """
    lines = text.split("\n")
    result: list[str] = []
    i = 0
    while i < len(lines):
        result.append(lines[i])
        # If this line is a blockquote line, look ahead
        if lines[i].startswith(">"):
            # Collect following blank lines
            j = i + 1
            blank_count = 0
            while j < len(lines) and lines[j].strip() == "":
                j += 1
                blank_count += 1
            # If blank lines found and next non-blank line is also a blockquote
            if blank_count > 0 and j < len(lines) and lines[j].startswith(">"):
                # Emit the blank lines, then a separator, then continue
                for _ in range(blank_count):
                    result.append("")
                result.append("<!-- blockquote-break -->")
                i = j
                continue
        i += 1
    return "\n".join(result)


def _fix_blockquote_heading_list(text: str) -> str:
    """Insert a blank blockquote line between a non-list blockquote line and an
    immediately following list marker line inside the same blockquote block.

    This ensures the markdown parser produces a <p> followed by a <ul> rather
    than merging them into a single <p> element.
    """
    lines = text.split("\n")
    result: list[str] = []
    for i, line in enumerate(lines):
        result.append(line)
        if not line.startswith(">"):
            continue
        # Look ahead for a list marker line
        if i + 1 >= len(lines):
            continue
        next_line = lines[i + 1]
        if not next_line.startswith(">"):
            continue
        # Current line is a blockquote line but NOT a list item
        stripped_current = re.sub(r"^>+\s*", "", line)
        if re.match(r"^[-*]\s", stripped_current):
            continue  # current is already a list item
        # Next line IS a list item
        stripped_next = re.sub(r"^>+\s*", "", next_line)
        if re.match(r"^[-*]\s", stripped_next):
            # Insert a blank blockquote line between them
            result.append(">")
    return "\n".join(result)


def _fix_paragraph_list_in_list_items(text: str) -> str:
    """Insert a blank line between a non-list continuation line and an
    immediately following bullet marker line inside a list item.

    Inside list items (4+ space-indented content), a plain continuation line
    followed directly by a bullet item (without a blank line between them)
    gets merged into a single paragraph by most markdown parsers.  Adding the
    blank line causes the parser to produce a proper <p> + <ul> structure.

    Example
    -------
    Before::

        The sigmoid function has an S-shaped curve:
        - When z is very negative, probability is close to 0
        - When z is very positive, probability is close to 1

    After::

        The sigmoid function has an S-shaped curve:

        - When z is very negative, probability is close to 0
        - When z is very positive, probability is close to 1
    """
    lines = text.split("\n")
    result: list[str] = []
    for i, line in enumerate(lines):
        result.append(line)
        if i + 1 >= len(lines):
            continue
        next_line = lines[i + 1]
        # Current line must be an indented (list-item continuation) non-bullet, non-blank line
        if not re.match(r"^ {4,}\S", line):
            continue
        if re.match(r"^ {4,}[-*]\s", line):
            continue  # current line is already a bullet
        if re.match(r"^ {4,}\d+\.\s", line):
            continue  # current line is a numbered item
        if re.match(r"^ {4,}>", line):
            continue  # current line is a blockquote (handled separately)
        # Next line is an indented bullet → insert blank line
        if re.match(r"^ {4,}[-*]\s", next_line):
            result.append("")
    return "\n".join(result)


def _preprocess_fenced_code_in_lists(text: str) -> tuple[str, dict[str, str]]:
    """Replace fenced code blocks that Python markdown cannot handle with placeholders.

    Three cases are covered:

    1. **Indented fenced blocks** (inside list items) — indented by 4+ spaces.
       Python markdown's fenced_code extension does not reliably render these:
       blank lines inside the block cause it to be split into multiple paragraphs.

    2. **Blockquote-prefixed fenced blocks** — lines starting with ``>`` that open
       a fenced code block on the same line (e.g. ``> ```text``).  Python
       markdown misparses the opening fence as inline code.

    3. **Blockquote-prefixed fenced blocks inside list items** — lines with 4+
       leading spaces followed by a ``>`` prefix (e.g. ``    > ```text``).
       This combination is not handled by either case 1 or case 2 above.

    All cases are replaced with a unique placeholder token.  After markdown
    parsing the caller must call :func:`_restore_code_placeholders` to substitute
    the tokens back with the correct ``<pre><code>`` HTML.

    Returns
    -------
    tuple[str, dict[str, str]]
        Modified markdown text and a ``{placeholder_key: html}`` mapping.
    """
    lines = text.split("\n")
    result: list[str] = []
    in_fenced = False
    fence_indent = ""      # string prefix that must match on every content/close line
    fence_marker = ""
    lang = ""
    code_lines: list[str] = []
    placeholders: dict[str, str] = {}
    counter = 0

    for line in lines:
        if not in_fenced:
            # Case 1: indented fenced block (4+ spaces, inside list item)
            m_indent = re.match(r"^( {4,})(```+|~~~+)(\S*)$", line)
            # Case 2: blockquote-prefixed fenced block  (> ```lang)
            m_bq = re.match(r"^(>+ *)(```+|~~~+)(\S*)$", line)
            # Case 3: blockquote inside list item  (    > ```lang)
            m_bq_in_list = re.match(r"^( {4,})(>+ *)(```+|~~~+)(\S*)$", line)

            if m_bq_in_list:
                # Must test before m_indent: both match indented lines, but
                # m_indent would not match (its group 2 would need to start
                # with a backtick, not '>'), so order is a safeguard.
                in_fenced = True
                fence_indent = m_bq_in_list.group(1) + m_bq_in_list.group(2)
                fence_marker = m_bq_in_list.group(3)
                lang = m_bq_in_list.group(4)
                code_lines = []
            elif m_indent:
                in_fenced = True
                fence_indent = m_indent.group(1)
                fence_marker = m_indent.group(2)
                lang = m_indent.group(3)
                code_lines = []
            elif m_bq:
                in_fenced = True
                fence_indent = m_bq.group(1)
                fence_marker = m_bq.group(2)
                lang = m_bq.group(3)
                code_lines = []
            else:
                result.append(line)
        else:
            end_pattern = r"^" + re.escape(fence_indent) + re.escape(fence_marker) + r"\s*$"
            if re.match(end_pattern, line):
                in_fenced = False
                lang_attr = f' class="language-{lang}"' if lang else ""
                code_content = ""
                for cl in code_lines:
                    # Strip the fence prefix (indentation or blockquote markers).
                    if cl.startswith(fence_indent):
                        cl = cl[len(fence_indent):]
                    # Escape HTML special characters inside the code block.
                    cl = cl.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    code_content += cl + "\n"
                html = f"<pre><code{lang_attr}>{code_content}</code></pre>"
                key = f"CBKCODE{counter}PLACEHOLDER"
                counter += 1
                placeholders[key] = html
                # For blockquote-prefixed fences, wrap the placeholder in blank
                # blockquote lines so the markdown parser produces a standalone
                # <p>key</p> rather than appending the token to the preceding
                # paragraph.  This ensures _restore_code_placeholders can do a
                # clean <p>key</p> → <pre><code> substitution.
                if ">" in fence_indent:
                    # Wrap the placeholder in blank blockquote lines so the
                    # parser produces a standalone <p>key</p> rather than
                    # appending the token to the preceding paragraph.  This
                    # works for pure blockquotes ("> ") and blockquotes inside
                    # list items ("    > ").
                    bq_blank = fence_indent.rstrip()  # strip trailing space after ">"
                    result.append(bq_blank)
                    result.append(fence_indent + key)
                    result.append(bq_blank)
                else:
                    # Emit the placeholder at the same indentation level so the
                    # markdown parser places it inside the correct list item.
                    result.append(fence_indent + key)
            else:
                code_lines.append(line)

    if in_fenced:
        # Unclosed fence — emit as-is so the document is not silently truncated.
        result.append(f"{fence_indent}{fence_marker}{lang}")
        result.extend(code_lines)

    return "\n".join(result), placeholders


def _restore_code_placeholders(html: str, placeholders: dict[str, str]) -> str:
    """Replace code placeholder tokens in HTML with the actual ``<pre><code>`` blocks.

    Python markdown may wrap placeholder tokens in ``<p>...</p>`` and may
    insert a trailing newline inside the tag (e.g. ``<p>KEY\\n</p>``).  A
    regex match is used to handle both variants cleanly.
    """
    for key, replacement in placeholders.items():
        # Match <p>KEY</p> with optional surrounding whitespace.
        html = re.sub(r"<p>\s*" + re.escape(key) + r"\s*</p>", replacement, html)
        # Fallback: replace any remaining bare token (e.g. inside a list item).
        html = html.replace(key, replacement)
    return html


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


def _non_emoji_blockquote_to_table(container: Tag, soup: BeautifulSoup) -> None:
    """Convert non-emoji <blockquote> elements to single-column bordered tables.

    The table uses a white background with a visible border.  Lists inside the
    blockquote are converted to the nested ``ul > li[none] > ul > li[aria]``
    structure used by the Chumbaka LMS.
    """
    for blockquote in list(container.find_all("blockquote")):
        # Build table wrapper
        table = soup.new_tag("table")
        table["style"] = "border-collapse: collapse; width: 100%; background-color: #ffffff;"
        table["border"] = "1"
        table["cellpadding"] = "20"

        tbody = soup.new_tag("tbody")
        tr = soup.new_tag("tr")
        td = soup.new_tag("td")
        td["style"] = "width: 100%;"

        for child in list(blockquote.children):
            if isinstance(child, NavigableString):
                continue  # skip bare whitespace text nodes

            if child.name in ("ul", "ol"):
                # Convert to nested list structure
                outer_ul = soup.new_tag("ul")
                outer_li = soup.new_tag("li")
                outer_li["style"] = "list-style-type: none;"
                inner_ul = soup.new_tag("ul")

                for item in list(child.find_all("li", recursive=False)):
                    new_li = soup.new_tag("li")
                    new_li["aria-level"] = "1"
                    new_li.extend(list(item.children))
                    inner_ul.append(new_li)

                outer_li.append(inner_ul)
                outer_ul.append(outer_li)
                td.append(outer_ul)

            elif child.name == "p":
                # Detect bold-only paragraph → heading
                contents = [c for c in child.children
                            if not (isinstance(c, NavigableString) and c.strip() == "")]
                if (len(contents) == 1
                        and isinstance(contents[0], Tag)
                        and contents[0].name == "strong"):
                    heading_text = contents[0].decode_contents().rstrip(":")
                    new_p = BeautifulSoup(
                        f"<p><strong>{heading_text}</strong></p>", "html.parser"
                    ).find("p")
                    td.append(new_p)
                else:
                    td.append(child.__copy__())
            else:
                td.append(child.__copy__())

        tr.append(td)
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


def _style_markdown_tables(container: Tag) -> None:
    """Add border and border-collapse styling to plain markdown tables.

    Regular markdown tables (generated by the ``tables`` extension) have no
    border attributes.  This step adds ``border="1"`` and
    ``style="border-collapse: collapse;"`` to every ``<table>`` that has not
    already been styled by one of the blockquote transforms.

    Styled tables (emoji callout and non-emoji blockquote) already carry an
    explicit ``border`` attribute, so they are skipped.
    """
    for table in container.find_all("table"):
        # Skip tables already created by blockquote transforms (they have border set)
        if table.get("border") is not None:
            continue
        table["border"] = "1"
        existing_style = table.get("style", "")
        if "border-collapse" not in existing_style:
            collapse_style = "border-collapse: collapse;"
            table["style"] = (
                (collapse_style + " " + existing_style).strip()
                if existing_style
                else collapse_style
            )


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


def _add_details_spacing(container: Tag, soup: BeautifulSoup) -> None:
    """Append trailing <br> tags inside each <details> element.

    - Every non-last <details>: append 3 <br> at the end of its content so
      there is visual separation before the next section when expanded.
    - Last <details>: append 2 <br> at the end of its content.

    All <br> tags are placed *inside* the <details> elements so they are only
    visible when a section is expanded, not as blank space between collapsed
    section headers.
    """
    details_list = [c for c in container.children
                    if isinstance(c, Tag) and c.name == "details"]
    if not details_list:
        return

    # 3 <br> at the end of each non-last <details> (inside)
    for det in details_list[:-1]:
        for _ in range(3):
            det.append(soup.new_tag("br"))

    # 2 <br> at the end of the last <details> (inside)
    last = details_list[-1]
    for _ in range(2):
        last.append(soup.new_tag("br"))


def _add_sub_list_spacing(container: Tag, soup: BeautifulSoup) -> None:
    """Add 2 <br> tags at the end of each non-last <li> in nested <ol> (sub-numbered lists).

    Targets only <ol> elements that are direct children of <li> (i.e. the
    alphabetical sub-lists produced by Transform 3).  Each non-last sub-item
    gets 2 trailing <br> tags for visual breathing room inside long steps.
    """
    for ol in container.find_all("ol"):
        # Only target nested lists (parent is an <li>)
        if not (ol.parent and ol.parent.name == "li"):
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
            for _ in range(max(0, 2 - br_count)):
                li.append(soup.new_tag("br"))


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
# Syntax highlighting (step 8)
# ---------------------------------------------------------------------------

def _apply_syntax_highlighting(html: str) -> str:
    """Replace ``<pre><code class="language-X">`` blocks with Pygments inline-CSS HTML.

    Only languages listed in ``_SYN_HIGHLIGHT_LANGS`` are processed.  Blocks
    with ``language-text`` or an unknown language label are left unchanged.
    Blocks with no language class are also left unchanged.

    Requires Pygments (``pip install pygments``).  If Pygments is not
    installed, ``_PYGMENTS_AVAILABLE`` is ``False`` and this function should
    not be called.
    """
    soup = BeautifulSoup(f"<div>{html}</div>", "html.parser")
    container = soup.find("div")

    formatter = _HtmlFormatter(
        style=_SYN_STYLE,
        linenos=False,
        noclasses=True,
        cssclass="",
        cssstyles=_SYN_WRAP + _SYN_DIVSTYLES,
        prestyles=_SYN_PRE,
    )

    for pre_tag in container.find_all("pre"):
        code_tag = pre_tag.find("code")
        if not code_tag:
            continue

        # Determine language from class, e.g. "language-cpp" → "cpp"
        classes = code_tag.get("class") or []
        lang = ""
        for cls in classes:
            if cls.startswith("language-"):
                lang = cls[len("language-"):].lower()
                break

        if not lang or lang in _SYN_SKIP_LANGS:
            continue
        if lang not in _SYN_HIGHLIGHT_LANGS:
            continue

        # Resolve lexer (arduino falls back to cpp)
        actual_lang = "cpp" if lang == "arduino" else lang
        try:
            lexer = _get_lexer_by_name(actual_lang)
        except _ClassNotFound:
            continue

        # .get_text() decodes HTML entities so Pygments receives clean source code
        code_text = code_tag.get_text()

        highlighted = _pygments_highlight(code_text, lexer, formatter)

        # Replace the <pre> tag in-place with the Pygments HTML fragment
        highlighted_soup = BeautifulSoup(highlighted, "html.parser")
        pre_tag.replace_with(highlighted_soup)

    return container.decode_contents()


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
    markdown_text = _strip_front_matter(markdown_text)
    markdown_text = _separate_consecutive_blockquotes(markdown_text)
    markdown_text = _fix_blockquote_heading_list(markdown_text)
    markdown_text = _fix_paragraph_list_in_list_items(markdown_text)
    markdown_text, code_placeholders = _preprocess_fenced_code_in_lists(markdown_text)

    converter = _md_lib.Markdown(extensions=["tables", "fenced_code"])
    raw_html = converter.convert(markdown_text)
    raw_html = _restore_code_placeholders(raw_html, code_placeholders)
    # Remove the blockquote-break separator comments (Step 0c cleanup)
    raw_html = raw_html.replace("<!-- blockquote-break -->", "")

    # Wrap in a root element for reliable top-level child iteration
    soup = BeautifulSoup(f"<div id='cbk-root'>{raw_html}</div>", "html.parser")
    container = soup.find("div", id="cbk-root")

    _h3_to_collapsible(container, soup, border_radius)
    _emoji_blockquote_to_table(container, soup)
    _non_emoji_blockquote_to_table(container, soup)
    _nested_ol_to_alpha(container)
    _style_markdown_tables(container)
    _add_table_spacing(container, soup)
    if add_list_spacing:
        _add_list_spacing(container, soup)
    _add_sub_list_spacing(container, soup)
    _add_details_spacing(container, soup)

    html = container.decode_contents()
    if _PYGMENTS_AVAILABLE:
        html = _apply_syntax_highlighting(html)
    return html


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

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = src.with_suffix(".html")

    html = convert(
        src.read_text(encoding="utf-8"),
        add_list_spacing=not args.no_list_spacing,
        border_radius=args.border_radius,
    )

    out_path.write_text(html, encoding="utf-8")
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
