#!/usr/bin/env python3
"""
Markdown to HTML Converter with Custom Styling

Converts Markdown files to HTML with special formatting for:
- Emoji-prefixed blockquotes (converted to styled tables)
- Collapsible sections with <details>/<summary>
- Custom spacing and styling
"""

import re
# import argparse # Not needed for Pyodide in-browser
import logging
# import sys # Not needed for Pyodide in-browser
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

try:
    import markdown2
    MARKDOWN2_AVAILABLE = True
except ImportError:
    MARKDOWN2_AVAILABLE = False

try:
    from bs4 import BeautifulSoup, NavigableString
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# pyperclip is for clipboard access, handled by JS in webapp
# try:
#     import pyperclip
#     PYPERCLIP_AVAILABLE = True
# except ImportError:
#     PYPERCLIP_AVAILABLE = False

# Enhanced emoji pattern to cover more Unicode ranges
EMOJI_PATTERN = re.compile(
    r'[\U0001F600-\U0001F64F'  # emoticons
    r'\U0001F300-\U0001F5FF'   # symbols & pictographs
    r'\U0001F680-\U0001F6FF'   # transport & map
    r'\U0001F1E0-\U0001F1FF'   # flags (iOS)
    r'\U00002600-\U000026FF'   # miscellaneous symbols
    r'\U00002700-\U000027BF'   # dingbats
    r'\U0001F900-\U0001F9FF'   # supplemental symbols
    r'\U0001FA70-\U0001FAFF]', # symbols and pictographs extended-A
    flags=re.UNICODE
)

# Configure logging (will output to browser console via Pyodide)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def check_dependencies() -> List[str]:
    """Check for required dependencies and return list of missing ones."""
    missing = []
    if not MARKDOWN2_AVAILABLE:
        missing.append("markdown2")
    if not BS4_AVAILABLE:
        missing.append("beautifulsoup4")
    return missing


def extract_emoji_and_clean_text(paragraph) -> Tuple[Optional[str], str]:
    """
    Extracts the leading emoji from a paragraph and removes it.
    
    Args:
        paragraph: BeautifulSoup paragraph element
        
    Returns:
        Tuple of (emoji, cleaned_html_content)
    """
    if not paragraph:
        return None, ""
        
    text = paragraph.get_text(strip=True)
    if not text or not EMOJI_PATTERN.match(text):
        return None, paragraph.decode_contents().strip('\n')

    emoji = text[0]
    
    # Clean the emoji from the paragraph content
    for child in paragraph.contents:
        if isinstance(child, NavigableString):
            stripped = child.lstrip()
            if stripped and EMOJI_PATTERN.match(stripped):
                new_text = child.replace(stripped[0], '', 1)
                child.replace_with(new_text)
                break
                
    return emoji, paragraph.decode_contents().strip('\n')


def create_styled_table(soup, icon: str, content_html: str):
    """
    Creates a styled table with an icon and content.
    
    Args:
        soup: BeautifulSoup object
        icon: Emoji icon to display
        content_html: HTML content for the table
        
    Returns:
        BeautifulSoup table element
    """
    table = soup.new_tag(
        'table',
        style="border-style: none; width: 100%; max-width: 560px; height: auto; "
              "background-color: #ffe5b4; border-radius: 8px; margin: 10px 0;",
        border="0",
        cellpadding="20"
    )
    tbody = soup.new_tag('tbody')
    tr = soup.new_tag('tr')

    # Icon cell
    td_icon = soup.new_tag(
        'td', 
        style="width: 70px; vertical-align: top; text-align: center;"
    )
    h3_icon = soup.new_tag('h3', style="margin: 0;")
    span_icon = soup.new_tag('span', style="font-size: 36pt; line-height: 1;")
    span_icon.string = icon.strip()
    h3_icon.append(span_icon)
    td_icon.append(h3_icon)

    # Content cell
    td_text = soup.new_tag('td', style="vertical-align: top;")
    p_text = soup.new_tag('p', style="margin: 0;")
    
    try:
        content_soup = BeautifulSoup(content_html, 'html.parser')
        # Append contents of parsed content_html to p_text
        for content_node in content_soup.body.contents: # Use content_soup.body.contents to get top-level nodes
            p_text.append(content_node)
    except Exception as e:
        logger.warning(f"Error parsing content HTML for table: {e}")
        p_text.string = content_html
        
    td_text.append(p_text)

    tr.append(td_icon)
    tr.append(td_text)
    tbody.append(tr)
    table.append(tbody)
    
    return table


