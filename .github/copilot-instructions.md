## AI Coding Agent Guide

Use this to get productive quickly on this repo. Keep changes minimal, static-host friendly, and aligned with the existing patterns.

### Big picture
- Purpose: Convert Markdown to HTML for Chumbaka LMS authoring and embedding.
- Two UIs exist:
	- `index.html`: standalone, no build; uses CDN `marked` and custom DOM transforms.
	- React app: `MarkdownToHTMLApp.jsx`; prebuilt output lives in `docs/` (Vite build), served as static site.
- No Node toolchain is committed here (no package.json). React builds happen outside this repo and the output is copied into `docs/`.

### Source layout
- `index.html`: vanilla app with inline CSS/JS; key functions: `convertMarkdown`, `processCustomMarkdown`, `createCollapsibleSections`, `processBlockquotes`, `applyCustomSpacing`, `getElementType` and UI utilities.
- `MarkdownToHTMLApp.jsx`: React component exporting the same converter behaviors via `formatHtml(...)` with options (spacing for numbered lists; optional rounded summary corners).
- `docs/`: Vite-generated static site for hosting (GitHub Pages). Entry is `docs/index.html` mounting React at the element with id 'root' and loading assets under /cbk-markdown-to-html/.

### Core transforms and spacing rules
- H3 to collapsible sections: Consecutive content after each <h3> is wrapped in <details><summary>...</summary> ...</details>. Summary style uses background color f9f7f0 and padding; border radius is optional in React (prop flag).
- Emoji blockquotes: A blockquote whose first paragraph starts with an emoji becomes a peach table block. In vanilla: a table element with class emoji-blockquote and inline background-color ffe5b4, with CSS in index.html. In React: inline widths/height and cellpadding=20 for consistent layout.
- Spacing: Implemented with explicit `<br>` insertions.
	- Vanilla: global `spacingConfig` controls element-to-element spacing (e.g., list-to-list, image-to-paragraph). Applied by `applyCustomSpacing` across top-level and nested list content.
	- React: `addLineSpacing('table')` and optional 3-line spacing after first-level ordered list items.
- Clipboard: Uses `navigator.clipboard` with `execCommand` fallback; keep both paths.

### Development and running
- Quick preview (no build): open `index.html` in a browser, or serve the folder statically.
- Preview prod build: serve `docs/` statically. Example PowerShell: `npx http-server .\docs -p 8080`; open http://localhost:8080.
- React development: create a separate Vite/CRA project locally, import `MarkdownToHTMLApp.jsx`, build, then copy the build output back into `docs/` (respecting base path `/cbk-markdown-to-html/`).

### When to edit what
- Minor UI/spacing/transform tweaks for the standalone tool: edit `index.html` JS/CSS. Mirror meaningful transform changes in `MarkdownToHTMLApp.jsx` to keep parity.
- React-only UX (shadcn-style button, options toggles): edit `MarkdownToHTMLApp.jsx`; regenerate external build and update `docs/`.
- Do not add a package.json or introduce a bundler here unless requested; this repo intentionally commits only the source component and the built site.

### Conventions and cautions
- Keep transforms idempotent and DOM-based after `marked.parse()`. Avoid introducing script injection in generated HTML.
- For new spacing cases, update `getElementType` and `spacingConfig` (vanilla) or extend targeted spacing in React; prefer `<br>` insertion over CSS margins to match LMS behavior.
- GitHub Pages pathing: `docs/index.html` references assets under `/cbk-markdown-to-html/`. Preserve that base when rebuilding.

### References
- Writing: `.github/instructions/writing.instructions.md`
- Markdown rules: `.github/instructions/markdown.instructions.md`
- Design system: `.github/instructions/design_system.md`
- Project overview: `README.md`

