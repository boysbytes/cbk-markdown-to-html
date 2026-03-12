---
name: cbk-markdown-to-html
description: 'Convert Markdown to HTML for Chumbaka LMS with custom transforms. Use when: user says "Chumbaka", "LMS authoring", "convert for LMS", or requests "markdown to HTML with custom transforms"; user needs H3 headings converted to collapsible sections; user needs emoji blockquotes converted to styled callout tables; user requests Chumbaka-specific HTML output. For standard markdown-to-HTML without LMS customisation, use the markdown-to-html skill instead.'
---

# CBK Markdown to HTML

Converts Markdown to HTML with Chumbaka LMS-specific transforms. Use the included Python script for programmatic conversion, or apply the rules manually as an AI agent.

## Quick Start

### Programmatic (recommended)

Script at `scripts/cbk_markdown_to_html.py`:

```bash
# Install dependencies once
pip install markdown beautifulsoup4

# Convert a file — output defaults to input filename with .html extension
python cbk_markdown_to_html.py input.md

# Explicit output path
python cbk_markdown_to_html.py input.md output.html

# With options
python cbk_markdown_to_html.py input.md --no-list-spacing --border-radius
```

Import as a module:

```python
from cbk_markdown_to_html import convert
html = convert(markdown_text)
```

### Manual (AI agent)

1. Strip YAML front matter (the `---` block at the start of the file) before converting.
2. Parse markdown with a standard parser.
3. Apply the four transforms **in order** (details in [cbk-transforms.md](references/cbk-transforms.md)):
   - H3 → collapsible sections
   - Emoji blockquotes → styled callout tables
   - Nested ordered lists → alphabetical numbering
   - Spacing: `<br>` around tables; optional 3 `<br>` after numbered list items
4. **Write the output to a file** — use the same base name as the input with a `.html` extension (e.g. `A1_Class.md` → `A1_Class.html`). Do not only display it in the chat.

## Transforms at a Glance

| # | Transform | Trigger | Output |
|---|-----------|---------|--------|
| 1 | H3 collapsible | `<h3>Step 1</h3>` | `<details><summary …><strong>Step 1</strong></summary>…</details>` |
| 2a | Emoji callout | `<blockquote><p>💡 …</p></blockquote>` | `<table class="emoji-blockquote" …>…</table>` |
| 2b | Non-emoji blockquote | `<blockquote>` (no leading emoji) | `<table style="border-collapse:collapse;width:100%;background-color:#ffffff;" border="1" cellpadding="20">…</table>` |
| 3 | Nested OL alpha | `<li><ol><li>…` | `<li><ol type="a"><li>…` |
| 4a | Markdown table border | `<table>` (no existing border) | `<table border="1" style="border-collapse: collapse;">` |
| 4b | Table spacing | `…<table>…` | `…<br><table>…<br>` |
| 4c | List spacing | `<li>item</li><li>` | `<li>item<br><br><br></li><li>` |
| 4c | Sub-list spacing | non-last `<li>` inside nested `<ol type="a">` | append `<br><br>` at end of each non-last sub-item |
| 5 | Section trailing spacing | last element in each non-last `<details>` | append `<br><br><br>` inside section |
| 5 | Last section trailing | last element in last `<details>` | append `<br><br>` inside section |

Full rules, examples, and edge cases: [cbk-transforms.md](references/cbk-transforms.md).

## Configuration Options

| Option | Default | CLI flag | Description |
|--------|---------|----------|-------------|
| Numbered list spacing | ON | `--no-list-spacing` | 3 `<br>` after each non-last first-level `<li>` |
| Border radius on summary | OFF | `--border-radius` | Adds `border-radius:10px;` to section headers |
| Section-to-section spacing | 3 | — | `<br>` count appended inside each non-last `<details>` (visible only when expanded) |
| Last section trailing spacing | 2 | — | `<br>` count appended inside the last `<details>` block |

When converting manually, ask: "Add 3-line spacing after numbered list items? (default: yes)" and "Add rounded corners to section titles? (default: no)". Section-to-section spacing (3 `<br>`) and last-section trailing spacing (2 `<br>`) are always applied.