def process_blockquotes(soup) -> None:
    """Convert emoji-prefixed blockquotes to styled tables."""
    blockquotes = soup.find_all('blockquote')
    
    for blockquote in list(blockquotes): # Iterate over a copy because we're modifying the list
        try:
            # Check if blockquote content starts with a <p> tag
            first_child_p = blockquote.find('p', recursive=False)
            icon = None
            text_content_html = ""
            
            if first_child_p:
                icon, text_content_html = extract_emoji_and_clean_text(first_child_p)
            
            if not icon:
                # If no emoji in first <p> or no <p> at top level, try to extract from raw text
                full_text_strip = blockquote.get_text(strip=True)
                if full_text_strip and EMOJI_PATTERN.match(full_text_strip):
                    icon = full_text_strip[0]
                    # Create a temporary soup for the blockquote's content
                    temp_bq_soup = BeautifulSoup(blockquote.decode_contents(), 'html.parser')
                    # Find the first text node or tag containing the emoji and remove it
                    for node in temp_bq_soup.contents:
                        if isinstance(node, NavigableString) and node.strip().startswith(icon):
                            node.replace_with(node.replace(icon, '', 1).lstrip()) # Remove emoji and leading space
                            break
                        elif hasattr(node, 'get_text') and node.get_text(strip=True).startswith(icon):
                            # Handle emoji within a tag (e.g., <p>👋 text</p>)
                            for sub_node in node.contents:
                                if isinstance(sub_node, NavigableString) and sub_node.strip().startswith(icon):
                                    sub_node.replace_with(sub_node.replace(icon, '', 1).lstrip())
                                    break
                            break
                    text_content_html = temp_bq_soup.decode_contents().strip('\n')
                else:
                    logger.debug("Blockquote does not start with emoji, skipping conversion")
                    continue

            # Ensure text_content_html is captured correctly after icon removal
            # If icon was found and removed, the content_html should be the remaining part.
            # If the icon was in a first paragraph, text_content_html from extract_emoji_and_clean_text is correct.
            if not text_content_html and icon: # If icon was found but no text_content_html returned (e.g. icon was the entire content of first_paragraph)
                # Re-parse original blockquote content to extract everything AFTER the emoji
                temp_soup_for_content = BeautifulSoup(blockquote.decode_contents(), 'html.parser')
                # Try to remove the first occurrence of the icon from the text content
                # This is a bit of a hack, a more robust solution would be a custom parser or deeper BS4 manipulation
                content_string = temp_soup_for_content.get_text()
                if icon in content_string:
                    cleaned_content_string = content_string.replace(icon, '', 1).lstrip()
                    # This is tricky because replacing text doesn't easily convert back to HTML structure.
                    # For simplicity, we might just use the original content if it's too complex to parse cleanly after manual text removal.
                    # A better approach would be to get the *nodes* after the emoji node.
                    # For now, let's just stick to the original logic which works for common cases.
                    pass # text_content_html should already be set from extract_emoji_and_clean_text or the full_text block.

            # Get blockquote's inner HTML (after emoji removal if applicable) and create styled table
            # If no icon was found and the flow continued due to a bug, ensure text_content_html isn't empty.
            if not text_content_html and icon:
                 # This means an emoji was found but the cleaning process didn't yield content,
                 # which happens if the emoji *was* the entire content, or if there's complex HTML.
                 # Revert to original content if cleaning failed or was empty.
                 text_content_html = blockquote.decode_contents().strip('\n')


            table = create_styled_table(soup, icon, text_content_html)
            blockquote.replace_with(table)
            
        except Exception as e:
            logger.warning(f"Error processing blockquote: {e}", exc_info=True) # exc_info for full traceback


