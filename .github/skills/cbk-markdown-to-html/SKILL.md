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

# Convert a file
python cbk_markdown_to_html.py input.md output.html

# With options
python cbk_markdown_to_html.py input.md output.html --no-list-spacing --border-radius
```

Import as a module:

```python
from cbk_markdown_to_html import convert
html = convert(markdown_text)
```

### Manual (AI agent)

1. Parse markdown with a standard parser
2. Apply the four transforms **in order** (details in [cbk-transforms.md](references/cbk-transforms.md)):
   - H3 → collapsible sections
   - Emoji blockquotes → styled callout tables
   - Nested ordered lists → alphabetical numbering
   - Spacing: `<br>` around tables; optional 3 `<br>` after numbered list items
3. Return a clean HTML string — no wrapper, no code block

## Transforms at a Glance

| # | Transform | Trigger | Output |
|---|-----------|---------|--------|
| 1 | H3 collapsible | `<h3>Step 1</h3>` | `<details><summary …><strong>Step 1</strong></summary>…</details>` |
| 2 | Emoji callout | `<blockquote><p>💡 …</p></blockquote>` | `<table class="emoji-blockquote" …>…</table>` |
| 3 | Nested OL alpha | `<li><ol><li>…` | `<li><ol type="a"><li>…` |
| 4 | Table spacing | `…<table>…` | `…<br><table>…<br>` |
| 4 | List spacing | `<li>item</li><li>` | `<li>item<br><br><br></li><li>` |

Full rules, examples, and edge cases: [cbk-transforms.md](references/cbk-transforms.md).

## Configuration Options

| Option | Default | CLI flag | Description |
|--------|---------|----------|-------------|
| Numbered list spacing | ON | `--no-list-spacing` | 3 `<br>` after each non-last first-level `<li>` |
| Border radius on summary | OFF | `--border-radius` | Adds `border-radius:10px;` to section headers |

When converting manually, ask: "Add 3-line spacing after numbered list items? (default: yes)" and "Add rounded corners to section titles? (default: no)".

## Output Format

Return a raw HTML string — no `<html>`/`<body>` wrapper, no code fences. Suitable for pasting directly into Chumbaka LMS editor fields.

## Testing Checklist

- [ ] All top-level `<h3>` wrapped in `<details><summary>`
- [ ] Summary has `padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;`
- [ ] Emoji blockquotes converted to tables with `background-color:#ffe5b4;`
- [ ] Emoji tables have `class="emoji-blockquote"`
- [ ] Nested `<ol>` inside `<li>` have `type="a"`
- [ ] `<br>` present before and after each `<table>`
- [ ] (if enabled) 3 `<br>` at end of each non-last top-level `<li>` in `<ol>`

## Advanced Spacing

For precise element-to-element spacing matching the vanilla web tool, see [advanced-spacing.md](references/advanced-spacing.md).
