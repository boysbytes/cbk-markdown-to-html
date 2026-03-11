---
description: 'Documentation and content creation standards'
applyTo: '**/*.md'
---

## Markdown Content Rules

The following markdown content rules are enforced in the validators:

1. **Headings**: Use appropriate heading levels (H2, H3, etc.) to structure your content. Do not use an H1 heading, as this will be generated based on the title.
2. **Lists**: Use bullet points or numbered lists for lists. Ensure proper indentation and spacing.
3. **Code Blocks**: Use fenced code blocks for code snippets. Specify the language for syntax highlighting.
4. **Links**: Use proper markdown syntax for links. Ensure that links are valid and accessible.
5. **Images**: Use proper markdown syntax for images. Include alt text for accessibility.
6. **Tables**: Use markdown tables for tabular data. Ensure proper formatting and alignment.
7. **Line Length**: Limit line length to 400 characters for readability.
8. **Whitespace**: Use appropriate whitespace to separate sections and improve readability.
9. **Front Matter**: Include YAML front matter at the beginning of every file with all required metadata fields as defined below.

## Front Matter

Every Markdown file must begin with a YAML front matter block. Three fields are always required; all other fields are optional and vary by use case.

### Required fields

| Field | Type | Description |
|---|---|---|
| `title` | string | Full descriptive title of the document, in quotes. |
| `description` | string | One-sentence summary of the document's content or learning goal. |
| `target_audience` | string | Intended audience (e.g. `"13-17 year old students"`, `"Students (13–17)"`). |

### Optional fields

Include only the fields relevant to the document. Common examples:

| Field | Type | Description |
|---|---|---|
| `purpose` | string | High-level purpose. Use `lesson`, `reference`, `guide`, or `template`. |
| `project` | string | Project identifier (e.g. `A`, `B`, `C`). |
| `lesson_id` | string | Unique lesson identifier (e.g. `C1`, `A3`). |
| `type` | string | Document type. Use `Class`, `Lab`, `Slide`, `Notes`, or `Other`. |
| `version` | string | Semantic version string (e.g. `v1.0`). |
| `last_updated` | date | Date of last update in `YYYY-MM-DD` format. |
| `lesson` | integer | Lesson number within a sequence. |
| `duration` | integer | Estimated duration in minutes. |
| `tags` | list | List of relevant topic tags. |
| `lesson_reference` | string | Filename of a related lesson document. |

### Examples

Standalone lesson note:

```yaml
---
title: "Define Data-Driven Problems"
description: "Turn your Design Thinking problem into a measurable data science question, identify needed data, and decide if machine learning fits."
target_audience: "Students (13–17)"
last_updated: 2025-12-30
lesson: 3
tags: ["data-driven", "define", "problem-formulation"]
---
```

Webinar session:

```yaml
---
title: "From Human Problems to Data-Driven Solutions"
description: "Interactive webinar teaching participants how to translate Design Thinking problems into measurable data science questions."
target_audience: "Students (13–17)"
duration: 60
lesson_reference: "03-dt-proto-defining-data-driven-problems.md"
---
```

Class or Lab lesson file:

```yaml
---
title: "C1 Class - Text Patterns and n-gram Models"
description: "Introduction to text prediction through pattern recognition and frequency analysis."
target_audience: "13-17 year old students"
purpose: "lesson"
project: "C"
lesson_id: "C1"
type: "Class"
version: "v1.0"
---
```

## Formatting and Structure

Follow these guidelines for formatting and structuring your markdown content:

- **Headings**: Use `##` for H2 and `###` for H3. Ensure that headings are used in a hierarchical manner. Recommend restructuring if content includes H4, and more strongly recommend for H5.
- **Lists**: Use `-` for bullet points and `1.` for numbered lists. Indent nested lists with two spaces.
- **Code Blocks**: Use triple backticks (```) to create fenced code blocks. Specify the language after the opening backticks for syntax highlighting (e.g., ```csharp).
- **Links**: Use `[link text](https://example.com)` for links. Ensure that the link text is descriptive and the URL is valid.
- **Images**: Use `![alt text](https://example.com/image.jpg)` for images. Include a brief description of the image in the alt text.
- **Tables**: Use `|` to create tables. Ensure that columns are properly aligned and headers are included.
- **Line Length**: Break lines at 400 characters to improve readability. Use soft line breaks for long paragraphs.
- **Whitespace**: Use blank lines to separate sections and improve readability. Avoid excessive whitespace.

## Validation Requirements

Ensure compliance with the following validation requirements:

- **Content Rules**: Ensure that the content follows the markdown content rules specified above.
- **Formatting**: Ensure that the content is properly formatted and structured according to the guidelines.
- **Validation**: Run the validation tools to check for compliance with the rules and guidelines.
