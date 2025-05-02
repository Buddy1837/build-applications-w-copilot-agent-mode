import pdfplumber

with pdfplumber.open("gpt-4-system-card.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f" ----------------------------------- Page {i+1} -----------------------------------\n{text}")