## Pre-processing Rules

Apply these **before** passing the markdown text to the parser.

| Step | Rule | Why |
|------|------|-----|
| 0a | Strip YAML front matter (`---` block) | Prevents it rendering as raw paragraph text |
| 0b | Replace fenced code blocks (indented 4+, `>` prefixed, or both) with placeholders | Python's `markdown` library misparses these |
| 0c | Inject `<!-- blockquote-break -->` between adjacent blockquote groups | Prevents parser merging them into one `<blockquote>` |
| 0d | Insert blank `>` line between a non-list blockquote line and an immediately following `> - ` list line | Produces `<p>` + `<ul>` instead of merged `<p>` |
| 0e | Insert blank line between a plain continuation line and a bullet marker line inside a list item (4+ space indent) | Produces `<p>` + `<ul>` instead of merged `<p>` |

Full rules: [cbk-transforms.md](references/cbk-transforms.md).

## Output Format

Return a raw HTML string — no `<html>`/`<body>` wrapper, no code fences. Suitable for pasting directly into Chumbaka LMS editor fields.

**Always write the output to a file.** Use the input filename with a `.html` extension unless the user specifies otherwise.

## Critical Rules for AI Agents

These are the most commonly violated rules that produce incorrect output.

### 1. Strip YAML front matter first

Remove the `---` delimited front matter block before passing text to the markdown parser. Otherwise it renders as raw paragraph content.

### 2. All siblings between H3 headings go inside `<details>`

Every element that follows an `<h3>` — including paragraphs, ordered/unordered lists, images, blockquotes, and callout tables — must be placed **inside** the corresponding `<details>` block.  Collect siblings continuously until the next `<h3>` or end of document. Do not stop collecting at the end of a numbered list if non-H3 content follows.

```
Section boundary: <h3>Step 1</h3>  <--- opens a new <details>
  <ol>…</ol>                        ]
  <blockquote>…</blockquote>        ]  ALL go inside the same <details>
  <table>…</table>                  ]
<h3>Step 2</h3>                     <--- opens the NEXT <details>
```

### 3. Emoji callout table is always two columns

Every emoji callout becomes a two-column `<table>`:
- **Column 1 (left)**: the emoji inside `<h3 style="font-size:48px;margin:0;"><span style="font-size:48px;">EMOJI</span></h3>`
- **Column 2 (right)**: all remaining text and elements (paragraphs, code blocks, lists)

Never merge the emoji into a single cell with the text.

```html
<table class="emoji-blockquote" style="border-style:none;width:560px;background-color:#ffe5b4;" border="0" cellpadding="20">
  <tbody><tr>
    <td style="width:70.9062px;vertical-align:middle;">
      <h3 style="font-size:48px;margin:0;"><span style="font-size:48px;">💡</span></h3>
    </td>
    <td style="width:488.094px;vertical-align:middle;">
      <p>The tip content goes here.</p>
    </td>
  </tr></tbody>
</table>
```

### 4. Do not omit section content

Every H3 section has content. If a section like "Share and reflect" seems empty, check the full source — the content is there as a numbered list inside the section.

### 5. Write output to a file

After conversion, always write the HTML to a file on disk. Do not only show it in the chat response. Use the same base name as the input file with a `.html` extension.

### 6. Separate consecutive blockquotes