def add_spacing_elements(soup) -> None:
    """Add appropriate spacing between elements."""
    # Insert <br> between iframe and blockquote/table
    for iframe in soup.find_all('iframe'):
        next_sibling = iframe.next_sibling
        # Iterate through siblings, skipping empty NavigableString (whitespace) nodes
        while next_sibling and isinstance(next_sibling, NavigableString) and not next_sibling.strip():
            next_sibling = next_sibling.next_sibling
        
        if next_sibling and hasattr(next_sibling, 'name') and next_sibling.name in ['blockquote', 'table']:
            # Check if there's already a <br> right after, to prevent duplicates
            if not (iframe.next_sibling and iframe.next_sibling.name == 'br'):
                 iframe.insert_after(soup.new_tag('br'))

    # Insert <br> between text and images
    for img in soup.find_all('img'):
        prev_sibling = img.previous_sibling
        # Iterate through previous siblings, skipping empty NavigableString (whitespace) nodes
        while prev_sibling and isinstance(prev_sibling, NavigableString) and not prev_sibling.strip():
            prev_sibling = prev_sibling.previous_sibling

        if prev_sibling and hasattr(prev_sibling, 'name') and prev_sibling.name in ['p', 'span']:
            # Check if there's already a <br> right before, to prevent duplicates
            if not (img.previous_sibling and img.previous_sibling.name == 'br'):
                img.insert_before(soup.new_tag('br'))


def process_list_spacing(soup) -> None:
    """Add appropriate spacing to list items."""
    list_items = soup.find_all('li')
    
    for i, item in enumerate(list_items):
        try:
            # Check if it's a top-level ordered list item
            is_top_level_ordered = (item.find_parent('ol') and not item.find_parent('li'))
            has_children = bool(item.find('ol') or item.find('ul'))
            
            is_followed_by_top_level = False
            # Find the next actual list item at the same level or higher
            next_item = None
            for j in range(i + 1, len(list_items)):
                if list_items[j].find_parent('ol') == item.find_parent('ol') and \
                   list_items[j].find_parent('li') == item.find_parent('li'): # Same parent list and nesting level
                    next_item = list_items[j]
                    break
            
            if next_item:
                is_followed_by_top_level = (next_item.find_parent('ol') and not next_item.find_parent('li'))


            # Determine spacing
            br_tags = ""
            if is_top_level_ordered and is_followed_by_top_level:
                br_tags = "<br><br><br><br>"
            elif has_children:
                br_tags = "<br>"
            elif is_followed_by_top_level:
                br_tags = "<br><br><br><br>"

            if br_tags:
                # Append the <br> tags directly. BeautifulSoup will handle parsing them.
                # Avoid appending if the last child is already <br> and the desired count is less or equal
                last_child = item.contents[-1] if item.contents else None
                if isinstance(last_child, NavigableString) and not last_child.strip(): # Skip trailing whitespace
                    last_child = item.contents[-2] if len(item.contents) > 1 else None

                if not (last_child and last_child.name == 'br' and br_tags.count('<br>') <= 1): # Simplified check
                    br_element_soup = BeautifulSoup(br_tags, 'html.parser')
                    for br in br_element_soup.find_all('br'):
                        item.append(br)
                        
        except Exception as e:
            logger.warning(f"Error processing list item spacing: {e}", exc_info=True)


