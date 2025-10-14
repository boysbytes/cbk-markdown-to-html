import React, { useState, useMemo } from "react";
import { marked } from "marked";
// Importing Button and Copy from lucide-react and shadcn/ui respectively
import { Copy } from "lucide-react";

// Shadcn Button component (simplified for direct inclusion)
const Button = ({ children, onClick, variant, size, title, className }) => {
  const baseClasses = "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50";
  const variants = {
    outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
    ghost: "hover:bg-accent hover:text-accent-foreground",
    default: "bg-primary text-primary-foreground hover:bg-primary/90",
  };
  const sizes = {
    default: "h-10 px-4 py-2",
    sm: "h-9 rounded-md px-3",
    lg: "h-11 rounded-md px-8",
    icon: "h-10 w-10",
  };

  return (
    <button
      className={`${baseClasses} ${variants[variant || "default"]} ${sizes[size || "default"]} ${className || ""}`}
      onClick={onClick}
      title={title}
    >
      {children}
    </button>
  );
};

// Function to format the raw HTML by applying custom transformations
function formatHtml(html, addSpacingNumberedLists, addBorderRadius) { // Added addBorderRadius parameter
  // Return original HTML if window object is not defined (e.g., during Server-Side Rendering)
  if (typeof window === "undefined") return html; 

  const parser = new window.DOMParser();
  // Parse the HTML string into a DOM document, wrapped in a div for consistent parsing
  const doc = parser.parseFromString(`<div>${html}</div>`, "text/html");
  const container = doc.body.firstChild;
  // If no container element is found, return the original HTML
  if (!container) return html;

  // --- Step 1: <h3> to <details> transformation ---
  // This loop iterates through the direct children of the container
  let node = container.firstChild;
  while (node) {
    // Check if the current node is an H3 element
    if (node.nodeName === "H3") {
      const summary = doc.createElement("summary");
      // Define base styles for the summary element
      let summaryStyle = "padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;";
      // Conditionally add border-radius based on the addBorderRadius parameter
      if (addBorderRadius) {
        summaryStyle += "border-radius:10px;";
      }
      // Apply inline styles to the summary element for visual presentation
      summary.setAttribute("style", summaryStyle);
      // Assign the entire innerHTML of the H3 node to the summary, wrapped in <strong>
      // This change ensures all content from the <h3> is included without specific replacements.
      summary.innerHTML = `<strong>${node.innerHTML}</strong>`; 
      const details = doc.createElement("details");
      details.appendChild(summary);

      // Move all consecutive block-level siblings after the <h3> into the <details> element
      // This loop continues as long as there is a next sibling and it's not another H3
      let next = node.nextSibling;
      while (next && next.nodeName !== "H3") {
        const toMove = next;
        next = next.nextSibling; // Advance next before appending to avoid infinite loop
        details.appendChild(toMove);
      }
      
      // Replace the original H3 element with the new <details> element
      const toReplace = node;
      node = details; // Set node to the newly created details element to continue iteration correctly
      container.replaceChild(details, toReplace);
    }
    // Move to the next sibling in the container
    node = node.nextSibling;
  }

  // --- Step 2: Emoji <blockquote> transformation ---
  // Use querySelectorAll to find all blockquote elements in the entire document
  const blockquotes = doc.querySelectorAll('blockquote');
  blockquotes.forEach(blockquote => {
    // Check if the blockquote contains a paragraph as its first child
    if (blockquote.firstElementChild) {
      const firstChild = blockquote.firstElementChild;
      const firstChildHtml = firstChild.innerHTML.trim();
      // Regex to match most emojis at the start of the string, followed by an optional space
      const emojiMatch = firstChildHtml.match(/^([\u231A-\u32FF\uD83C-\uDBFF\uDC00-\uDFFF\u2600-\u27BF\uFE0F\u200D]+)\s*/);

      if (emojiMatch) {
        const emoji = emojiMatch[1];
        // The text content of the first paragraph *after* the emoji
        const remainingFirstChildHtml = firstChildHtml.substring(emojiMatch[0].length).trim();

        // Create the table structure
        const table = doc.createElement("table");
        // Apply inline styles and attributes to the table for layout and appearance
        table.setAttribute("style", "border-style: none; width: 560px; height: 73px; background-color: #ffe5b4;"); // Set exact width and height
        table.setAttribute("border", "0");
        table.setAttribute("cellpadding", "20");
        const tbody = doc.createElement("tbody");
        const tr = doc.createElement("tr");

        // First TD for emoji
        const td1 = doc.createElement("td");
        // Changed vertical-align to 'middle' to center the emoji vertically
        td1.setAttribute("style", "width: 70.9062px; vertical-align: middle;"); 
        const h3 = doc.createElement("h3");
        h3.setAttribute("style", "font-size: 48px; margin: 0;"); // Set font-size and margin
        const span = doc.createElement("span"); // Create span for emoji
        span.setAttribute("style", "font-size: 48px;"); // Set font-size on span
        span.innerHTML = emoji;
        h3.appendChild(span);
        td1.appendChild(h3);

        // Second TD for text content and subsequent elements
        const td2 = doc.createElement("td");
        td2.setAttribute("style", "width: 488.094px; vertical-align: middle;"); // Set exact width and vertical-align

        // Append the remaining content of the first child, if any
        if (remainingFirstChildHtml) {
            const p = doc.createElement('p');
            p.innerHTML = remainingFirstChildHtml;
            td2.appendChild(p);
        }

        // Move all subsequent siblings of the first child into td2
        // This ensures lists and other elements within the blockquote are correctly moved
        let currentSibling = firstChild.nextElementSibling; // Use nextElementSibling to skip text nodes
        while (currentSibling) {
            const nodeToMove = currentSibling;
            currentSibling = currentSibling.nextElementSibling;
            td2.appendChild(nodeToMove);
        }

        tr.appendChild(td1);
        tr.appendChild(td2);
        tbody.appendChild(tr);
        table.appendChild(tbody);

        // Replace the original blockquote element with the new table element
        blockquote.parentNode.replaceChild(table, blockquote);
      }
    }
  });

  // --- Step 3: Convert nested ordered lists to alphabetical type ---
  // Use a recursive approach to catch all nested <ol> that are not top-level
  // Set type="a" for any <ol> that is not a direct child of the container (i.e., not top-level)
  const allOrderedLists = container.querySelectorAll('ol');
  allOrderedLists.forEach(ol => {
    if (ol.parentElement !== container) {
      const typeAttr = ol.getAttribute('type');
      if (!typeAttr || typeAttr.trim().toLowerCase() === '1') {
        ol.setAttribute('type', 'a');
      }
    }
  });

  // --- Step 4: Custom Line Spacing for transformed tables ---
  // Helper function to add line spacing (br tags) around specified elements
  const addLineSpacing = (targetTagName, count = 1) => {
    const elements = container.querySelectorAll(targetTagName);
    elements.forEach(el => {
      // Check if a <br> or significant content exists before the element
      let prevNode = el.previousSibling;
      let needsBrBefore = true;
      while (prevNode) {
        if (prevNode.nodeName === 'BR') {
          needsBrBefore = false;
          break;
        }
        // If it's an element or non-empty text node, we can add a <br>
        if (prevNode.nodeType === Node.ELEMENT_NODE || (prevNode.nodeType === Node.TEXT_NODE && prevNode.nodeValue.trim() !== '')) {
          break; // Found content, so we can add <br>
        }
        prevNode = prevNode.previousSibling;
      }

      if (needsBrBefore) {
        el.parentNode.insertBefore(doc.createElement('br'), el);
      }

      // Check if sufficient <br> tags exist after the element
      let nextNode = el.nextSibling;
      let brCountAfter = 0;
      while (nextNode && nextNode.nodeName === 'BR') {
        brCountAfter++;
        nextNode = nextNode.nextSibling;
      }

      // Only add if less than 'count' BRs exist immediately after
      if (brCountAfter < count) {
        for (let i = 0; i < (count - brCountAfter); i++) {
          el.parentNode.insertBefore(doc.createElement('br'), el.nextSibling);
        }
      }
    });
  };

  // Apply line spacing specifically to the tables created from blockquotes
  addLineSpacing('table');

  // --- Step 5: Custom Line Spacing after first-level numbered list items ---
  if (addSpacingNumberedLists) {
    const orderedLists = container.querySelectorAll('ol');
    orderedLists.forEach(ol => {
      // Iterate through direct children (first-level list items)
      Array.from(ol.children).forEach(li => {
        if (li.nodeName === 'LI') {
          // Check if it's not the last list item in the current ordered list
          // We only add spacing if there's a subsequent sibling (another li or other content)
          if (li.nextSibling) {
            let brCountAtEnd = 0;
            // Count existing <br> tags at the very end of the current list item's content
            let lastChild = li.lastChild;
            while (lastChild && lastChild.nodeName === 'BR') {
                brCountAtEnd++;
                lastChild = lastChild.previousSibling;
            }

            // Insert <br> tags if less than 3 exist at the end of the li
            if (brCountAtEnd < 3) {
              for (let i = 0; i < (3 - brCountAtEnd); i++) {
                li.appendChild(doc.createElement('br')); // Append BR directly to the LI
              }
            }
          }
        }
      });
    });
  }

  // Return the inner HTML of the container after all transformations
  return container.innerHTML;
}

