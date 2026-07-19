from pathlib import Path
from ingestion.pdf_reader import read_pdf_pages
from ingestion.chunker import chunk_text
from llm.embedding_client import generate_embeddings
from database.vectore_store import insert_document

if __name__=="__main__":
    BASE_DIR=Path(__file__).resolve().parent.parent
    pdf_path=BASE_DIR/"documents"/"bellek.pdf"

    pages=read_pdf_pages(pdf_path)

    chunks=chunk_text(pages)

    embeddings=generate_embeddings(
        [c["chunk"] for c in chunks]
    )
    
    filename=pdf_path.name

    for chunk_info,embedding in zip(chunks,embeddings):

        doc_id=insert_document(
            filename=filename,
            page=chunk_info["page"],
            chunk_index=chunk_info["chunk_index"],
            chunk=chunk_info["chunk"],
            embedding=embedding,
        )

        print(
            f"[Page {chunk_info['page']}]"
            f"[Chunk{chunk_info['chunk_index']}]"
            f"Inserted document id={doc_id}"
        )
    
    print(f"\n{filename} uploaded to databese")
    print(f"Total chunks:{len(chunks)}")

