# Project Guidelines

## Architecture & Focus
- **Purpose**: Convert Markdown to HTML for Chumbaka LMS authoring and embedding.
- **Primary Tool**: The AI skill (`.github/skills/cbk-markdown-converter/SKILL.md`) is the primary interface for performing conversions directly via AI agents.
- **Web UI**: Two UIs exist for manual editing:
  - `index.html`: A standalone vanilla app without build steps.
  - `vite-app/`: A Vite-powered React project (using `MarkdownToHTMLApp.jsx`) that builds the static site.
- **Static Output**: The prebuilt Vite output is stored in the `docs/` folder, which is served via GitHub Pages at `/cbk-markdown-to-html/`.

## Build and Test
- **Web UI Development**:
  ```powershell
  cd vite-app
  npm install
  npm run dev
  ```
- **Web UI Production Build**:
  ```powershell
  cd vite-app
  npm run build
  # After building, copy the contents of vite-app/dist/ into docs/ to update the GitHub Pages site.
  ```
- **Local Preview**:
  ```powershell
  npx http-server .\docs -p 8080
  ```

## Conventions
- **Idempotency**: Keep custom Markdown transforms idempotent and DOM-based after `marked.parse()`.
- **Spacing**: Use explicit `<br>` insertions rather than CSS margins to match LMS behavior. 
- **Core Transforms**:
  - H3 headers become collapsible `<details><summary>` blocks (padding and optional border radius).
  - Blockquotes starting with an emoji become peach-colored table blocks.
- **Static First**: Avoid introducing script injections in generated HTML. Ensure LMS safety.
- **Parity**: When editing transforms or spacing in `vite-app/src/MarkdownToHTMLApp.jsx`, mirror the changes in the standalone `index.html` to keep feature parity.

## References
- **Skill Definition**: `.github/skills/cbk-markdown-converter/SKILL.md`
- **Writing Docs**: `.github/instructions/writing.instructions.md`
- **Markdown Rules**: `.github/instructions/markdown.instructions.md`
- **Project Overview**: `README.md`

