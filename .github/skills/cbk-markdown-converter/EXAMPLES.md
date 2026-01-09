# CBK Markdown Converter Skill - Usage Examples

This document demonstrates how to use the CBK Markdown Converter skill with AI agents.

## Example 1: Simple Collapsible Section

**Input Markdown**:
```markdown
### Step 1 - Getting Started

This is the introduction to the course. Follow along carefully.

Here are some key points:
- First point
- Second point
```

**AI Agent Command**:
"Convert this markdown to HTML for Chumbaka LMS"

**Expected Output**:
```html
<details>
  <summary style="padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;">
    <strong>Step 1 - Getting Started</strong>
  </summary>
  <p>This is the introduction to the course. Follow along carefully.</p>
  <p>Here are some key points:</p>
  <ul>
    <li>First point</li>
    <li>Second point</li>
  </ul>
</details>
```

## Example 2: Emoji Blockquote

**Input Markdown**:
```markdown
> 💡 Remember to save your work frequently to avoid losing progress.
```

**AI Agent Command**:
"Convert this markdown to HTML for Chumbaka LMS"

**Expected Output**:
```html
<br>
<table style="border-style:none;width:560px;background-color:#ffe5b4;" border="0" cellpadding="20">
<tbody><tr>
  <td style="width:70.9062px;vertical-align:middle;">
    <h3 style="font-size:48px;margin:0;"><span style="font-size:48px;">💡</span></h3>
  </td>
  <td style="width:488.094px;vertical-align:middle;">
    <p>Remember to save your work frequently to avoid losing progress.</p>
  </td>
</tr></tbody>
</table>
<br>
```

## Example 3: Combined Features

**Input Markdown**:
```markdown
### Step 2 - Important Concepts

Here are the main ideas:

1. First concept
2. Second concept
3. Third concept

> ⚠️ Warning: Do not skip this section!

### Step 3 - Practice

Try the following exercises.
```

**AI Agent Command**:
"Convert this markdown to HTML for Chumbaka LMS with numbered list spacing enabled"

**Expected Output**:
```html
<details>
  <summary style="padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;">
    <strong>Step 2 - Important Concepts</strong>
  </summary>
  <p>Here are the main ideas:</p>
  <ol>
    <li>First concept<br><br><br></li>
    <li>Second concept<br><br><br></li>
    <li>Third concept</li>
  </ol>
  <br>
  <table style="border-style:none;width:560px;background-color:#ffe5b4;" border="0" cellpadding="20">
  <tbody><tr>
    <td style="width:70.9062px;vertical-align:middle;">
      <h3 style="font-size:48px;margin:0;"><span style="font-size:48px;">⚠️</span></h3>
    </td>
    <td style="width:488.094px;vertical-align:middle;">
      <p>Warning: Do not skip this section!</p>
    </td>
  </tr></tbody>
  </table>
  <br>
</details>
<details>
  <summary style="padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;">
    <strong>Step 3 - Practice</strong>
  </summary>
  <p>Try the following exercises.</p>
</details>
```

## Example 4: Nested Lists

**Input Markdown**:
```markdown
1. Main item one
   a. Sub-item A
   b. Sub-item B
2. Main item two
```

**Expected Output**:
```html
<ol>
  <li>Main item one<br><br><br>
    <ol type="a">
      <li>Sub-item A</li>
      <li>Sub-item B</li>
    </ol>
  </li>
  <li>Main item two</li>
</ol>
```

## Testing the Skill

To test if the skill is working correctly:

1. Ask your AI agent: "Do you have the CBK Markdown Converter skill?"
2. Provide sample markdown and request conversion
3. Verify the output contains:
   - H3 headings wrapped in `<details><summary>`
   - Emoji blockquotes converted to styled tables
   - Nested lists with `type="a"`
   - Appropriate spacing (br tags)

## Common User Requests

**Request**: "Convert my markdown course content to Chumbaka HTML"
- Agent should recognize this needs the CBK skill
- Should ask about spacing preferences

**Request**: "Turn this markdown into LMS-friendly HTML"
- Agent might ask: "Is this for Chumbaka LMS?" or apply standard conversion
- If user mentions Chumbaka, should use CBK skill

**Request**: "Format this for Chumbaka with collapsible sections"
- Clear trigger for CBK skill
- Should convert H3s to details/summary

## Troubleshooting

**Issue**: Emoji not detected
- Verify the emoji is at the start of the blockquote
- Check Unicode range (skill supports most common emojis)

**Issue**: Spacing not applied
- Confirm spacing option is enabled
- Check if it's the last item (no spacing after last item)

**Issue**: H3 not collapsing
- Ensure it's exactly `### ` (three hashes and space)
- Verify subsequent content exists to wrap

**Issue**: Nested lists not alphabetical
- Confirm the list is truly nested (indented under a parent `<li>`)
- Check if `type` attribute was already set to something else
