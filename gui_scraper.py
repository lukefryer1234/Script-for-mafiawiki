import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
from wiki_scraper import crawl_wiki, save_content_to_file
# Note: If wiki_scraper.py's core logic (crawl_wiki, save_content_to_file)
# is inside its own if __name__ == '__main__': block, this import won't work as expected.
# Assuming they are defined at the top level or otherwise importable.

class ScraperApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Wiki Scraper Deluxe")
        self.root.geometry("600x500") # Initial size

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure grid column weights for main_frame to allow expansion
        main_frame.columnconfigure(1, weight=1) # Column with entries and status area

        # --- Row 0: URL Input ---
        self.url_label = ttk.Label(main_frame, text="Start URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(main_frame, width=60) # Increased width
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # --- Row 1: CSS Selector Input ---
        self.selector_label = ttk.Label(main_frame, text="CSS Selector:")
        self.selector_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.selector_entry = ttk.Entry(main_frame)
        self.selector_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.selector_hint_label = ttk.Label(main_frame, text="(Optional: e.g., #main-content, article.body)")
        self.selector_hint_label.grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky="w")

        # --- Row 3: Output Format Selection ---
        self.format_label = ttk.Label(main_frame, text="Output Format:")
        self.format_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.output_format_var = tk.StringVar(value="txt")
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        self.txt_radio = ttk.Radiobutton(format_frame, text="TXT", variable=self.output_format_var, value="txt")
        self.txt_radio.pack(side=tk.LEFT, padx=5)
        self.md_radio = ttk.Radiobutton(format_frame, text="MD", variable=self.output_format_var, value="md")
        self.md_radio.pack(side=tk.LEFT, padx=5)

        # --- Row 4: Output File Path ---
        self.output_file_label = ttk.Label(main_frame, text="Output File:")
        self.output_file_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.output_file_var = tk.StringVar()
        self.output_file_entry = ttk.Entry(main_frame, textvariable=self.output_file_var, state="readonly")
        self.output_file_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.browse_button = ttk.Button(main_frame, text="Browse...")
        self.browse_button.grid(row=4, column=2, padx=5, pady=5, sticky="e")

        # --- Row 5: Start Button ---
        self.start_button = ttk.Button(main_frame, text="START SCRAPING")
        self.start_button.grid(row=5, column=0, columnspan=3, padx=5, pady=10, sticky="ew")

        # --- Row 6: Status Area ---
        self.status_label = ttk.Label(main_frame, text="Status:")
        self.status_label.grid(row=6, column=0, padx=5, pady=5, sticky="nw") # North-west for label

        self.status_area = scrolledtext.ScrolledText(main_frame, height=10, state="disabled", wrap=tk.WORD)
        self.status_area.grid(row=6, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Configure row weight for status area to expand vertically
        main_frame.rowconfigure(6, weight=1)

        # Link button commands
        self.browse_button.config(command=self.browse_output_file)
        self.start_button.config(command=self.start_scraping_thread)

        self.scraped_content_to_save = None # To store content from thread

        self.update_status("Ready. Fill in the details and click 'Browse...' to select an output file.")

    def update_status(self, message):
        # Ensure GUI updates are done in the main thread
        self.root.after(0, self._do_update_status, message)

    def _do_update_status(self, message):
        self.status_area.configure(state="normal")
        self.status_area.insert(tk.END, message + "\n")
        self.status_area.configure(state="disabled")
        self.status_area.see(tk.END) # Scroll to the end

    def browse_output_file(self):
        current_format = self.output_format_var.get()
        if current_format == "txt":
            default_ext = ".txt"
            file_types = [("Text files", "*.txt"), ("All files", "*.*")]
        elif current_format == "md":
            default_ext = ".md"
            file_types = [("Markdown files", "*.md"), ("All files", "*.*")]
        else:
            default_ext = ""
            file_types = [("All files", "*.*")]

        filename = filedialog.asksaveasfilename(
            defaultextension=default_ext,
            filetypes=file_types,
            title="Save As..."
        )
        if filename:
            self.output_file_var.set(filename)
            self.update_status(f"Output file set to: {filename}")

    def start_scraping_thread(self):
        url = self.url_entry.get().strip()
        selector = self.selector_entry.get().strip()
        if not selector: # Default to 'body' if empty
            selector = 'body'
        output_format = self.output_format_var.get() # Not directly used by crawl_wiki, but good to have
        output_filepath = self.output_file_var.get().strip()

        if not url:
            self.update_status("Error: Start URL cannot be empty.")
            return
        if not output_filepath:
            self.update_status("Error: Output file path must be set via 'Browse...'.")
            return

        self.start_button.config(state="disabled")
        self.update_status(f"Starting scraping for: {url} with selector: '{selector}'")
        self.scraped_content_to_save = None # Reset previous content

        thread = threading.Thread(
            target=self._execute_scraping,
            args=(url, selector, output_filepath, output_format) # output_format passed for completeness
        )
        thread.daemon = True
        thread.start()

    def _execute_scraping(self, url, selector, output_filepath, output_format):
        try:
            # Initial message before detailed callbacks start
            self.update_status(f"Initiating crawl for: {url} with selector '{selector}'...")
            consolidated_text = crawl_wiki(url, selector, status_callback=self.update_status)
            self.scraped_content_to_save = consolidated_text # Store for saving

            # The actual save_content_to_file will be called in the next step
            # For now, we confirm content is ready.
            if self.scraped_content_to_save is not None:
                 self.update_status(f"Scraping finished. {len(self.scraped_content_to_save)} characters found.")
                 self.update_status(f"Content ready to be saved to: {output_filepath}")
                 # Simulate saving for now, actual saving in next step.
                 save_content_to_file(self.scraped_content_to_save, output_filepath)
                 self.update_status(f"Content successfully saved to {output_filepath}")

            else:
                self.update_status("Scraping completed, but no content was extracted.")

        except Exception as e:
            self.update_status(f"Error during scraping: {e}")
        finally:
            # Re-enable the start button in the main thread
            self.root.after(0, lambda: self.start_button.config(state="normal"))

if __name__ == '__main__':
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
