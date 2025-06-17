# How to Use the Wiki Scraper

## 1. Overview

This document provides detailed instructions on how to use the Wiki Scraper tools. The scraper is designed to crawl a website or wiki, starting from a given URL, extract textual content from its pages, and save it into a single file. It can follow links within the same domain and allows for customization of the content extraction and output format.

Two interfaces are available:
*   A **Command-Line Interface (CLI)** using `wiki_scraper.py` for automation and advanced users.
*   A **Graphical User Interface (GUI)** using `gui_scraper.py` for ease of use.

Key Features (common to both interfaces):
*   **Web Crawling:** Starts from a specified URL and explores linked pages on the same domain.
*   **Content Extraction:** Extracts text from web pages. You can specify a CSS selector to target the main content area for more precise extraction.
*   **Configurable Output:**
    *   Supports output in plain text (`.txt`) or Markdown (`.md`) formats.
    *   Allows specifying the name of the output file.

## 2. General Installation

### Prerequisites
*   Python 3.6 or higher is recommended.
*   `pip` (Python package installer).

### Steps
1.  **Download the scripts:**
    *   Ensure you have `wiki_scraper.py` and (if using the GUI) `gui_scraper.py`.
    *   (If applicable, mention cloning the repository if it were in one, e.g., `git clone <repo_url>`)

2.  **Install required Python libraries:**
    *   Open your terminal or command prompt.
    *   Navigate to the directory where the scripts are located (if necessary).
    *   Run the following command to install `requests` (for web requests) and `beautifulsoup4` (for HTML parsing). These are needed for both the CLI and GUI versions.
        ```bash
        pip install requests beautifulsoup4
        ```
    *   The GUI version also uses Tkinter, which is part of Python's standard library, so no separate installation is usually needed for it.

## 3. Using the Command-Line Scraper (`wiki_scraper.py`)

The command-line script (`wiki_scraper.py`) is ideal for users who prefer to work in the terminal, need to automate scraping tasks, or want to integrate the scraper into other scripts.

### Command Syntax
```bash
python wiki_scraper.py <start_url> [options]
```

### Arguments and Options

*   **`start_url`** (Required)
    *   Description: The full starting URL of the wiki or website you want to scrape (e.g., "https://en.wikipedia.org/wiki/Main_Page").
    *   Must be a complete URL including `http://` or `https://`.

*   **`-o <filename>` / `--output <filename>`** (Optional)
    *   Description: Specifies the name for the output file.
    *   If you provide a name with an extension (e.g., `my_data.txt`), that will be used directly if the format matches.
    *   If you provide a name without an extension (e.g., `my_data`), the script will append the correct extension (`.txt` or `.md`) based on the chosen format.
    *   Default: `scraped_content` (which becomes `scraped_content.txt` or `scraped_content.md`).
    *   Example: `--output my_wiki_scrape`

*   **`-c <selector>` / `--selector <selector>`** (Optional)
    *   Description: A CSS selector that points to the main content area of the pages you are scraping. This helps in extracting only the relevant text and excluding headers, footers, navigation menus, etc.
    *   Default: `'body'` (extracts all text within the `<body>` tag, which can be very broad).
    *   Example: `--selector "#content"` or `--selector ".article-body"` or `--selector "article"`
    *   See Section 5: "Tips for Finding CSS Selectors" for more details.

*   **`--format <format>`** (Optional)
    *   Description: Specifies the output file format.
    *   Choices: `txt` (plain text), `md` (Markdown).
    *   Default: `txt`.
    *   Example: `--format md`

### CLI Examples

1.  **Basic Scrape (Text Output, default filename):**
    ```bash
    python wiki_scraper.py "https://en.wikipedia.org/wiki/Python_(programming_language)"
    ```
    *   This will scrape the given Wikipedia page and linked Wikipedia pages, saving the content to `scraped_content.txt`.

2.  **Scrape with Custom Output File and Markdown Format:**
    ```bash
    python wiki_scraper.py "https://example.com/wiki" -o "my_custom_output" --format md
    ```
    *   This will scrape `example.com/wiki`, save the content as `my_custom_output.md`.

3.  **Scrape with a Specific Content Selector:**
    ```bash
    python wiki_scraper.py "https://some-game-wiki.com/items" -c "#main-article-body" -o "game_items" --format md
    ```
    *   This targets content within the HTML element having the ID `main-article-body` (e.g., `<div id="main-article-body">...</div>`). Output will be `game_items.md`.

## 4. Using the GUI Scraper (`gui_scraper.py`)

The GUI scraper (`gui_scraper.py`) provides a user-friendly graphical interface for the same core scraping functionality.

### Launching the GUI
1.  Ensure you have completed the steps in Section 2: "General Installation".
2.  Open your terminal or command prompt.
3.  Navigate to the directory where the scripts are located.
4.  Run the following command:
    ```bash
    python gui_scraper.py
    ```
    This will launch the "Wiki Scraper Deluxe" application window.

### Interface Overview
The GUI window consists of the following components:

*   **Start URL field:**
    *   Purpose: Enter the full starting URL for the website or wiki you wish to scrape.
    *   Example: `https://en.wikipedia.org/wiki/Web_scraping`

*   **CSS Selector field:**
    *   Purpose: Optionally, enter a CSS selector to target the specific HTML element containing the main content on the pages. This helps to get cleaner text by excluding navigation, ads, footers, etc.
    *   Default: If left empty, it defaults to scraping the entire `<body>` of the pages.
    *   Hint: A small label below this field provides examples like `#main-content` or `article.body`.
    *   For detailed help on finding good selectors, refer to Section 5: "Tips for Finding CSS Selectors".

