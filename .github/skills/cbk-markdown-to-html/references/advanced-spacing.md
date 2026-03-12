# Advanced Spacing Rules

Complete spacing configuration matching the vanilla web implementation (`MarkdownToHTMLApp.jsx`). Defines how many `<br>` tags to insert between different element types.

## When to Use This Reference

- User reports spacing inconsistencies with the vanilla web tool
- User explicitly requests "exact vanilla implementation"
- User needs granular control over spacing between specific element pairs
- Debugging spacing in complex nested content

For most use cases, the simplified spacing in SKILL.md (table `<br>` + optional numbered list spacing) is sufficient.

## Default Implementation

The main SKILL covers two spacing rules:

1. **Table spacing**: 1 `<br>` before and after tables
2. **Numbered list spacing**: 3 `<br>` after each non-last first-level `<li>` (optional)

The rules below are only needed for more precise control.

---

## Complete Spacing Configuration

Format: `"current-element_to_next-element": number-of-br-tags`

### Emoji Blockquote Spacing

```javascript
"emoji-blockquote_to_ol-l1": 3,   // Emoji table → Level 1 ordered list
"emoji-blockquote_to_ol-l2": 1,   // Emoji table → Level 2 ordered list
"emoji-blockquote_to_p": 1,       // Emoji table → Paragraph
```

### Numbered List Item Spacing

```javascript
"ol-li-l1_to_ol-li-l1": 3,  // Level 1 → Level 1 (same-level items)
"ol-li-l1_to_ol-li-l2": 1,  // Level 1 → Level 2 (nesting deeper)
"ol-li-l2_to_ol-li-l2": 0,  // Level 2 → Level 2 (between nested items)
"ol-li-l2_to_ol-li-l1": 1,  // Level 2 → Level 1 (returning to parent)
```

### Bulleted List Item Spacing

```javascript
"ul-li-l1_to_ul-li-l1": 1,  // Level 1 → Level 1
"ul-li-l1_to_ul-li-l2": 1,  // Level 1 → Level 2
"ul-li-l2_to_ul-li-l2": 1,  // Level 2 → Level 2
"ul-li-l2_to_ul-li-l1": 1,  // Level 2 → Level 1
```

### Numbered List to Details

```javascript
"ol_to_details": 1,          // Ordered list → Collapsible section
```

### Paragraph Spacing

```javascript
"p_to_image": 1,             // Paragraph → Image
"p_to_details": 1,           // Paragraph → Collapsible section
```

### Image Spacing

```javascript
"image_to_p": 1,             // Image → Paragraph
"image_to_ol": 2,            // Image → Ordered list
"image_to_emoji-blockquote": 2,  // Image → Emoji table
"image_to_table": 2,         // Image → Table
```

### Table Spacing

```javascript
"table_to_ol": 1,            // Table → Ordered list
"table_to_image": 2,         // Table → Image
"table_to_p": 1,             // Table → Paragraph
"table_to_details": 1,       // Table → Collapsible section
```

### End of Bulleted List Spacing

```javascript
"ul_to_ol": 1,               // Bulleted list → Ordered list
"ul_to_image": 1,            // Bulleted list → Image
"ul_to_table": 1,            // Bulleted list → Table
"ul_to_p": 1,                // Bulleted list → Paragraph
"ul_to_details": 1,          // Bulleted list → Collapsible section
"ul_to_emoji-blockquote": 2, // Bulleted list → Emoji table
```

### Details (Collapsible) Spacing

```javascript
"details_trailing": 3,       // <br> appended inside each non-last <details> (before </details>)
"details_last_trailing": 2,  // <br> appended inside the last <details>
```

> **Note:** Spacing is placed **inside** the `<details>` block so it is only visible when a section is
> expanded. No `<br>` tags are inserted between `</details>` and `<details>` tags, which would create
> blank gaps between collapsed section headers.

### Iframe Spacing

```javascript
"iframe_to_image": 1,
"iframe_to_emoji-blockquote": 2,
"iframe_to_table": 2,
"iframe_to_ol-li-l1": 1,
"iframe_to_ol-li-l2": 1,
"iframe_to_ul-li-l1": 1,
"iframe_to_ul-li-l2": 1,
"iframe_to_iframe": 1,
"iframe_to_p": 1,
```

