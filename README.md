## cbk-markdown-to-html
Convert authoring Markdown into LMS‑ready HTML with Chumbaka‑specific transforms.

A lightweight converter that can run in three different ways:

1. **AI Skill** – the preferred interface for GitHub Copilot and other AI coding assistants. Feed your markdown to the skill and receive polished HTML back.
2. **Programmatic script** – a small Python helper for CI pipelines or batch jobs (see `scripts/cbk_markdown_to_html.py`).
3. **Web UI** – a static site you can host or run locally when you need a quick manual editor.

> **Primary focus:** the AI skill. The web application exists for convenience and will eventually be deprecated.

---

## Using the AI Skill (GitHub Copilot)

The skill is defined in `.github/skills/cbk-markdown-converter/SKILL.md` and is automatically available to Copilot and other OpenAI‑based coding agents when the repository is in context.

> [!note]
> The AI skill is **triggered** by natural language requests. No CLI or build step is required.

### Typical requests

```text
Format this Markdown for the Chumbaka LMS.:
```

The agent will strip YAML front matter, run all transforms, and return raw HTML suitable for pasting into the LMS editor.

## Programmatic use (Python script)

There is a tiny helper script in `scripts/cbk_markdown_to_html.py` that exposes the same logic used by the skill.

```bash
pip install markdown beautifulsoup4

# convert a file (output defaults to input.md → input.html)
python scripts/cbk_markdown_to_html.py input.md

# custom output path
python scripts/cbk_markdown_to_html.py input.md output.html

# disable list spacing or enable rounded headers
python scripts/cbk_markdown_to_html.py input.md --no-list-spacing --border-radius
```

You can also import the converter in other Python code:

```python
from cbk_markdown_to_html import convert
html = convert(markdown_text)
```

> [!tip]
> This mode is handy for automation, linting, or CI pipelines where an AI agent isn't available.

## Web interface

A static UI lives in the `docs/` folder and its source component is `MarkdownToHTMLApp.jsx` at the repo root.

### Quick start

```powershell
npx http-server .\docs -p 8080
# visit http://localhost:8080
```

Paste Markdown into the editor and copy resulting HTML. This is useful for manual editing and previewing the rules in action.

> [!warning]
> The web UI is secondary and planned for eventual removal. Prefer the AI skill for long‑term workflows.

## Repository layout

```
.
├── index.html             # lightweight shell for standalone use
├── MarkdownToHTMLApp.jsx # React component used by the web UI
├── docs/                  # prebuilt static site (also deployed to GitHub Pages)
├── examples-for-test/     # sample markdown and generated HTML
├── scripts/               # utility scripts (including Python converter)
├── vite-app/              # minimal Vite project used to rebuild docs/
└── .github/skills/        # Copilot skill definitions
```



