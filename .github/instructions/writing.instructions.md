---
description: 'Writing style guidelines for creating clear, concise, and user-friendly documentation.'
applyTo: '**/*.md'
---

# Documentation Writing Instructions

These are our documentation writing style guidelines.

## Content conventions and patterns
- Use British English spelling.
- Use inclusive, respectful language.
- Create content that is accurate, relevant, easy to understand, and accessible (easy to retrieve).

## General Style tips
- Get to the point fast.
- Talk like a person.
- Simpler is better.
- Be brief. Give customers just enough information to make decisions confidently. Prune every excess word.

## Grammar
- Use present tense verbs (is, open) instead of past tense (was, opened).
- Write factual statements and direct commands. Avoid hypotheticals like "could" or "would".
- Use active voice where the subject performs the action.
- Write in second person (you) to speak directly to readers.
- Use gender-neutral language.
- Avoid multiple -ing words that can create ambiguity.
- Keep prepositional phrases simple and clear.
- Place modifiers close to what they modify.

## Numbers
- Spell out numbers for zero through nine, unless space is limited. Use numerals for 10 and above.
- Spell out numbers at the beginning of a sentence.
- Spell out ordinal numbers such as first, second, and third. Don't add -ly to form adverbs from ordinal numbers.

## Punctuation
- Use short, simple sentences.
- End all sentences with a period.
- Use one space after punctuation marks.
- After a colon, capitalize only proper nouns.
- Avoid semicolons - use separate sentences instead.
- Use question marks sparingly.
- Don't use slashes (/) - use "or" instead.
- Prefer single over double quotes, avoiding typographic quotes.
- Only use apostrophe (U+0027) and quotes (U+0022), not left or right single or double quotation marks.

## Text formatting

- UI elements, like menu items, dialog names, and names of text boxes, should be in bold text.
- Use code style for:
    - Code elements, like method names, property names, and language keywords.
    - SQL commands.
    - NuGet package names.
    - Command-line commands.
    - Database table and column names.
    - Resource names (like virtual machine names) that shouldn't be localized.
    - URLs that you don't want to be selectable.
- For code placeholders, if you want users to replace part of an input string with their own values, use angle brackets (less than < and greater than > characters) on that placeholder text.

## Links

- Links to other documentation articles should be relative, not absolute. Include the `.md` suffix.
- Links to bookmarks within the same article should be relative and start with `#`.
- Link descriptions should be descriptive and make sense on their own. Don't use "click here" or "this link" or "here".

## Images
- Use images only when they add value.
- Images have a descriptive and meaningful alt text that starts with "Screenshot showing" and ends with ".".
- Videos have a descriptive and meaningful alt text or title that starts with "Video showing" and ends with ".".

## Lists
- Use numbered lists for steps in a procedure.
- Keep list items parallel in structure.

## Numbered steps
- Write complete sentences with capitalization and periods
- Use imperative verbs
- Clearly indicate where actions take place (UI location)
- For single steps, use a bullet instead of a number
- Use angle brackets for menu sequences (File > Open)

## Terminology
- Use "Select" instead of "Click" for UI elements like buttons, menu items, links, dropdowns, and checkboxes.
- Use "might" instead of "may" for conditional statements.
- Avoid latin abbreviations like "e.g.". Use "for example" instead.
- Use the verb "to enable" instead "to allow" unless you're referring to permissions.
- Follow the terms and capitalization guidelines in #microsoft-docs-mcp