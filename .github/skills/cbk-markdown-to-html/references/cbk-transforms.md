# CBK Transform Rules

Complete rules, algorithms, and input/output examples for all four Chumbaka LMS transforms.

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

### Advanced Spacing

For precise element-to-element spacing matching the vanilla web tool (40+ element-pair rules), see [advanced-spacing.md](advanced-spacing.md).
