import sys
import pdfplumber

if len(sys.argv) < 3:
    print("Penggunaan: python search_pdf.py <path_to_pdf> <keyword1> [keyword2 ...]")
    sys.exit(1)

pdf_path, *keywords = sys.argv[1:]
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        for kw in keywords:
            if kw.lower() in text.lower():
                try:
                    line = next(l for l in text.splitlines() if kw.lower() in l.lower())
                    print(f"hlm. {i:>3} | {kw} | {line.strip()[:120]}")
                except StopIteration:
                    pass
