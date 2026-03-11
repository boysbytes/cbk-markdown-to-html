# GitHub Copilot Instructions for Building HTML Tools

## Core Principles

When building HTML tools, follow these essential patterns:

### Architecture
- Create **single-file HTML applications** with inline JavaScript and CSS
- Avoid React, JSX, or anything requiring a build step
- Keep tools small (a few hundred lines maximum)
- Make tools easily copyable and pasteable

### Dependencies
- Load all dependencies from CDNs (cdnjs.cloudflare.com or jsdelivr.com)
- **Always include version numbers in CDN URLs** for long-term reliability
- Minimize dependencies - only use well-known libraries when necessary
- Never use external CSS files - inline all styles in `<style>` tags

## Code Structure

### Basic Template
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tool Name</title>
    <style>
        /* Inline all CSS here */
    </style>
</head>
<body>
    <!-- HTML content -->
    <script>
        // Inline all JavaScript here
    </script>
</body>
</html>
```

## Key Patterns

### State Persistence

**URL Parameters for Shareable State:**
- Use URL hash or search parameters for state that should be shareable
- Serialize complex state as JSON in URLs
- Update URLs when state changes for bookmarkability
```javascript
// Reading from URL
const params = new URLSearchParams(window.location.search);
const state = JSON.parse(params.get('state') || '{}');

// Writing to URL
const newUrl = new URL(window.location);
newUrl.searchParams.set('state', JSON.stringify(state));
window.history.replaceState({}, '', newUrl);
```

**localStorage for Secrets and Large State:**
- Store API keys in localStorage, never in URLs or HTML
- Use localStorage for work-in-progress content
- Save automatically as users type
```javascript
// Storing API key
const apiKey = localStorage.getItem('api_key') || prompt('Enter API key:');
if (apiKey) localStorage.setItem('api_key', apiKey);

// Auto-save content
textarea.addEventListener('input', (e) => {
    localStorage.setItem('draft', e.target.value);
});
```

### User Input/Output

**Copy and Paste:**
- Make copy-to-clipboard functionality prominent
- Handle rich paste events with multiple data formats
```javascript
// Copy to clipboard
async function copyToClipboard(text) {
    await navigator.clipboard.writeText(text);
    // Show feedback to user
}

// Handle rich paste
element.addEventListener('paste', (e) => {
    e.preventDefault();
    const items = e.clipboardData.items;
    for (let item of items) {
        if (item.type.startsWith('image/')) {
            const blob = item.getAsFile();
            // Process image
        } else if (item.type === 'text/html') {
            item.getAsString(html => {
                // Process HTML
            });
        }
    }
});
```

**File Handling:**
- Use `<input type="file">` to process files client-side
- No server upload needed - read files directly in JavaScript
```javascript
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
        const content = event.target.result;
        // Process file content
    };
    reader.readAsText(file); // or readAsDataURL() for binary
});
```

**File Downloads:**
- Generate downloadable files without server-side processing
```javascript
function downloadFile(content, filename, type = 'text/plain') {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}
```

### API Integration

**CORS-Enabled APIs:**
- Build a collection of APIs that support CORS
- Useful APIs: GitHub, PyPI, iNaturalist, Bluesky, Mastodon
- GitHub raw content is always CORS-enabled and CDN-cached

**LLM APIs:**
- All major LLM providers (OpenAI, Anthropic, Google) support CORS
- Store API keys in localStorage
- Prompt users for keys on first use
```javascript
async function callClaude(messages) {
    const apiKey = localStorage.getItem('anthropic_api_key');
    if (!apiKey) {
        const key = prompt('Enter Anthropic API key:');
        localStorage.setItem('anthropic_api_key', key);
    }
    
    const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': apiKey,
            'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
            model: 'claude-3-sonnet-20240229',
            max_tokens: 1024,
            messages: messages
        })
    });
    return response.json();
}
```

### Advanced Capabilities

**Python in Browser (Pyodide):**
- Load Pyodide from CDN for Python execution
- Use micropip to load pure-Python packages from PyPI
```javascript
// Load Pyodide
<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>

