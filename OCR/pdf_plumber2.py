import pdfplumber

with pdfplumber.open("sample of interview skills.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f" ----------------------------------- Page {i+1} -----------------------------------\n{text}")

