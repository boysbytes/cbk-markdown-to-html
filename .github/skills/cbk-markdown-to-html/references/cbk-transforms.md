# CBK Transform Rules

Complete rules, algorithms, and input/output examples for all CBK Chumbaka LMS transforms.

## Pre-processing (before markdown parsing)

Apply these steps to the raw markdown string **before** passing it to the markdown parser.

### Step 0a: Strip YAML front matter

Remove the YAML front matter block (delimited by `---` lines) at the start of the file.

```
Pattern: ^---\s*\n.*?\n---\s*\n  (DOTALL, at start of string)
```

If no front matter is present, the text is unchanged.

### Step 0b: Pre-process fenced code blocks in list items and blockquotes

Python's `markdown.extensions.fenced_code` extension does not reliably handle:
- Fenced code blocks indented inside list items (blank lines inside the block break it).
- Fenced code blocks prefixed with `>` inside blockquotes (parsed as inline code).

**Detection:**
- **List-item block:** Line matches `^( {4,})(```+|~~~+)(\S*)$` (4+ leading spaces).
- **Blockquote block:** Line matches `^(>+ *)(```+|~~~+)(\S*)$` (blockquote prefix).

**Algorithm:**
1. Replace each such fenced block with a unique placeholder token (e.g. `CBKCODE0PLACEHOLDER`) at the same indentation/prefix level.
2. After markdown parsing, replace `<p>TOKEN</p>` (with optional whitespace) with the corresponding `<pre><code class="language-LANG">…</code></pre>` HTML.
3. Strip only the fence-prefix indentation from code lines; preserve relative indentation within the block.
4. Escape `&`, `<`, `>` inside the code block.

### Step 0c: Separate consecutive blockquotes

Some parsers (including Python's `markdown` library) merge two adjacent blockquote blocks into one `<blockquote>` element when they are separated by a blank line. To prevent this, inject an HTML comment between them before parsing.

**Detection:** Two or more groups of consecutive `>` lines where the groups are separated by one or more blank lines.

**Algorithm:**
1. Split the markdown into lines.
2. Track when a `> `-prefixed block ends (a line that starts with `>` followed by a blank line).
3. If the next non-blank line also starts with `>`, insert `<!-- blockquote-break -->` between the two groups.
4. After markdown parsing, remove any `<!-- blockquote-break -->` that may appear in the output.

```
Before:
> Learning objectives line 1
> - item 1

> ⚠️ Board compatibility paragraph

After:
> Learning objectives line 1
> - item 1

<!-- blockquote-break -->

> ⚠️ Board compatibility paragraph
```

### Step 0d: Fix heading + list in blockquotes

Some parsers do not create a `<ul>` out of list markers (`- `) that follow a non-list line inside a blockquote unless there is a blank line between them. This causes both the heading text and the list items to appear in a single merged `<p>` tag.

**Detection:** Inside a blockquote block (consecutive lines starting with `>`), a non-list line is immediately followed by a line starting with `> - ` or `> * ` (with no blank blockquote line between them).

**Algorithm:**
1. Scan each blockquote block line by line.
2. When a non-list `>` line is immediately followed by a `> - ` or `> * ` line, insert an empty blockquote line `>` between them.

```
Before:
> **Learning objectives**
> - Explain what capacitance is...

After:
> **Learning objectives**
>
> - Explain what capacitance is...
```

---

## Transform 1: H3 to Collapsible Sections

Every top-level `<h3>` and all its following siblings (up to the next `<h3>`) become a `<details><summary>` block.

### Algorithm

```
For each direct-child <h3> of the container:
  1. Create <details>
  2. Create <summary> with inline style:
       padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;
       (optionally append border-radius:10px; if user requested)
  3. Wrap all <h3> content in <strong> inside <summary>
  4. Move all consecutive siblings into <details> until the next <h3>
  5. Replace <h3> with the <details> element
```

### Styles

```
summary style (base):    padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;
summary style (optional): border-radius:10px;
```

### Example

Input:

```html
<h3>Step 1 - Getting Started</h3>
<p>Welcome to the tutorial.</p>
<ul><li>First item</li></ul>
<h3>Step 2 - Next Steps</h3>
<p>Continue here.</p>
```

Output:

```html
<details>
  <summary style="padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;">
    <strong>Step 1 - Getting Started</strong>
  </summary>
  <p>Welcome to the tutorial.</p>
  <ul><li>First item</li></ul>
</details>
<details>
  <summary style="padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;">
    <strong>Step 2 - Next Steps</strong>
  </summary>
  <p>Continue here.</p>
</details>
```

### Edge Cases

- **Empty content after H3**: Still wrap in `<details><summary>`. The `<details>` body will be empty.
- **Multiple consecutive H3s**: Each becomes a separate `<details>` — no siblings are collected for each.
- **H3 with inline formatting**: Content is moved verbatim into `<strong>`. Example: `<h3><code>myFunc()</code></h3>` → `<summary><strong><code>myFunc()</code></strong></summary>`.
- **H1/H2 headings**: Not affected. Only `<h3>` triggers this transform.
- **Blockquote or callout table after a list**: If a `<blockquote>` or emoji callout table appears after the list but before the next `<h3>`, it is **inside** the same `<details>` block. Do not stop collecting siblings at the end of a list.

  ```html
  <!-- Input (after markdown parse) -->
  <h3>Step 1</h3>
  <ol>…</ol>
  <blockquote>💡 tip text</blockquote>   ← still belongs to Step 1
  <h3>Step 2</h3>

  <!-- Output -->
  <details>
    <summary>…Step 1…</summary>
    <ol>…</ol>
    <table class="emoji-blockquote">…</table>   ← inside Step 1 <details>
  </details>
  <details>
    <summary>…Step 2…</summary>
    …
  </details>
  ```

---

## Transform 2: Emoji Blockquotes to Styled Tables

A `<blockquote>` whose first child element starts with an emoji becomes a two-column styled table (peach background).

### Detection

Test the first element child's innerHTML against:

```
^([\U0001F300-\U0001FFFF\u231A-\u32FF\u2600-\u27BF\uFE0F\u200D\u20E3]+)\s*
```

If it matches, the blockquote is transformed. Otherwise it is left unchanged.

### Algorithm

```
For each <blockquote>:
  If first element child innerHTML starts with emoji:
    1. Extract emoji characters and remaining inline HTML
    2. Build <table class="emoji-blockquote" …>:
       style: border-style:none;width:560px;background-color:#ffe5b4;
       attributes: border="0" cellpadding="20"
    3. TD 1 (emoji column):
       style: width:70.9062px;vertical-align:middle;
       content: <h3 style="font-size:48px;margin:0;"><span style="font-size:48px;">EMOJI</span></h3>
    4. TD 2 (text column):
       style: width:488.094px;vertical-align:middle;
       content: <p>REMAINING_HTML</p> (if any remaining text)
               + all further element siblings of the first child
    5. Replace <blockquote> with the <table>
```

> **Note:** The `class="emoji-blockquote"` attribute is required for the advanced spacing
> `getElementType` function to distinguish emoji tables from regular markdown tables.
> The vanilla web app (`MarkdownToHTMLApp.jsx`) does not add this class — that is an
> inconsistency fixed here and in the Python script.

### Styles Summary

| Element | Style |
|---------|-------|
| `<table>` | `border-style:none;width:560px;background-color:#ffe5b4;` |
| TD 1 | `width:70.9062px;vertical-align:middle;` |
| TD 2 | `width:488.094px;vertical-align:middle;` |
| `<h3>` inside TD 1 | `font-size:48px;margin:0;` |
| `<span>` inside h3 | `font-size:48px;` |

> **Inconsistency fixed:** The JSX source adds `height:73px` to the table style. This is
> content-dependent and not documented in the original SKILL — it is omitted here.

### Example

Input markdown:

```markdown
> 💡 This is a helpful tip
> - Remember this
> - And this
```

Intermediate HTML (after markdown parse):

```html
<blockquote>
  <p>💡 This is a helpful tip</p>
  <ul><li>Remember this</li><li>And this</li></ul>
</blockquote>
```

Output HTML:

```html
<table class="emoji-blockquote" style="border-style:none;width:560px;background-color:#ffe5b4;" border="0" cellpadding="20">
  <tbody><tr>
    <td style="width:70.9062px;vertical-align:middle;">
      <h3 style="font-size:48px;margin:0;"><span style="font-size:48px;">💡</span></h3>
    </td>
    <td style="width:488.094px;vertical-align:middle;">
      <p>This is a helpful tip</p>
      <ul><li>Remember this</li><li>And this</li></ul>
    </td>
  </tr></tbody>
</table>
```

### Edge Cases

- **No emoji at start**: Blockquote is left as-is.
- **Emoji only, no text**: TD 2 is empty (no `<p>`, no siblings).
- **Multi-emoji sequence**: The entire leading emoji sequence (including ZWJ sequences) is captured as the emoji.
- **Inline formatting in the text** (e.g. `> 💡 **Bold tip**`): Remaining HTML `<strong>Bold tip</strong>` is placed inside `<p>` in TD 2.

### Common Emojis in Blockquotes

| Emoji | Unicode | Typical use |
|-------|---------|-------------|
| 💡 | U+1F4A1 | Tips |
| ⚠️ | U+26A0 | Warnings |
| ℹ️ | U+2139 | Info |
| ✅ | U+2705 | Do this |
| ❌ | U+274C | Don't do this |
| 🎯 | U+1F3AF | Goals |
| 📝 | U+1F4DD | Notes |
| 🔔 | U+1F514 | Reminders |

---

## Transform 2b: Non-Emoji Blockquotes to Bordered Tables

A `<blockquote>` whose content does **not** start with an emoji becomes a single-column white-background bordered table.

### Detection

Test whether Transform 2 (emoji callout) applies. If the blockquote's first child element does **not** start with an emoji character, apply Transform 2b instead.

### Algorithm

```
For each <blockquote> that is NOT an emoji blockquote:
  1. Create <table style="border-collapse: collapse; width: 100%; background-color: #ffffff;"
          border="1" cellpadding="20">
  2. Wrap all content in a single <td style="width: 100%;">
  3. For each child element of the blockquote:
     a. Bold-only paragraph: <p><strong>…</strong></p> or <p><strong>…:</strong></p>
        → render as <p><strong>heading text</strong></p>
           (strip trailing colon from heading text if present)
     b. <ul> or <ol> list:
        → convert to nested structure (see below)
     c. Any other element: include as-is
  4. Replace <blockquote> with the <table>
```

### List Conversion (nested structure)

Each `<ul>` or `<ol>` child of the blockquote becomes a nested list inside the table cell:

```html
<ul>
<li style="list-style-type: none;">
<ul>
<li aria-level="1">First item text</li>
<li aria-level="1">Second item text</li>
</ul>
</li>
</ul>
```

Preserve all inline HTML inside list item text (bold, code, links, math, etc.) without alteration.

### Bold-Only Paragraph Detection

A `<p>` is considered bold-only (treated as a heading) if its entire text content is wrapped in a single `<strong>` element and contains no other block-level children.

Strip a trailing `:` from the text when rendering, so `**Learning objectives:**` and `**Learning objectives**` both become `<p><strong>Learning objectives</strong></p>`.

### Styles Summary

| Element | Style / Attributes |
|---------|-------------------|
| `<table>` | `style="border-collapse: collapse; width: 100%; background-color: #ffffff;"` `border="1"` `cellpadding="20"` |
| `<td>` | `style="width: 100%;"` |

### Example

Input markdown:

```markdown
> **Learning objectives**
> - Explain what capacitance is and how the sensor works.
> - Describe how soil moisture affects a capacitive sensor reading.
> - Calibrate a sensor by recording values for dry and wet conditions.
```

Intermediate HTML (after markdown parse + pre-processing):

```html
<blockquote>
  <p><strong>Learning objectives</strong></p>
  <ul>
    <li>Explain what capacitance is and how the sensor works.</li>
    <li>Describe how soil moisture affects a capacitive sensor reading.</li>
    <li>Calibrate a sensor by recording values for dry and wet conditions.</li>
  </ul>
</blockquote>
```

Output HTML:

```html
<table style="border-collapse: collapse; width: 100%; background-color: #ffffff;" border="1" cellpadding="20">
<tbody>
<tr>
<td style="width: 100%;">
<p><strong>Learning objectives</strong></p>
<ul>
<li style="list-style-type: none;">
<ul>
<li aria-level="1">Explain what capacitance is and how the sensor works.</li>
<li aria-level="1">Describe how soil moisture affects a capacitive sensor reading.</li>
<li aria-level="1">Calibrate a sensor by recording values for dry and wet conditions.</li>
</ul>
</li>
</ul>
</td>
</tr>
</tbody>
</table>
```

### Edge Cases

- **No list, only paragraphs**: All `<p>` children are included as-is. The table still wraps them.
- **Bold heading + regular paragraph**: Bold-only `<p>` becomes heading; remaining `<p>` children are included unchanged.
- **Inline code in list items**: `<code>text</code>` is preserved without alteration.
- **Emoji NOT at the very start**: A blockquote like `> ⚠️ **Warning:**` starts with an emoji and is handled by Transform 2 (emoji callout), not Transform 2b.

---

## Transform 3: Nested List Alphabetical Numbering

Ordered lists that are direct children of `<li>` elements get `type="a"` for alphabetical numbering.

### Algorithm

```
For each <ol> that is a direct child of <li>:
  If type attribute is absent or "1":
    Set type="a"
  Else:
    Preserve existing type attribute
```

### Example

Input:

```html
<ol>
  <li>First item
    <ol>
      <li>Nested item A</li>
      <li>Nested item B</li>
    </ol>
  </li>
</ol>
```

Output:

```html
<ol>
  <li>First item
    <ol type="a">
      <li>Nested item A</li>
      <li>Nested item B</li>
    </ol>
  </li>
</ol>
```

### Edge Cases

- **Existing `type` attribute**: Preserved unless it is `"1"` (numeric), which is replaced with `"a"`.
- **Unordered lists (`<ul>`)**: Not affected — only `<ol>` elements nested inside `<li>` are targeted.
- **Deeper nesting** (3+ levels): Only immediate `<ol>` children of `<li>` are targeted. Third-level nesting is not modified unless itself nested inside another `<li>`.

---

## Transform 4: Custom Spacing

### A. Table Spacing (always applied)

Add one `<br>` before and after each `<table>` element, unless one is already present.

**Before check:** Walk backwards through previous siblings. If a `<br>` is found before any non-empty non-br content, skip. Otherwise insert `<br>`.

**After check:** Count consecutive `<br>` tags immediately after the table. If count < 1, insert one `<br>`.

### B. Numbered List Spacing (optional, default: ON)

Add 3 `<br>` tags at the end of each non-last first-level `<li>` in `<ol>`.

```
For each top-level <ol> (parent is NOT an <li>):
  For each direct <li> child EXCEPT the last:
    Count existing trailing <br> tags in li
    If count < 3: append (3 - count) <br> tags
```

**Example** (1 existing `<br>` → append 2 more):

```html
<!-- Input li -->
<li>First item<br></li>

<!-- Output li -->
<li>First item<br><br><br></li>
```

### C. Sub-List Item Spacing (always applied)

Add 2 `<br>` tags at the end of each non-last `<li>` in nested `<ol>` elements (alphabetical sub-lists created by Transform 3).

```
For each nested <ol> (parent is an <li>):
  For each direct <li> child EXCEPT the last:
    Count existing trailing <br> tags in li
    If count < 2: append (2 - count) <br> tags
```

This applies unconditionally — it is not controlled by a configuration option.

**Example:**

```html
<!-- Input: sub-numbered items a, b, c inside a parent <li> -->
<ol type="a">
  <li><p><strong>STEP 1:</strong></p><p>Do the first thing.</p></li>
  <li><p><strong>STEP 2:</strong></p><p>Do the second thing.</p></li>
  <li><p><strong>STEP 3:</strong></p><p>Do the third thing.</p></li>
</ol>

<!-- Output: 2 <br> appended after each non-last sub-item -->
<ol type="a">
  <li><p><strong>STEP 1:</strong></p><p>Do the first thing.</p><br><br></li>
  <li><p><strong>STEP 2:</strong></p><p>Do the second thing.</p><br><br></li>
  <li><p><strong>STEP 3:</strong></p><p>Do the third thing.</p></li>
</ol>
```

### Advanced Spacing

For precise element-to-element spacing matching the vanilla web tool (40+ element-pair rules), see [advanced-spacing.md](advanced-spacing.md).

### D. Section Trailing Spacing (always applied)

Append 3 `<br>` tags at the end of content inside each **non-last** `<details>` element, and 2 `<br>` at the end of the **last** `<details>` element.  All `<br>` tags go **inside** the `<details>` so they are only visible when a section is expanded, and do not create blank gaps between collapsed section headers.

```
For each <details> that is NOT the last:
  Append <br><br><br> before </details>

For the last <details>:
  Append <br><br> before </details>
```

**Example:**

```html
<!-- Non-last section -->
<details>
  <summary>…Step 1…</summary>
  <ol>…</ol>
  <br><br><br>
</details>
<details>
  <summary>…Step 4 (last)…</summary>
  <ol>…</ol>
  <br><br>
</details>
```
