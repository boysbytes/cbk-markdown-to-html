import React, { useState, useMemo } from "react";
import { marked } from "marked";
import { Copy } from "lucide-react";

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

function formatHtml(html, addSpacingNumberedLists, addBorderRadius) {
  if (typeof window === "undefined") return html;

  const parser = new window.DOMParser();
  const doc = parser.parseFromString(`<div>${html}</div>`, "text/html");
  const container = doc.body.firstChild;
  if (!container) return html;

  let node = container.firstChild;
  while (node) {
    if (node.nodeName === "H3") {
      const summary = doc.createElement("summary");
      let summaryStyle = "padding:15px;margin-bottom:25px;cursor:pointer;background:#f9f7f0;";
      if (addBorderRadius) {
        summaryStyle += "border-radius:10px;";
      }
      summary.setAttribute("style", summaryStyle);
      summary.innerHTML = `<strong>${node.innerHTML}</strong>`;
      const details = doc.createElement("details");
      details.appendChild(summary);

      let next = node.nextSibling;
      while (next && next.nodeName !== "H3") {
        const toMove = next;
        next = next.nextSibling;
        details.appendChild(toMove);
      }

      const toReplace = node;
      node = details;
      container.replaceChild(details, toReplace);
    }
    node = node.nextSibling;
  }

  const blockquotes = doc.querySelectorAll('blockquote');
  blockquotes.forEach(blockquote => {
    if (blockquote.firstElementChild) {
      const firstChild = blockquote.firstElementChild;
      const firstChildHtml = firstChild.innerHTML.trim();
      const emojiMatch = firstChildHtml.match(/^([\u231A-\u32FF\uD83C-\uDBFF\uDC00-\uDFFF\u2600-\u27BF\uFE0F\u200D]+)\s*/);

      if (emojiMatch) {
        const emoji = emojiMatch[1];
        const remainingFirstChildHtml = firstChildHtml.substring(emojiMatch[0].length).trim();

        const table = doc.createElement("table");
        table.setAttribute("style", "border-style: none; width: 560px; height: 73px; background-color: #ffe5b4;");
        table.setAttribute("border", "0");
        table.setAttribute("cellpadding", "20");
        const tbody = doc.createElement("tbody");
        const tr = doc.createElement("tr");

        const td1 = doc.createElement("td");
        td1.setAttribute("style", "width: 70.9062px; vertical-align: middle;");
        const h3 = doc.createElement("h3");
        h3.setAttribute("style", "font-size: 48px; margin: 0;");
        const span = doc.createElement("span");
        span.setAttribute("style", "font-size: 48px;");
        span.innerHTML = emoji;
        h3.appendChild(span);
        td1.appendChild(h3);

        const td2 = doc.createElement("td");
        td2.setAttribute("style", "width: 488.094px; vertical-align: middle;");

        if (remainingFirstChildHtml) {
            const p = doc.createElement('p');
            p.innerHTML = remainingFirstChildHtml;
            td2.appendChild(p);
        }

        let currentSibling = firstChild.nextElementSibling;
        while (currentSibling) {
            const nodeToMove = currentSibling;
            currentSibling = currentSibling.nextElementSibling;
            td2.appendChild(nodeToMove);
        }

        tr.appendChild(td1);
        tr.appendChild(td2);
        tbody.appendChild(tr);
        table.appendChild(tbody);

        blockquote.parentNode.replaceChild(table, blockquote);
      }
    }
  });

  const nestedOrderedLists = container.querySelectorAll('li > ol');
  nestedOrderedLists.forEach(ol => {
    const typeAttr = ol.getAttribute('type');
    if (!typeAttr || typeAttr.trim().toLowerCase() === '1') {
      ol.setAttribute('type', 'a');
    }
  });

  const addLineSpacing = (targetTagName, count = 1) => {
    const elements = container.querySelectorAll(targetTagName);
    elements.forEach(el => {
      let prevNode = el.previousSibling;
      let needsBrBefore = true;
      while (prevNode) {
        if (prevNode.nodeName === 'BR') {
          needsBrBefore = false;
          break;
        }
        if (prevNode.nodeType === Node.ELEMENT_NODE || (prevNode.nodeType === Node.TEXT_NODE && prevNode.nodeValue.trim() !== '')) {
          break;
        }
        prevNode = prevNode.previousSibling;
      }

      if (needsBrBefore) {
        el.parentNode.insertBefore(doc.createElement('br'), el);
      }

      let nextNode = el.nextSibling;
      let brCountAfter = 0;
      while (nextNode && nextNode.nodeName === 'BR') {
        brCountAfter++;
        nextNode = nextNode.nextSibling;
      }

      if (brCountAfter < count) {
        for (let i = 0; i < (count - brCountAfter); i++) {
          el.parentNode.insertBefore(doc.createElement('br'), el.nextSibling);
        }
      }
    });
  };

  addLineSpacing('table');

  if (addSpacingNumberedLists) {
    const orderedLists = container.querySelectorAll('ol');
    orderedLists.forEach(ol => {
      Array.from(ol.children).forEach(li => {
        if (li.nodeName === 'LI') {
          if (li.nextSibling) {
            let brCountAtEnd = 0;
            let lastChild = li.lastChild;
            while (lastChild && lastChild.nodeName === 'BR') {
                brCountAtEnd++;
                lastChild = lastChild.previousSibling;
            }

            if (brCountAtEnd < 3) {
              for (let i = 0; i < (3 - brCountAtEnd); i++) {
                li.appendChild(doc.createElement('br'));
              }
            }
          }
        }
      });
    });
  }

  return container.innerHTML;
}

export default function MarkdownToHtmlApp() {
  const [markdown, setMarkdown] = useState("");
  const [copied, setCopied] = useState(false);
  const [addSpacingNumberedLists, setAddSpacingNumberedLists] = useState(true);
  const [addBorderRadius, setAddBorderRadius] = useState(false);

  const html = useMemo(() => {
    if (typeof window === "undefined") {
      return marked.parse(markdown, { gfm: true });
    }
    const raw = marked.parse(markdown, { gfm: true });
    return formatHtml(raw, addSpacingNumberedLists, addBorderRadius);
  }, [markdown, addSpacingNumberedLists, addBorderRadius]);

  const handleCopy = () => {
    if (document.execCommand) {
      const textarea = document.createElement('textarea');
      textarea.value = html;
      textarea.style.position = 'fixed';
      textarea.style.left = '-9999px';
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
        setCopied(true);
        setTimeout(() => setCopied(false), 1200);
      } catch (err) {
        console.error("Failed to copy using execCommand: ", err);
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
        <div className="flex flex-col relative">
          <label htmlFor="html-output" className="font-semibold mb-2 text-gray-700">HTML Output</label>
          <textarea
            id="html-output"
            className="w-full h-80 p-3 rounded-2xl border border-gray-200 bg-gray-100 font-mono shadow-md resize-none"
            value={html}
            readOnly
            spellCheck={false}
          />
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
          {copied && (
            <span className="absolute top-2 right-16 bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs shadow-md animate-fade-in">
              Copied!
            </span>
          )}
        </div>
      </div>

      <details className="w-full max-w-5xl mb-4 p-4 bg-white rounded-2xl shadow-lg border border-gray-200">
        <summary className="font-bold text-lg cursor-pointer text-gray-800">Custom Options</summary>
        <div className="mt-4 space-y-2">
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
