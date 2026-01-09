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

Three simple ways to use this project:

1. **Web UI (Static)**: Use the files in `docs/` for static hosting (GitHub Pages, Netlify, or any static host).
2. **Web UI (Local)**: Run the source app locally (requires a React toolchain).
3. **AI Agent Skill**: Use the CBK Markdown Converter skill with AI coding agents to perform conversions directly.

### AI Agent Skill

The **CBK Markdown Converter Skill** (`.github/skills/cbk-markdown-converter/SKILL.md`) enables AI coding assistants like GitHub Copilot to perform markdown-to-HTML conversions directly without needing the web interface.

**When to use**:
- You're working with an AI coding agent
- You need conversions done programmatically within your workflow
- You want to batch convert markdown content
- You're integrating conversions into automated processes

**How to use**:
Simply ask your AI agent: "Convert this markdown to HTML for Chumbaka LMS" and provide your markdown content. The agent will apply all the same transformations (H3 to collapsible sections, emoji blockquotes to styled tables, custom spacing, etc.).

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

This repository includes a minimal Vite project (in `vite-app/`) to make rebuilding the static `docs/` straightforward. Follow these steps when you want to implement changes:

Edit source

1. Open `MarkdownToHTMLApp.jsx` at the repository root and make your changes. The file exports a default React component; keep that contract so the build entry can render it unchanged.

Build using the included Vite project

1. From the repository root, change into the Vite app folder and install dependencies (only required the first time):

```powershell
cd .\vite-app
npm install
```

2. Build the production output:

```powershell
npm run build
# this produces a `dist/` folder inside `vite-app/`
```

3. Replace the tracked `docs/` folder with the new build and back up the existing `docs/` first. From the repository root:

```powershell
$ts = Get-Date -Format yyyyMMddHHmmss
if (Test-Path docs) { Rename-Item docs docs-old-$ts }
Move-Item vite-app/dist docs
```

Preview locally

Serve the updated `docs/` with any static host (for quick preview):

```powershell
npx http-server .\docs -p 8080
# then open http://localhost:8080
```

Commit and push

When you are satisfied with the changes and the updated build, commit and push the relevant source and build files. Example:

```powershell
git add MarkdownToHTMLApp.jsx docs
git commit -m "chore: update converter and rebuild docs"
git push
```

Notes and recommendations

- The Vite config (`vite-app/vite.config.js`) sets `base` to `/cbk-markdown-to-html/` so built asset URLs are correct for GitHub Pages when hosted under that path. If you deploy to a different path, update `base` before building.
- The repository currently tracks `docs/` to make GitHub Pages deployment straightforward. If you prefer to build during CI and avoid tracking built files, add `docs/` to `.gitignore` and update your deployment pipeline.
- Tailwind is not included in the minimal Vite build. If you need exact parity with prior styling, add Tailwind to the Vite project and rebuild.
- I keep backups of replaced `docs/` folders as `docs-old-<timestamp>` when following the above Move-Item step.

## Troubleshooting

- If pasted Markdown does not render as expected, check whether the converter preserves front-matter or special fenced blocks.
- If the LMS strips HTML on import, try embedding the HTML inside an iframe or use the LMS authoring API to create content that accepts HTML.

## Contact

For questions about this repository or integration tips, open an issue in this repository.
