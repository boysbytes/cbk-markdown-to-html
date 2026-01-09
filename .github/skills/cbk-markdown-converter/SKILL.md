---
name: cbk-markdown-converter
description: Convert Markdown to HTML for Chumbaka LMS with custom transforms - H3 to collapsible sections, emoji blockquotes to styled tables, nested list formatting, and custom spacing rules. Use when users need to convert markdown content for LMS authoring or request Chumbaka-specific HTML formatting.
---

# CBK Markdown to HTML Converter

Converts Markdown to HTML with Chumbaka LMS-specific transformations. This skill replicates the logic from the cbk-markdown-to-html project.

## When to Use

- User requests conversion of Markdown to HTML for Chumbaka LMS
- User mentions "Chumbaka", "LMS authoring", or "markdown to HTML with custom transforms"
- User needs H3 headings converted to collapsible sections
- User needs emoji blockquotes converted to styled tables
- User requests custom spacing in HTML output

## Quick Start

1. Parse user's markdown with standard markdown parser
2. Apply transforms in order: H3→collapsible, emoji blockquotes, nested lists, spacing
3. Return formatted HTML

## Core Transformations

### 1. H3 to Collapsible Sections

**Pattern**: Every `<h3>` becomes a `<details>` with `<summary>`.

**Algorithm**:
```
For each <h3>:
  - Create <details> element
  - Create <summary> with:
    - Style: padding:15px; margin-bottom:25px; cursor:pointer; background:#f9f7f0;
    - Optional: border-radius:10px; (ask user preference)
    - Content: <strong>[H3 content]</strong>
  - Move all consecutive siblings until next <h3> into <details>
  - Replace <h3> with <details>
```

**Example**:
```html
<!-- Input -->
<h3>Step 1 - Getting Started</h3>
<p>Welcome to the tutorial.</p>
<ul><li>First item</li></ul>

<!-- Output -->
<details>
  <summary style="padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;">
    <strong>Step 1 - Getting Started</strong>
  </summary>
  <p>Welcome to the tutorial.</p>
  <ul><li>First item</li></ul>
</details>
```

### 2. Emoji Blockquotes to Styled Tables

