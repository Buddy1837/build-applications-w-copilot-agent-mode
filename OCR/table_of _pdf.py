
import pdfplumber
import warnings
warnings.filterwarnings("ignore", message="CropBox missing from /Page, defaulting to MediaBox")


with pdfplumber.open("smp.pdf") as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables({
        "vertical_strategy": "lines",    # Try "text" or "lines"
        "horizontal_strategy": "lines",  # Or try "text"
        "intersection_tolerance": 5      # Adjust if needed
    })

    for i, table in enumerate(tables):
        if tables:
            print(f"--- Table {i+1} ---")
            for table in tables:  # Iterate over each table
                for row in table:  # Iterate over rows in the table
                    print(row)
        else:
            print("No table found on the page.")
        print("\n")