*   **Output Format:**
    *   Purpose: Choose the format for the saved file.
    *   Options:
        *   **TXT:** Plain text file (`.txt`).
        *   **MD:** Markdown file (`.md`), where paragraphs are separated by double newlines.

*   **Output File field & "Browse..." button:**
    *   Purpose: To specify where the scraped content will be saved.
    *   **"Browse..." button:** Click this button to open a "Save As" dialog. Here you can navigate to your desired directory, type a filename, and select the file type (which will often be pre-filtered by your "Output Format" choice).
    *   **Output File field:** This (read-only) field displays the full path to the file you selected or named via the "Browse..." dialog.
    *   **Important:** You must use "Browse..." to set an output file before starting the scrape.

*   **"START SCRAPING" button:**
    *   Purpose: Click this button to begin the web scraping process after you have filled in the URL and selected an output file.
    *   The button will be temporarily disabled while scraping is in progress.

*   **Status Area:**
    *   Purpose: A scrollable text box at the bottom of the window. It displays real-time messages about the scraper's progress, such as:
        *   The current URL being processed.
        *   Confirmation when scraping starts and finishes.
        *   The number of characters extracted.
        *   Error messages if any issues occur.

### Step-by-Step Usage Guide (GUI)
1.  **Launch the application:** Run `python gui_scraper.py` from your terminal.
2.  **Enter Start URL:** Type or paste the full URL of the website/wiki you want to scrape into the "Start URL" field.
3.  **Enter CSS Selector (Optional):** If you want to target specific content areas, enter the appropriate CSS selector in the "CSS Selector" field. If unsure, you can leave this blank to use the default (`body`).
4.  **Select Output Format:** Click either the "TXT" or "MD" radio button to choose your desired output file format.
5.  **Specify Output File:** Click the "Browse..." button. In the dialog that appears, choose a directory, enter a filename for your scraped content, and click "Save". The chosen path will appear in the field next to the button. **This step is mandatory.**
6.  **Start Scraping:** Click the "START SCRAPING" button.
7.  **Monitor Progress:** Observe the "Status Area" for updates on the scraping process. You'll see which URLs are being processed and any errors.
8.  **Completion:** Once the scraping is complete, a message will indicate this in the Status Area, and the content will be saved to the file you specified. The "START SCRAPING" button will become active again.

## 5. Tips for Finding CSS Selectors

To effectively use the `--selector` option (in CLI) or the "CSS Selector" field (in GUI), you need to find a CSS selector that accurately targets the main content of the wiki pages. Here's how:

1.  **Open Developer Tools:**
    *   In your web browser (Chrome, Firefox, Edge, etc.), navigate to one of the wiki pages you want to scrape.
    *   Right-click on the main content area of the page (e.g., the text of an article).
    *   Select "Inspect" or "Inspect Element" from the context menu. This will open the browser's developer tools, usually showing the HTML structure.

2.  **Identify the Content Container:**
    *   In the HTML view, hover over different elements. The browser will highlight the corresponding parts on the page.
    *   Look for an HTML element that encloses *all* the main content you want but *excludes* things like sidebars, headers, and footers.
    *   Common tags for main content include `<article>`, `<main>`, or `<div>` elements with specific IDs (e.g., `id="content"`, `id="main"`) or classes (e.g., `class="article-content"`, `class="wiki-body"`).

3.  **Determine the Selector:**
    *   **By ID:** If the element has a unique ID (e.g., `<div id="main-content">`), the selector is `#main-content`.
    *   **By Class:** If it has a distinctive class (e.g., `<article class="post-body">`), the selector could be `article.post-body` (for an article tag with that class) or just `.post-body` (if the class is unique enough). If the class name has spaces (e.g. `class="content main"`), you would use dots for each class: `.content.main`.
    *   **By Tag Name:** Sometimes, just the tag name like `article` or `main` is sufficient if there's only one such prominent tag.
    *   **Combined Selectors:** You can combine these for more specificity, e.g., `div#content .article-text`.

4.  **Test the Selector (Optional but Recommended):**
    *   In the developer tools' "Console" or "Elements" tab (varies by browser), you can often test CSS selectors. For example, in Chrome's console, you could type `document.querySelectorAll('#your-selector')` to see what elements it matches.

## 6. Basic Troubleshooting

These tips apply to both the CLI and GUI versions.

*   **No content extracted / Empty output file:**
    *   Check your CSS selector (if used). It might be too specific, incorrect, or the content structure might change between pages. Try a broader selector (like `article`, `main`, or even the default `body`) to see if any text is extracted.
    *   Verify the start URL is correct and accessible.
    *   The website might be heavily JavaScript-driven. This script primarily works with server-rendered HTML. Content loaded by JavaScript after the initial page load might not be captured.

*   **Few pages scraped / Crawl stops prematurely:**
    *   The wiki might have links that point outside the main domain/subdomain, and the scraper is designed to stay on the same domain as the `start_url`.
    *   Ensure the links within the wiki are standard `<a>` tags with `href` attributes.

*   **Access Denied / HTTP Errors (403, 503, etc.):**
    *   The website might have anti-scraping measures.
    *   Running the script too frequently might lead to your IP being temporarily blocked.
    *   Consider adding delays or using a custom User-Agent (features not yet in this script).

*   **Incorrect character encoding:**
    *   The script saves in UTF-8. If you see garbled characters, ensure the source website is also using a compatible encoding (most modern sites use UTF-8).

*   **GUI doesn't start (specific to `gui_scraper.py`):**
    *   Ensure Python and Tkinter are correctly installed. While Tkinter is standard, minimal Python installations might sometimes omit it (though rare).
    *   Check the terminal for any error messages when you try to run `python gui_scraper.py`.

---
If you encounter issues not covered here, please refer to the script's comments or seek further assistance if a support channel is available.
```