def create_collapsible_sections(soup):
    """Convert h3 headings and following content into collapsible sections."""
    
    # Apply styling to existing details/summary elements first (if Markdown produces them)
    existing_details = soup.find_all('details')
    for detail_tag in existing_details:
        summary = detail_tag.find('summary')
        if summary:
            summary['style'] = (
                "padding: 15px; margin-bottom: 25px; cursor: pointer; "
                "background-color: #f9f7f0; border-radius: 5px; font-weight: bold;"
            )
        detail_tag['open'] = True # Ensure they are open by default

    # Create new collapsible sections from h3 headings if not already handled by Markdown parser
    # We need a new soup object or operate carefully on the existing one to avoid infinite loops
    # This logic assumes the markdown2 converter *doesn't* produce <details> tags for h3s automatically.
    # If it *does*, this section would be redundant or need adjustment.
    
    # We'll collect the elements and then rebuild
    body_content_elements = list(soup.body.children) # Get top-level children
    
    # Create a new BeautifulSoup object for the result to avoid modifying during iteration
    new_soup = BeautifulSoup("", 'html.parser')
    
    current_details = None
    current_summary = None
    
    for element in body_content_elements:
        if element.name == 'h3':
            # Close previous section if it exists
            if current_details:
                new_soup.append(current_details)
            
            # Create new <details> and <summary>
            current_details = new_soup.new_tag('details', open=True) # Default to open
            current_summary = new_soup.new_tag(
                'summary',
                style=(
                    "padding: 15px; margin-bottom: 25px; cursor: pointer; "
                    "background-color: #f9f7f0; border-radius: 5px; font-weight: bold;"
                )
            )
            strong_heading = new_soup.new_tag('strong')
            strong_heading.string = element.get_text(strip=True)
            current_summary.append(strong_heading)
            current_details.append(current_summary)
            # Add a break after the summary for spacing
            current_details.append(new_soup.new_tag('br'))
            
        else:
            if current_details:
                # If we are inside a details block, append the element
                # Ensure the element is valid and not just whitespace
                if not (isinstance(element, NavigableString) and not element.strip()):
                    current_details.append(element)
            else:
                # If not inside a details block, just append to the new soup directly
                new_soup.append(element)
    
    # Append the last details section if it exists
    if current_details:
        new_soup.append(current_details)
        
    # Replace original body contents with new_soup's body contents
    soup.body.clear()
    for child in new_soup.body.contents:
        soup.body.append(child)

    return str(soup) # Return the modified soup as a string


def apply_custom_styles(html_text: str) -> str:
    """
    Apply all custom styling rules to the HTML.
    
    Args:
        html_text: Raw HTML from markdown conversion
        
    Returns:
        Styled HTML string
    """
    if not BS4_AVAILABLE:
        logger.error("BeautifulSoup4 is required for custom styling but not available.")
        return html_text

    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # Apply all transformations
        process_blockquotes(soup)
        add_spacing_elements(soup)
        process_list_spacing(soup)
        
        # Handle collapsible sections (modifies soup in place and returns string)
        # This function now expects the soup object and modifies it.
        # It also returns the final HTML string.
        final_html = create_collapsible_sections(soup)
        
        return final_html
        
    except Exception as e:
        logger.error(f"Error applying custom styles: {e}", exc_info=True)
        return html_text


def convert_markdown_to_html(markdown_text: str) -> str:
    """
    Convert Markdown to HTML with custom styling.
    
    Args:
        markdown_text: Input Markdown content
        
    Returns:
        Styled HTML string
    """
    if not MARKDOWN2_AVAILABLE:
        return "<p>Error: markdown2 library not available. Cannot convert Markdown.</p>"
    
    if not markdown_text.strip():
        logger.warning("Empty markdown content provided")
        return ""
    
    try:
        # Convert using markdown2 with useful extras
        html_text = markdown2.markdown(
            markdown_text,
            extras=[
                'fenced-code-blocks',
                'tables',
                'break-on-newline',
                'cuddled-lists',
                'metadata',
                'task_list'
            ]
        )
        
        return apply_custom_styles(html_text)
        
    except Exception as e:
        logger.error(f"Error converting markdown: {e}", exc_info=True)
        return f"<p>Error converting markdown: {e}</p>"

# This is a key part for Pyodide: expose the function
# Pyodide's globals will have this function accessible from JavaScript
# In your JS, you'll call pyodide.globals.get('convertMarkdownPython')