// Main React component for the Markdown to HTML converter application
export default function MarkdownToHtmlApp() {
  // State to store the markdown input
  const [markdown, setMarkdown] = useState("");
  // State to manage the "Copied!" message visibility
  const [copied, setCopied] = useState(false);
  // State for custom spacing option for numbered lists, set to true by default
  const [addSpacingNumberedLists, setAddSpacingNumberedLists] = useState(true); // Enabled by default
  // State for optional border-radius on summary element - now defaults to false
  const [addBorderRadius, setAddBorderRadius] = useState(false); // Changed default to false

  // Memoized HTML output, re-calculates only when markdown or spacing options change
  const html = useMemo(() => {
    // If window is not defined (e.g., during SSR), parse markdown without DOM manipulation
    if (typeof window === "undefined") {
      return marked.parse(markdown, { gfm: true });
    }
    // Parse markdown to raw HTML
    const raw = marked.parse(markdown, { gfm: true });
    // Format the raw HTML using the custom formatHtml function, passing spacing options
    return formatHtml(raw, addSpacingNumberedLists, addBorderRadius);
  }, [markdown, addSpacingNumberedLists, addBorderRadius]); // Add addBorderRadius to dependencies

  // Handler for copying the HTML output to the clipboard
  const handleCopy = () => {
    // Fallback to document.execCommand('copy') for better compatibility in iframes
    if (document.execCommand) {
      const textarea = document.createElement('textarea');
      textarea.value = html;
      textarea.style.position = 'fixed'; // Prevent scrolling to bottom
      textarea.style.left = '-9999px'; // Hide off-screen
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
        setCopied(true);
        setTimeout(() => setCopied(false), 1200);
      } catch (err) {
        console.error("Failed to copy using execCommand: ", err);
        // Fallback to navigator.clipboard.writeText if execCommand fails (though less likely to work if execCommand is preferred)
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(html)
            .then(() => {
              setCopied(true);
              setTimeout(() => setCopied(false), 1200);
            })
            .catch(e => console.error("Failed to copy using navigator.clipboard: ", e));
        }
      } finally {
        document.body.removeChild(textarea);
      }
    } else if (navigator.clipboard && navigator.clipboard.writeText) {
      // Original navigator.clipboard.writeText as a primary fallback if execCommand is not available
      navigator.clipboard.writeText(html)
        .then(() => {
          setCopied(true);
          setTimeout(() => setCopied(false), 1200);
        })
        .catch(err => console.error("Failed to copy: ", err));
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-8 px-2 font-sans">
      <h1 className="text-3xl font-bold mb-4 text-center text-gray-800">Markdown to HTML Converter</h1>
      <div className="w-full max-w-5xl grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {/* Markdown Input Section */}
        <div className="flex flex-col">
          <label htmlFor="markdown-input" className="font-semibold mb-2 text-gray-700">Markdown</label>
          <textarea
            id="markdown-input"
            className="w-full h-80 p-3 rounded-2xl border border-gray-200 bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all duration-200"
            value={markdown}
            onChange={e => setMarkdown(e.target.value)}
            spellCheck={false}
            placeholder="Enter your Markdown here..."
          />
        </div>
        {/* HTML Output Section */}
        <div className="flex flex-col relative">
          <label htmlFor="html-output" className="font-semibold mb-2 text-gray-700">HTML Output</label>
          <textarea
            id="html-output"
            className="w-full h-80 p-3 rounded-2xl border border-gray-200 bg-gray-100 font-mono shadow-md resize-none"
            value={html}
            readOnly
            spellCheck={false}
          />
          {/* Copy Button */}
          <div className="absolute top-2 right-2">
            <Button
              variant="outline"
              size="icon"
              title="Copy HTML"
              onClick={handleCopy}
              className="bg-white hover:bg-gray-100 border-gray-300 text-gray-600 hover:text-gray-800 rounded-full shadow-sm"
            >
              <Copy className="w-4 h-4" />
            </Button>
          </div>
          {/* Copied Message */}
          {copied && (
            <span className="absolute top-2 right-16 bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs shadow-md animate-fade-in">
              Copied!
            </span>
          )}
        </div>
      </div>

      {/* Custom Options Section */}
      <details className="w-full max-w-5xl mb-4 p-4 bg-white rounded-2xl shadow-lg border border-gray-200">
        <summary className="font-bold text-lg cursor-pointer text-gray-800">Custom Options</summary>
        <div className="mt-4 space-y-2"> {/* Added space-y-2 for spacing between options */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="spacing-numbered-lists"
              className="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              checked={addSpacingNumberedLists}
              onChange={(e) => setAddSpacingNumberedLists(e.target.checked)}
            />
            <label htmlFor="spacing-numbered-lists" className="text-gray-700 select-none">Add 3 lines spacing after first-level numbered list items</label>
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="border-radius-summary"
              className="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              checked={addBorderRadius}
              onChange={(e) => setAddBorderRadius(e.target.checked)}
            />
            <label htmlFor="border-radius-summary" className="text-gray-700 select-none">Add rounded corners to section titles</label>
          </div>
        </div>
      </details>
    </div>
  );
}