**Pattern**: A `<blockquote>` starting with an emoji becomes a styled table (peach background #ffe5b4).

**Detection**: First child's innerHTML starts with emoji regex: `^([\u231A-\u32FF\uD83C-\uDBFF\uDC00-\uDFFF\u2600-\u27BF\uFE0F\u200D]+)\s*`

**Algorithm**:
```
For each <blockquote>:
  If first paragraph starts with emoji:
    - Extract emoji and remaining text
    - Create table with:
      - Style: border-style:none; width:560px; background-color:#ffe5b4;
      - border="0" cellpadding="20"
    - First TD: emoji in <h3> with font-size:48px; margin:0;
      - TD style: width:70.9062px; vertical-align:middle;
    - Second TD: remaining text + all other blockquote children
      - TD style: width:488.094px; vertical-align:middle;
    - Replace blockquote with table
```

**Example**:
```html
<!-- Input -->
<blockquote>
<p>💡 This is a helpful tip</p>
<ul><li>Remember this</li></ul>
</blockquote>

<!-- Output -->
<table style="border-style:none;width:560px;background-color:#ffe5b4;" border="0" cellpadding="20">
<tbody><tr>
  <td style="width:70.9062px;vertical-align:middle;">
    <h3 style="font-size:48px;margin:0;"><span style="font-size:48px;">💡</span></h3>
  </td>
  <td style="width:488.094px;vertical-align:middle;">
    <p>This is a helpful tip</p>
    <ul><li>Remember this</li></ul>
  </td>
</tr></tbody>
</table>
```

### 3. Nested List Formatting

**Pattern**: Nested ordered lists use alphabetical numbering.

**Algorithm**:
```
For each <ol> inside an <li>:
  Set type="a" (unless already has type attribute other than "1")
```

**Example**:
```html
<!-- Input -->
<ol>
  <li>First item
    <ol>
      <li>Nested item</li>
    </ol>
  </li>
</ol>

<!-- Output -->
<ol>
  <li>First item
    <ol type="a">
      <li>Nested item</li>
    </ol>
  </li>
</ol>
```

### 4. Custom Spacing

Two spacing rules apply:

#### A. Table Spacing (Always Applied)
Add `<br>` before and after each `<table>` element unless already present.

#### B. Numbered List Spacing (Optional, Default: ON)
Add 3 `<br>` tags at the end of each first-level `<li>` in `<ol>` (except the last item).

**Algorithm**:
```
For each <ol>:
  For each direct child <li>:
    If li has nextSibling:
      Count existing <br> tags at end of li
      If count < 3:
        Append (3 - count) <br> tags to li
```

**Ask user**: "Enable 3-line spacing after numbered list items? (default: yes)"

#### Advanced Spacing Rules

For precise element-to-element spacing control (rarely needed), see [references/advanced-spacing.md](references/advanced-spacing.md). The vanilla implementation uses a detailed spacing configuration that defines exact `<br>` counts between 40+ element type combinations.

**When to use advanced spacing**:
- User reports spacing inconsistencies with vanilla tool
- User explicitly requests "exact vanilla implementation"
- Complex nested content with specific spacing requirements

For most use cases, the simple table + numbered list spacing above is sufficient.

## Implementation Steps

1. **Parse markdown**: Use standard markdown parser (marked.js equivalent)

2. **Parse HTML**: Create DOM from parsed HTML string

3. **Transform H3s**:
   - Iterate direct children
   - When H3 found, create details/summary
   - Move consecutive siblings into details
   - Replace H3 with details

4. **Transform emoji blockquotes**:
   - Query all blockquotes
   - Test first child for emoji
   - Create table structure
   - Replace blockquote with table

5. **Fix nested lists**:
   - Query `li > ol`
   - Set `type="a"`

6. **Apply spacing**:
   - Add br around tables
   - Optionally add 3 br at end of top-level li elements

7. **Return HTML**: Serialize DOM back to HTML string

## Edge Cases

- **Empty content after H3**: Still wrap in details/summary
- **Multiple consecutive H3s**: Each becomes separate details
- **No emoji in blockquote**: Leave blockquote unchanged
- **Existing type attribute on nested ol**: Preserve if not "1"
- **Last list item**: No spacing added after it
- **Already sufficient br tags**: Don't add more

## Output Format

Return clean HTML string suitable for pasting into Chumbaka LMS editor. No code block wrapper unless user requests it.

## Example Workflow

**User**: "Convert this markdown to HTML for Chumbaka:

```markdown
### Step 1 - Introduction
Welcome to the course.

> 💡 Remember to save your work regularly.
```
"

**Agent Response**:

```html
<details>
  <summary style="padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;">
    <strong>Step 1 - Introduction</strong>
  </summary>
  <p>Welcome to the course.</p>
</details>
<br>
<table style="border-style:none;width:560px;background-color:#ffe5b4;" border="0" cellpadding="20">
<tbody><tr>
  <td style="width:70.9062px;vertical-align:middle;">
    <h3 style="font-size:48px;margin:0;"><span style="font-size:48px;">💡</span></h3>
  </td>
  <td style="width:488.094px;vertical-align:middle;">
    <p>Remember to save your work regularly.</p>
  </td>
</tr></tbody>
</table>
<br>
```

## Configuration Options

### Border Radius on Summary
- **Default**: No border-radius
- **Option**: Add `border-radius:10px;` to summary style
- **Ask**: "Add rounded corners to collapsible sections?"

### Numbered List Spacing
- **Default**: Enabled (3 line breaks after each item)
- **Option**: Disable spacing
- **Ask**: "Add extra spacing after numbered list items?"

## Testing Your Output

Verify these elements in the output:
- [ ] All H3 headings are wrapped in details/summary
- [ ] Summary has correct inline styles (background #f9f7f0)
- [ ] Emoji blockquotes are converted to tables
- [ ] Tables have peach background (#ffe5b4)
- [ ] Nested ordered lists use type="a"
- [ ] Spacing br tags are present around tables
- [ ] (If enabled) 3 br tags after each numbered list item

## Common Emojis in Blockquotes

These commonly trigger the emoji blockquote transform:
- 💡 (lightbulb - tips)
- ⚠️ (warning)
- ℹ️ (info)
- ✅ (checkmark)
- ❌ (cross)
- 🎯 (target)
- 📝 (memo)
- 🔔 (bell)

## Known Limitations

- Fixed table width (560px) - not responsive
- Inline styles only (no CSS classes)
- Emoji detection limited to specific Unicode ranges
- No support for custom emoji graphics (only Unicode emojis)