### Default Fallback

```javascript
"default": 1,                // Any unspecified combination: 1 br
```

---

## Implementation Algorithm

```javascript
function applyCustomSpacing(container, config) {
  // 1. Process top-level children
  const children = Array.from(container.children);
  for (let i = 0; i < children.length - 1; i++) {
    const current = children[i];
    const next = children[i + 1];
    const currentType = getElementType(current);
    const nextType = getElementType(next);
    const key = `${currentType}_to_${nextType}`;
    const brCount = config[key] ?? config["default"] ?? 1;

    if (brCount > 0) {
      current.insertAdjacentHTML('afterend', '<br>'.repeat(brCount));
    }
  }

  // 2. Process list spacing (between and within list items)
  const lists = container.querySelectorAll('ol, ul');
  lists.forEach(list => {
    const listItems = Array.from(list.children).filter(c => c.tagName === 'LI');

    // Between list items
    for (let i = 0; i < listItems.length - 1; i++) {
      const currentLi = listItems[i];
      const nextLi = listItems[i + 1];
      const currentLevel = isNestedLi(currentLi) ? 'l2' : 'l1';
      const nextLevel = isNestedLi(nextLi) ? 'l2' : 'l1';
      const key = `${list.tagName.toLowerCase()}-li-${currentLevel}_to_${list.tagName.toLowerCase()}-li-${nextLevel}`;
      const brCount = config[key] ?? config["default"] ?? 1;

      if (brCount > 0) {
        currentLi.insertAdjacentHTML('beforeend', '<br>'.repeat(brCount));
      }
    }

    // Within each list item (between block children)
    listItems.forEach(li => {
      const blockChildren = getBlockChildren(li);
      for (let i = 0; i < blockChildren.length - 1; i++) {
        const current = blockChildren[i];
        const next = blockChildren[i + 1];
        const key = `${getElementType(current)}_to_${getElementType(next)}`;
        const brCount = config[key] ?? config["default"] ?? 1;

        if (brCount > 0) {
          let existingBrs = countBrsBetween(current, next);
          if (existingBrs < brCount) {
            current.insertAdjacentHTML('afterend', '<br>'.repeat(brCount - existingBrs));
          }
        }
      }
    });
  });
}
```

---

## Element Type Detection

The `getElementType` function categorises elements for spacing lookups.

> **Important:** Emoji blockquote tables are identified by `class="emoji-blockquote"`. The
> Python script (`scripts/cbk_markdown_to_html.py`) adds this class automatically. If
> converting via the vanilla web app (`MarkdownToHTMLApp.jsx`), you must add this class
> manually or patch the JSX — the original source does not add it, which means
> `getElementType` cannot distinguish emoji tables from plain markdown tables.

```javascript
function getElementType(element) {
  if (!element || !element.tagName) return 'unknown';

  const tagName = element.tagName.toLowerCase();

  switch (tagName) {
    case 'table':
      // Requires class="emoji-blockquote" to be present on emoji tables
      return element.classList.contains('emoji-blockquote')
        ? 'emoji-blockquote'
        : 'table';

    case 'p':
      // A paragraph containing only an <img> is categorised as 'image'
      if (element.children.length === 1 &&
          element.firstElementChild?.tagName.toLowerCase() === 'img') {
        return 'image';
      }
      return 'p';

    default:
      return tagName; // ol, ul, details, iframe, etc.
  }
}
```

---

## Level Detection for Lists

```javascript
function isNestedLi(li) {
  // Level 2 if the parent list is itself inside a list item
  const parentList = li.closest('ol, ul');
  return parentList?.parentElement?.tagName === 'LI';
}
```

---

## Usage Notes

1. **Order matters**: Apply in this sequence — top-level spacing → inter-list-item spacing → intra-list-item spacing.
2. **Avoid duplicate `<br>` tags**: Check existing `<br>` count before inserting.
3. **Last items**: No spacing after the last item in a container.
4. **Nested context**: List item spacing rules only apply within lists.
5. **Default fallback**: 1 `<br>` for any unspecified element-pair combination.
