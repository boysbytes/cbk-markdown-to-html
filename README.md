---
title: cbk-markdown-to-html
description: Convert Markdown to HTML for integration with the Chumbaka LMS.
---

## cbk-markdown-to-html

A small web application that converts Markdown to HTML for use with the Chumbaka LMS. The project includes a single-page React app source (`MarkdownToHTMLApp.jsx`) and a pre-built `docs` folder suitable for hosting (for example, GitHub Pages).

### Key files

- `MarkdownToHTMLApp.jsx` — React source for the Markdown → HTML converter.
- `index.html` — App shell used for development or lightweight hosting.
- `docs/` — Built static site (contains `index.html` and assets) you can deploy as a static site.

## Usage

There are two simple ways to use this project:

- Run the source app locally (requires a React toolchain).
- Use the files in `docs/` for static hosting (GitHub Pages, Netlify, or any static host).

### Quick start (static)

1. Serve the `docs/` folder from any static host. For a quick local preview you can use a simple static server. For example, with Node.js installed:

```powershell
npx http-server .\docs -p 8080
# then open http://localhost:8080
```

2. Open the site and paste or edit Markdown in the converter UI — copy the resulting HTML into Chumbaka where required.

## Integration notes

- The app outputs raw HTML. Ensure any receiving system (for example, LMS content fields) sanitises or accepts HTML as required by your security policy.
- If you embed the converter inside an LMS workflow, consider stripping scripts from output or running HTML sanitisation on the server side.

## Development

If you want to modify the React source (`MarkdownToHTMLApp.jsx`) or rebuild the static `docs/` output, use a React build setup compatible with the original `react-colab` starter. A minimal workflow:

1. Create a small React project (for example, using Vite or Create React App).
2. Copy `MarkdownToHTMLApp.jsx` into your `src/` and import it into your app entry point.
3. Build the project and copy the production output into `docs/`.

## Troubleshooting

- If pasted Markdown does not render as expected, check whether the converter preserves front-matter or special fenced blocks.
- If the LMS strips HTML on import, try embedding the HTML inside an iframe or use the LMS authoring API to create content that accepts HTML.

## Contact

For questions about this repository or integration tips, open an issue in this repository.

---
Small, focused project — intended to be easy to host and embed in LMS workflows.


