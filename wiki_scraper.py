"""
A web scraper script that starts from a given URL, crawls pages on the same domain,
extracts text content from a specified CSS selector (defaults to 'body'),
and saves it to a file in either plain text (.txt) or Markdown (.md) format.

Usage:
    python wiki_scraper.py <start_url> [-o <output_filename>] [-c <css_selector>] [--format <format>]

Example:
    python wiki_scraper.py "https://en.wikipedia.org/wiki/Python_(programming_language)" -o python_wiki -c "#content" --format md
"""

import argparse
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

def fetch_html(url):
    """
    Fetches the HTML content of a web page.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The HTML content (text) of the page if the request is successful (HTTP 200).
        None: If any network error occurs (e.g., DNS failure, HTTP error status codes).
              An error message is printed to stderr in case of failure.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e: # Catches connection errors, timeouts, HTTP errors etc.
        print(f"Error fetching URL {url}: {e}")
        return None

def parse_html_and_extract_data(html_content, base_url, content_selector='body'):
    """
    Parses HTML content to extract textual data from a specified selector and hyperlinks.

    The function extracts text from the HTML element identified by `content_selector`.
    If the selector doesn't find an element, it defaults to an empty string for text.
    It also finds all hyperlink (<a>) tags, resolves their 'href' attributes
    to absolute URLs using the provided `base_url`, and filters them to
    include only those that are on the same domain (matching scheme and netloc)
    as the `base_url`.

    Args:
        html_content (str): The HTML content of a page as a string.
        base_url (str): The original URL from which the `html_content` was fetched.
                        Used for resolving relative links and filtering by domain.
        content_selector (str, optional): The CSS selector for the main content area
                                          from which to extract text. Defaults to 'body'.

    Returns:
        tuple: A tuple containing two elements:
            - str: The extracted textual content from the specified selector.
                   Returns an empty string if the selector is not found,
                   the element has no text, or if parsing fails.
            - set: A set of unique absolute URLs (strings) found on the page that
                   belong to the same domain as `base_url`.
                   Returns an empty set if parsing fails or no relevant links are found.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
    except Exception as e: # Broad exception for any parsing errors
        print(f"Error parsing HTML from {base_url}: {e}")
        return "", set() # Return empty data if parsing fails

    # Content Extraction from specified selector
    content_element = soup.select_one(content_selector)
    if not content_element:
        print(f"Warning: Content selector '{content_selector}' not found in {base_url}. No text extracted from this element.")
        extracted_text = "" # Return empty string if selector not found
    else:
        # Get text from the selected element, using space as separator and stripping extra whitespace
        extracted_text = content_element.get_text(separator=' ', strip=True)

    # Link Extraction and Filtering
    absolute_links = set()
    parsed_base_url = urlparse(base_url) # Parse base_url once for efficiency
    base_scheme = parsed_base_url.scheme
    base_netloc = parsed_base_url.netloc

    for a_tag in soup.find_all('a', href=True): # Find all <a> tags with an href attribute
        href = a_tag['href']
        # Resolve relative URLs to absolute ones using the base_url
        absolute_link = urljoin(base_url, href)

        # Filter links: only keep those on the same domain as the base_url
        parsed_link = urlparse(absolute_link)
        if parsed_link.scheme == base_scheme and parsed_link.netloc == base_netloc:
            absolute_links.add(absolute_link)

    return extracted_text, absolute_links

def crawl_wiki(start_url):
    """
    Performs a breadth-first crawl of a website starting from `start_url`.

    It collects text (from the specified `content_selector`) from all
    reachable pages on the same domain. A queue is used to manage URLs to visit,
    and a set tracks visited URLs to prevent re-processing and loops.

    Args:
        start_url (str): The initial URL to begin crawling from.
        content_selector (str): The CSS selector for the main content area
                                to extract text from on each page.
        status_callback (function, optional): A function to call with status updates
                                              (e.g., current URL being processed).
                                              Defaults to None.

    Returns:
        str: A single string containing all extracted text content from the
             visited pages (using the selector), with content from each page
             separated by "\n\n" (suitable for Markdown paragraphs).
             Returns an empty string if the start_url cannot be fetched or
             no content is extracted.
    """
    queue = deque()        # Queue for URLs to visit (BFS)
    visited_urls = set()   # Set to keep track of visited URLs to avoid cycles and redundant fetches
    all_pages_content = [] # List to store text content from each page

    # Initialize queue and visited set with the start_url
    queue.append(start_url)
    visited_urls.add(start_url)

    while queue: # Loop as long as there are URLs to process
        current_url = queue.popleft() # Get the next URL from the front of the queue
        if status_callback:
            status_callback(f"Processing: {current_url}")
        else:
            print(f"Crawling: {current_url}") # Fallback if no callback

        html_content = fetch_html(current_url)

        if html_content:
            # Parse the fetched HTML to get text (from selector) and links
            text_content, found_links = parse_html_and_extract_data(html_content, current_url, content_selector)

            if text_content: # Add extracted text if it's not empty
                all_pages_content.append(text_content)

            # Process newly found links
            for link in found_links:
                if link not in visited_urls: # If link hasn't been visited
                    visited_urls.add(link)   # Mark as visited
                    queue.append(link)       # Add to the queue to visit later
        else:
            # If fetching HTML failed, use callback or print, then skip to the next URL
            if status_callback:
                status_callback(f"Failed to fetch {current_url}. Skipping.")
            else:
                print(f"Failed to fetch or parse HTML from {current_url}. Skipping.")
            continue

    # Join content from all pages with double newlines for paragraph separation
    return "\n\n".join(all_pages_content)

def save_content_to_file(content, filename):
    """
    Saves the given string content to a specified file.

    The file is written using UTF-8 encoding. Errors during file operations
    are caught and an error message is printed.

    Args:
        content (str): The string content to be saved to the file.
        filename (str): The name (and path) of the file where the content will be saved.
    """
    try:
        # Open file in write mode with UTF-8 encoding
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content saved to {filename}")
    except IOError as e:
        print(f"Error saving content to {filename}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrapes a website starting from a given URL, following links on the same domain.")
    parser.add_argument("start_url", help="The starting URL to scrape.")
    parser.add_argument("-o", "--output", default="scraped_content.txt",
                        help="Name of the output file (default: scraped_content.txt). Extension will be adjusted by --format.")
    parser.add_argument("-c", "--selector", default="body",
                        help="CSS selector for the main content area (default: 'body')")
    parser.add_argument("--format", default="txt", choices=["txt", "md"],
                        help="Output format (txt or md). Default: txt")

    args = parser.parse_args()

    # Use arguments from command line
    start_page_url = args.start_url
    output_basename = args.output
    content_selector_arg = args.selector
    output_format_arg = args.format

    # Determine output filename based on user input and format
    base_name, _ = os.path.splitext(output_basename)
    output_filename = f"{base_name}.{output_format_arg}"

    # In CLI mode, we don't have a status_callback for crawl_wiki by default.
    # The prints within crawl_wiki will act as the status updates.
    print(f"Starting crawl from: {start_page_url} using selector: '{content_selector_arg}', output format: {output_format_arg}")
    total_scraped_content = crawl_wiki(start_page_url, content_selector_arg, status_callback=None)

    print("\n--- Crawling Complete ---")
    print(f"Total characters scraped: {len(total_scraped_content)}")

    # Print a snippet before saving
    print(f"\nSnippet of total scraped content (first 1000 chars):")
    print(total_scraped_content[:1000])

    save_content_to_file(total_scraped_content, output_filename)
