# Script-for-mafiawiki

This repository contains tools for scraping websites. Two versions are available:
- A command-line script (`wiki_scraper.py`) for versatile, automatable scraping.
- A graphical user interface (`gui_scraper.py`) for easier interactive use.

## Wiki Scraper Script (`wiki_scraper.py`)

### Purpose
The `wiki_scraper.py` script is a command-line tool designed to crawl and scrape text content from a website. It starts from a specified URL, follows hyperlinks that lead to pages within the same domain, extracts textual content from these pages, and consolidates it into a single output file.

### Prerequisites
To run the `wiki_scraper.py` script, you need Python 3 and the following Python libraries:

- `requests`: For making HTTP requests to fetch web pages.
- `beautifulsoup4`: For parsing HTML content and extracting data.

You can install these libraries using pip:
```bash
pip install requests beautifulsoup4
```

### Usage
You can run the script from your command line interface.

**Command Structure:**
```bash
python wiki_scraper.py <start_url> [options]
```

**Arguments:**

-   `<start_url>`: (Mandatory) The full URL of the initial page from which the scraper will begin crawling. This URL must be enclosed in quotes if it contains special characters.
-   `-o <filename>`, `--output <filename>`: (Optional) Specifies the name for the output file where the scraped text content will be saved. If not provided, the script will use a default filename, `scraped_content.txt`.

**Example Command:**
To scrape a wiki starting at `https://en.wikipedia.org/wiki/Web_scraping` and save the output to `wiki_scraping_content.txt`:
```bash
python wiki_scraper.py "https://en.wikipedia.org/wiki/Web_scraping" -o "wiki_scraping_content.txt"
```

## GUI Scraper (`gui_scraper.py`)

### Purpose
The `gui_scraper.py` script provides a graphical user interface (GUI) for the wiki scraping functionality. This makes the scraper more accessible and easier to use for those who prefer a visual interface over a command-line tool.

### Prerequisites
*   **Tkinter:** The GUI is built using Tkinter, which is part of Python's standard library. No additional installation is typically required for Tkinter itself.
*   **Core Scraper Libraries:** Since the GUI uses the underlying logic from `wiki_scraper.py`, the same prerequisites apply:
    ```bash
    pip install requests beautifulsoup4
    ```

### How to Run
1.  Ensure you have installed the prerequisites mentioned above.
2.  Run the script from your terminal or command prompt:
    ```bash
    python gui_scraper.py
    ```
3.  The application window will open, presenting the following:
    *   **Start URL field:** For entering the initial URL to scrape.
    *   **CSS Selector field:** An optional field to specify a CSS selector for targeting main content areas (e.g., `#content`, `article.body`). Defaults to `body` if left empty.
    *   **Output Format:** Radio buttons to choose between "TXT" (plain text) and "MD" (Markdown) for the output file.
    *   **Output File field & Browse button:** A field to display the chosen output file path and a "Browse..." button to open a file dialog for selecting where to save the scraped content.
    *   **START SCRAPING button:** To initiate the scraping process.
    *   **Status Area:** A text box that displays real-time status updates, progress messages, and any errors encountered.

### Relationship to `wiki_scraper.py`
The `gui_scraper.py` application is a front-end for the core scraping engine provided by `wiki_scraper.py`. It imports and utilizes functions like `crawl_wiki` and `save_content_to_file` from the command-line script to perform the actual web crawling and data processing.
