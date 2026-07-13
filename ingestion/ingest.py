from pathlib import Path
from ingestion.pdf_reader import read_pdf
from ingestion.chunker import chunk_text
from embeddings.embedding import generate_embeddings
from database.db import insert_document

if __name__=="__main__":
    BASE_DIR=Path(__file__).resolve().parent.parent
    pdf_path=BASE_DIR/"documents"/"bellek.pdf"

    text=read_pdf(pdf_path)
    chunks=chunk_text(text)
    embeddings=generate_embeddings(chunks)

    filename=pdf_path.name

    for chunk,embedding in zip(chunks,embeddings):
        doc_id=insert_document(
            filename,
            chunk,
            embedding
        )
        

    print(f"File Name:{filename}")
