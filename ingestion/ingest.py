from pathlib import Path
from ingestion.pdf_reader import read_pdf_pages
from ingestion.chunker import chunk_text
from llm.embedding_client import generate_embeddings
from database.vectore_store import insert_document,document_exists


def ingest_pdf(pdf_path:Path):

    filename=pdf_path.name

    if document_exists(filename):
        print(f"{filename} already exist")
        return

    pages=read_pdf_pages(pdf_path)

    chunks=[]

    for page in pages:
        page_chunks=chunk_text(page["text"])

        for i,chunk in enumerate(page_chunks,start=1):

            chunks.append({
                "page":page["page"],
                "chunk_id":i,
                "chunk":chunk,
            })

    embeddings=generate_embeddings(
            [c["chunk"] for c in chunks]
        )

    for info,embedding in zip(chunks,embeddings):

            doc_id=insert_document(
                filename,
                info["page"],
                info["chunk_id"],
                info["chunk"],
                embedding,
            )

            print(
                f"[Page {info['page']}]"
                f"[Chunk {info['chunk_id']}]"
                f"[Inserted document id={doc_id}]"
            )

    print(f"\n {filename} uploaded.")
    print(f"Total chunks:{len(chunks)}")


def ingest_all():
    BASE_DIR=Path(__file__).resolve().parent.parent

    documents_dir=BASE_DIR / "documents"

    pdf_files=list(documents_dir.glob("*.pdf"))

    if not pdf_files:
        print("no pdf files found")
        return

    for pdf in pdf_files:
        ingest_pdf(pdf)


if __name__=="__main__":
    ingest_all()