// Initialize and run Python
async function runPython() {
    let pyodide = await loadPyodide();
    await pyodide.loadPackage('numpy');
    return pyodide.runPython(`
        import numpy as np
        result = np.array([1, 2, 3])
        result.tolist()
    `);
}
```

**WebAssembly:**
- Load WASM libraries from CDN when available
- Examples: Tesseract.js for OCR, SQLite WASM

## UI/UX Best Practices

### User Experience
- Show loading indicators for async operations
- Provide clear error messages
- Include "Copy" buttons for generated output
- Make mobile-friendly (copy/paste is harder on mobile)
- Add keyboard shortcuts for power users

### Visual Feedback
- Show success/error states clearly
- Animate state transitions smoothly
- Display progress for long operations

### Accessibility
- Use semantic HTML
- Include proper ARIA labels
- Ensure keyboard navigation works
- Maintain good color contrast

## Development Workflow

### Prototyping
1. Start with Claude Artifacts, ChatGPT Canvas, or Gemini Canvas
2. Use prompt: "Build an artifact/canvas that [description]. No React."
3. Iterate until working
4. Copy final HTML to GitHub repository

### Hosting
- Use GitHub Pages for simple static hosting
- Configure repository: Settings → Pages → Deploy from main branch
- Access at `username.github.io/repository/filename.html`

### Documentation
- Include usage instructions in HTML comments
- Link to source in footer
- Record prompts and transcripts used to create the tool
- Save prompts in commit messages

## Common Patterns

### Debugging Tools
Build tools to understand capabilities:
- Clipboard format viewer
- Keyboard event debugger
- CORS tester
- EXIF data viewer

### Transform Tools
- JSON ↔ YAML converters
- Markdown renderers
- Image format converters
- Code formatters

### API Integration Tools
- GitHub issue to Markdown
- Package changelog generators
- Social media thread viewers
- API response explorers

## Quality Checklist

Before committing a tool, verify:
- [ ] All CSS is inline in `<style>` tags
- [ ] All JavaScript is inline in `<script>` tags
- [ ] Dependencies load from versioned CDN URLs
- [ ] No build step required
- [ ] Works when copied to any web server
- [ ] Mobile-friendly (if applicable)
- [ ] Includes error handling
- [ ] Has clear user instructions
- [ ] Stores secrets in localStorage (never in HTML/URLs)
- [ ] File is under 1000 lines

## Prohibited Patterns

**Never use:**
- React, Vue, or frameworks requiring JSX compilation
- npm packages that need bundling
- Server-side processing requirements
- Hardcoded API keys in source
- External CSS or JavaScript files (use CDN for libraries)

## Example Prompts

**For Claude:**
> "Build an artifact that lets me paste in JSON and shows it formatted with syntax highlighting. Include a copy button. No React. Use a CDN for any libraries."

**For ChatGPT/Gemini:**
> "Build a canvas that converts Markdown to HTML with live preview. Add copy button for the HTML output. No React. Load dependencies from CDN."

**For Complex Tools:**
> "Create a single-file HTML tool that: [detailed requirements]. Use inline CSS and JavaScript. Load any needed libraries from cdnjs. Store user preferences in localStorage. Make all output copyable with one click. No build step required."

## Resources

### Recommended CDNs
- **cdnjs.cloudflare.com** - Comprehensive library collection
- **cdn.jsdelivr.net** - Fast, reliable alternative
- **unpkg.com** - Direct npm package access

### Useful Libraries
- **Marked.js** - Markdown parsing
- **Highlight.js** - Syntax highlighting
- **Papa Parse** - CSV parsing
- **js-yaml** - YAML parsing
- **Tesseract.js** - OCR
- **Pyodide** - Python in browser
- **PDF.js** - PDF rendering

### CORS-Enabled APIs
- GitHub API (api.github.com)
- PyPI JSON API (pypi.org/pypi/{package}/json)
- iNaturalist API
- Bluesky API
- Most public Mastodon instances

Remember: The goal is to create **small, focused, self-contained tools** that solve specific problems and can be easily shared, modified, and hosted anywhere.