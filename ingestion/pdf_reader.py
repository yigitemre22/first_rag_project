import fitz
from pathlib import Path

def read_pdf(pdf_path: Path) -> str:
    pages = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            pages.append(page.get_text())

    return "\n\n".join(pages)


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    pdf_path = BASE_DIR / "documents" / "bellek.pdf"

    text = read_pdf(pdf_path)
    print(text[:500])