Consecutive markdown blockquote blocks (two groups of `>` lines separated by a blank line) must produce **separate** `<blockquote>` elements. Some parsers (such as Python's `markdown` library) merge them. Before parsing, insert a non-blockquote separator between consecutive blockquote blocks:

```
Pattern: Two groups of lines starting with > separated by one or more blank lines
Action:  Insert an HTML comment <!-- blockquote-break --> between them
Result:  Parser creates two separate <blockquote> elements
```

Also, if a blockquote contains a bold-only line immediately followed by list items (with no blank line between), insert a blank blockquote line `>` between them so the parser creates a `<p>` followed by a `<ul>` (not a merged single `<p>`).

### 7. Non-emoji blockquotes use the bordered table format

Every `<blockquote>` whose content does **not** start with an emoji becomes a single-column bordered table (white background):

```html
<table style="border-collapse: collapse; width: 100%; background-color: #ffffff;" border="1" cellpadding="20">
<tbody>
<tr>
<td style="width: 100%;">
<!-- content goes here -->
</td>
</tr>
</tbody>
</table>
```

Content conversion rules inside the `<td>`:
- **Bold-only paragraph** (`<p><strong>text</strong></p>` or bold text ending with `:`): render as `<p><strong>heading text</strong></p>` (strip the trailing colon if present).
- **List** (`<ul>` or `<ol>`): convert each item to the nested structure:

  ```html
  <ul>
  <li style="list-style-type: none;">
  <ul>
  <li aria-level="1">Item text</li>
  </ul>
  </li>
  </ul>
  ```

- **Regular paragraph**: render as `<p>content</p>` unchanged.

See full algorithm and examples in [cbk-transforms.md](references/cbk-transforms.md).

## Testing Checklist

- [ ] YAML front matter stripped (not present in output as raw text)
- [ ] Consecutive markdown blockquotes produce separate `<blockquote>` elements (not merged)
- [ ] All top-level `<h3>` wrapped in `<details><summary>`
- [ ] Summary has `padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;`
- [ ] Every element between consecutive H3 headings is inside the `<details>` block (including trailing blockquotes and callout tables)
- [ ] Emoji blockquotes converted to two-column tables with `background-color:#ffe5b4;`
- [ ] Emoji column uses `<h3 style="font-size:48px;margin:0;"><span style="font-size:48px;">EMOJI</span></h3>`
- [ ] Emoji tables have `class="emoji-blockquote"`
- [ ] Non-emoji blockquotes converted to single-column bordered tables (`border="1"`, `background-color:#ffffff;`)
- [ ] List items inside non-emoji blockquote tables use the `li[list-style-type:none] > ul > li[aria-level="1"]` nested structure
- [ ] Bold-only paragraphs inside non-emoji blockquote tables rendered as `<p><strong>…</strong></p>`
- [ ] Nested `<ol>` inside `<li>` have `type="a"`
- [ ] `<br>` present before and after each `<table>`
- [ ] 3 `<br>` appended inside each non-last `<details>` element (after its last child, before `</details>`)
- [ ] Last `<details>` element has `<br><br>` appended inside (before `</details>`)
- [ ] (if enabled) 3 `<br>` at end of each non-last top-level `<li>` in `<ol>`
- [ ] 2 `<br>` at end of each non-last `<li>` inside nested `<ol type="a">` (sub-numbered items)
- [ ] Fenced code blocks in emoji callout blockquotes render as `<pre><code>` (not inline `<code>` or raw backtick text)
- [ ] Fenced code blocks inside list-item blockquotes (4+-space-indented `>` lines) render as `<pre><code>`
- [ ] Plain markdown tables have `border="1"` and `style="border-collapse: collapse;"`
- [ ] Emoji tables do NOT get extra `border` or `border-collapse` styling
- [ ] Output written to `.html` file on disk

## Quality Check Before Handing Off

**Always perform these checks before presenting the output as complete.**

1. Open (or scan) the output `.html` file and verify:
   - All `<h3>` sections are wrapped in `<details><summary>` blocks.
   - All emoji blockquotes render as two-column peach tables — no raw `<code>` text inside them.
   - All non-emoji blockquotes render as single-column white bordered tables.
   - All plain markdown tables have `border="1"` and `border-collapse: collapse;`.
   - Paragraph + bullet-list combinations inside list items are separate elements (not merged into one `<p>`).
   - Fenced code blocks inside blockquotes inside list items render as `<pre><code>`, not inline code or raw text.
2. If any issue is detected, fix it before handing off.

## Advanced Spacing

For precise element-to-element spacing matching the vanilla web tool, see [advanced-spacing.md](references/advanced-spacing.md).
