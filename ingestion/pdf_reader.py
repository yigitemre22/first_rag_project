import fitz
from pathlib import Path

def read_pdf(pdf_path: Path) -> str:
    pages = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            pages.append(page.get_text())

    return "\n\n".join(pages)


def read_pdf_pages(pdf_path:Path):
    pages=[]

    with fitz.open(pdf_path) as doc:
        for page_number,page in enumerate(doc,start=1):
            pages.append(
                {
                    "page":page_number,
                    "text":page.get_text(),
                }
            )
        
        return pages

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    pdf_path = BASE_DIR / "documents" / "bellek.pdf"

    pages=read_pdf_pages(pdf_path)
    print(pages[0])