# cbk-markdown-to-html

> A small client-side app that converts Markdown into HTML formatted for the Chumbaka LMS.

This repository contains a lightweight React-based converter that turns Markdown input into HTML with a few Chumbaka-specific transformations (collapsible sections, styled blockquotes and spacing tweaks).

## Highlights

- Browser-only: no server required for the basic converter.
- Small codebase: the core logic lives in `MarkdownToHTMLApp.jsx`.
- Static build: a ready-to-open build is available in `docs/`.

> [!NOTE]
> A static build is included in `docs/`. Open `docs/index.html` in a browser to try the app without building.

## Quick start

1. Open the app directly

	 - Open `index.html` (development copy) or `docs/index.html` (static build) in your browser.

2. Serve locally (recommended for some browsers)

```powershell
# Serve the current folder on http://localhost:8000 (Python 3)
python -m http.server 8000

# or (Node) using npx http-server
npx http-server -p 8080
```

## How to use

- Paste or type Markdown into the left-hand editor.
- The app converts it to HTML on the fly and shows the result in the right-hand pane for copying.

## How it works (brief)

- Markdown parsing: the app uses the `marked` library to convert Markdown to HTML.
- Custom formatting: after HTML is generated, `formatHtml` (in `MarkdownToHTMLApp.jsx`) applies Chumbaka-specific transforms such as:
	- converting third-level headings (`<h3>`) into collapsible `<details>` sections,
	- transforming blockquotes that include emoji markers into styled table blocks,
	- adding custom line spacing and small structural tweaks to improve LMS rendering.

## Example

Input (Markdown):

```markdown
### Topic: Revision

Some content.

> 📝 Note: Remember to practise.
```

Result (HTML): the converter will create a collapsible section for the H3 and convert the emoji blockquote into a styled note block suitable for the LMS.

## Files of interest

- `MarkdownToHTMLApp.jsx` — main React component and conversion logic (core of the project).
- `index.html` — app entry for development.
- `docs/index.html` — static build you can open directly.

## Suggested next steps

- Add tests for the HTML transforms in `formatHtml` (unit tests that assert expected output for sample markdown).
- Provide a small CLI or Node script to batch-convert Markdown files to the Chumbaka HTML flavour.

## Notes

- This project is intentionally small and aimed at producing LMS-friendly HTML rather than being a full Markdown editor. If you need help adding features or tests, open an issue or a pull request with the changes you want.

---

Source / inspiration: the UI and conversion logic are implemented in `MarkdownToHTMLApp.jsx`.


