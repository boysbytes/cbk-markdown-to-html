# Advanced Spacing Rules

This document contains the complete spacing configuration used by the vanilla implementation (`index.html`). These rules define how many `<br>` tags to insert between different element types.

## When to Use This Reference

- User requests exact parity with vanilla implementation spacing
- User mentions specific element-to-element spacing issues
- User needs granular control over spacing between different HTML elements

## Default Implementation

The main SKILL.md describes two simpler spacing rules:
1. **Table spacing**: 1 br before and after tables
2. **Numbered list spacing**: 3 br after each first-level numbered list item (optional)

This is sufficient for most use cases. Use the rules below only when more precise spacing control is needed.

## Complete Spacing Configuration

Format: `"element-type_to_next-element-type": number-of-br-tags`

### Emoji Blockquote Spacing

```javascript
"emoji-blockquote_to_ol-l1": 3,     // Emoji table → Level 1 ordered list
"emoji-blockquote_to_ol-l2": 1,     // Emoji table → Level 2 ordered list
"emoji-blockquote_to_p": 1,         // Emoji table → Paragraph
```

### Numbered List Item Spacing

```javascript
// Level 1 to Level 1: 3 line breaks between same-level items
"ol-li-l1_to_ol-li-l1": 3,

// Level 1 to Level 2: 1 line break when nesting deeper
"ol-li-l1_to_ol-li-l2": 1,

// Level 2 to Level 2: 0 line breaks between nested items
"ol-li-l2_to_ol-li-l2": 0,

// Level 2 to Level 1: 1 line break when returning to parent level
"ol-li-l2_to_ol-li-l1": 1,
```

### Bulleted List Item Spacing

```javascript
"ul-li-l1_to_ul-li-l1": 1,          // Level 1 → Level 1
"ul-li-l1_to_ul-li-l2": 1,          // Level 1 → Level 2
"ul-li-l2_to_ul-li-l2": 1,          // Level 2 → Level 2
"ul-li-l2_to_ul-li-l1": 1,          // Level 2 → Level 1
```

### Numbered List to Details

```javascript
"ol_to_details": 1,                 // Ordered list → Collapsible section
```

### Paragraph Spacing

```javascript
"p_to_image": 1,                    // Paragraph → Image
"p_to_details": 1,                  // Paragraph → Collapsible section
```

### Image Spacing

```javascript
"image_to_p": 1,                    // Image → Paragraph
"image_to_ol": 2,                   // Image → Ordered list
"image_to_emoji-blockquote": 2,     // Image → Emoji table
"image_to_table": 2,                // Image → Table
```

### Table Spacing

```javascript
"table_to_ol": 1,                   // Table → Ordered list
"table_to_image": 2,                // Table → Image
"table_to_p": 1,                    // Table → Paragraph
"table_to_details": 1,              // Table → Collapsible section
```

### End of Bulleted List Spacing

```javascript
"ul_to_ol": 1,                      // Bulleted list → Ordered list
"ul_to_image": 1,                   // Bulleted list → Image
"ul_to_table": 1,                   // Bulleted list → Table
"ul_to_p": 1,                       // Bulleted list → Paragraph
"ul_to_details": 1,                 // Bulleted list → Collapsible section
"ul_to_emoji-blockquote": 2,        // Bulleted list → Emoji table
```

### Details (Collapsible) Spacing

```javascript
"details_to_details": 1,            // Collapsible → Collapsible
```

### Iframe Spacing

```javascript
"iframe_to_image": 1,               // Iframe → Image
"iframe_to_emoji-blockquote": 2,    // Iframe → Emoji table
"iframe_to_table": 2,               // Iframe → Table
"iframe_to_ol-li-l1": 1,           // Iframe → Level 1 list item
"iframe_to_ol-li-l2": 1,           // Iframe → Level 2 list item
"iframe_to_ul-li-l1": 1,           // Iframe → Level 1 bullet item
"iframe_to_ul-li-l2": 1,           // Iframe → Level 2 bullet item
"iframe_to_iframe": 1,             // Iframe → Iframe
"iframe_to_p": 1,                  // Iframe → Paragraph
```

### Default Fallback

```javascript
"default": 1,                       // Any unspecified combination: 1 br
```

## Implementation Algorithm

```javascript
function applyCustomSpacing(container, config) {
  // 1. Process top-level children
  const children = Array.from(container.children);
  for (let i = 0; i < children.length - 1; i++) {
    const current = children[i];
    const next = children[i+1];
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
          // Check existing br count between elements
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

## Element Type Detection

The `getElementType` function categorizes elements:

```javascript
function getElementType(element) {
  if (!element || !element.tagName) return 'unknown';
  
  const tagName = element.tagName.toLowerCase();
  
  switch (tagName) {
    case 'table':
      // Distinguish emoji blockquote tables from regular tables
      return element.classList.contains('emoji-blockquote') 
        ? 'emoji-blockquote' 
        : 'table';
    
    case 'p':
      // Paragraph containing only an image is categorized as 'image'
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

## Level Detection for Lists

List items are categorized as level 1 (l1) or level 2 (l2):

```javascript
function isNestedLi(li) {
  // Check if the parent list is inside another list item
  const parentList = li.closest('ol, ul');
  return parentList?.parentElement?.tagName === 'LI';
}
```

## Usage Notes

1. **Order matters**: Apply spacing rules in this order:
   - Top-level element spacing
   - Inter-list-item spacing
   - Intra-list-item spacing

2. **Avoid duplicate br tags**: Check for existing `<br>` tags before inserting more.

3. **Last items**: Don't add spacing after the last item in a container.

4. **Nested context**: List item spacing rules only apply within lists.

5. **Default fallback**: If no specific rule exists, use 1 br tag.

## When NOT to Use These Rules

For most Chumbaka LMS use cases, the simplified spacing in SKILL.md (table spacing + optional numbered list spacing) is sufficient. Use these detailed rules only when:

- User reports spacing inconsistencies with the vanilla tool
- User explicitly requests "exact vanilla implementation"
- User needs specific control over element-to-element spacing
- Debugging spacing issues in complex nested content
