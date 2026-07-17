from pathlib import Path
from ingestion.pdf_reader import read_pdf
from ingestion.chunker import chunk_text
from llm.embedding_client import generate_embeddings
from database.vectore_store import insert_document

if __name__=="__main__":
    BASE_DIR=Path(__file__).resolve().parent.parent
    pdf_path=BASE_DIR/"documents"/"bellek.pdf"

    text=read_pdf(pdf_path)
    chunks=chunk_text(text)
    embeddings=generate_embeddings(chunks)

    filename=pdf_path.name

    for i,(chunk,embedding) in enumerate(zip(chunks,embeddings),start=1):
        doc_id=insert_document(
            filename,
            chunk,
            embedding
        )

        print(f"[{i}/{len(chunks)}] inserted document id={doc_id}")

    print(f"\n {filename} uploaded database")
    print(f"total chunk:{len(chunks)}")
