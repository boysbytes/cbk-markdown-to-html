---
name: syntax-highlighter
description: "Offline syntax highlighting for Python, Arduino, C++, and Markdown using Pygments. Use for: (1) standalone code snippets to highlight individually; (2) Markdown files that are NOT being processed by cbk-markdown-to-html. Do NOT use for Chumbaka LMS lesson files — the cbk-markdown-to-html skill applies syntax highlighting automatically during conversion. Output is self-contained inline CSS, suitable for pasting into any HTML or Markdown context. Defaults to Pygments 'default' style with a left-rule border."
license: Complete terms in LICENSE.txt
---

## Overview

Use this skill to highlight code snippets or Markdown fenced blocks entirely offline using Pygments. Output has inline styles — no external stylesheet required.

### When to use this skill

| Situation | Use this skill? |
|-----------|----------------|
| Highlight a **standalone snippet** (paste result into HTML or Markdown) | Yes — `offline_highlight.py` |
| Highlight fenced blocks in a **non-LMS Markdown file** (e.g. README, docs) | Yes — `highlight_markdown.py` |
| Convert a **Chumbaka LMS lesson** (`.md` → `.html`) | **No** — use `cbk-markdown-to-html`; highlighting is automatic |
| Add highlighting to an **already-generated `.html` file** | **No** — re-run `cbk_markdown_to_html.py` on the source `.md` instead |

### Style defaults

- Languages: Python, Arduino (falls back to C++), Markdown. Use `--all-languages` for any Pygments-supported language.
- Style: Pygments `default`.
- CSS: No borders except a left rule; compact padding:
  - border: solid gray
  - border-width: 0em 0em 0em 0.8em
  - padding: 0.2em 0.6em
  - font-size: 12pt (applied on `<pre>`)

## Quick start

1. Install dependency (Pygments).
2. Use the offline scripts to highlight either standalone snippets or fenced blocks inside Markdown.

### Install dependency (once per repo)

```bash
python -m pip install -r .github/skills/syntax-highlighter/requirements.txt
```

### Offline helpers

Use `scripts/offline_highlight.py` for single snippets and `scripts/highlight_markdown.py` for Markdown files.

```bash
# Example: highlight Python from stdin (HTML out)
python .github/skills/syntax-highlighter/scripts/offline_highlight.py --lexer python <<'PY'
print('hello world!')
PY

# Example: highlight Arduino from a file (HTML out)
python .github/skills/syntax-highlighter/scripts/offline_highlight.py --lexer arduino --input sketch.ino > sketch.html

# Example: process a Markdown file in-place, replacing code fences with HTML blocks
python .github/skills/syntax-highlighter/scripts/highlight_markdown.py --in-place --input README.md

# Or write to stdout (non-destructive)
python .github/skills/syntax-highlighter/scripts/highlight_markdown.py --input README.md > README.with-html.md
```

### Parameters

- Supported lexer names
  - Python: `python`
  - Arduino: `arduino` (falls back to `cpp` if unavailable)
  - Markdown: `markdown` (alias `md` also works)
- Style: `default`
- Wrapper CSS (`divstyles`):

```
border:solid gray;border-width:.0em .0em .0em .8em;padding:.2em .6em;
```

### Markdown processing details

- Recognises triple backticks ``` and tildes ~~~ fences.
- Highlights only labelled fences by default where the language is one of: `python`, `arduino`, `markdown` (add `--all-languages` to highlight any labelled fence).
- Unlabelled fences are left unchanged.
- Output remains Markdown with embedded HTML blocks (compatible with most renderers). If your platform sanitises HTML, render server-side or use a trusted renderer.

## Troubleshooting

- Arduino not recognised: falls back to `cpp` automatically.
- Markdown fenced as ```markdown is highlighted as Markdown code, not rendered as rich HTML. If you need full Markdown rendering, run a Markdown renderer first, and then highlight code blocks in its HTML output.
- Different look: ensure `--style default` and the exact `--divstyles` value above (these are the defaults).

## Notes

- No servers or network calls are required.
- No external CSS is required because the formatter uses inline styles.
