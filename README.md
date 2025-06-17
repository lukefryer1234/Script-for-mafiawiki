# Script-for-mafiawiki

## Wiki Scraper Script

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
