from pathlib import Path
from ingestion.pdf_reader import read_pdf_pages
from ingestion.chunker import chunk_text
from llm.embedding_client import generate_embeddings
from database.vectore_store import insert_document,document_exists
if __name__=="__main__":
    BASE_DIR=Path(__file__).resolve().parent.parent
    
    documents_dir=BASE_DIR / "documents"

    pdf_files=list(documents_dir.glob("*.pdf"))

    if not pdf_files:
        print("no pdf files found")
        exit()
    

    for pdf_path in pdf_files:
        
        filename=pdf_path.name
        if document_exists(filename):
            print(f"✅ {filename} already exists in database.")
            print("Skipping...\n")
            continue


        pages=read_pdf_pages(pdf_path)

        chunks=[]

        for page in pages:
            page_chunks=chunk_text(page["text"])

            for i,chunk in enumerate(page_chunks,start=1):
                chunks.append(
                    {
                        "page":page["page"],
                        "chunk_id":i,
                        "chunk":chunk,
                    }
                )

        embeddings=generate_embeddings(
            [c["chunk"] for c in chunks]
        )

        filename=pdf_path.name

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
                f"[Insertred document id={doc_id}"
            )
        
        print(f"\n{filename} uploaded to database")
        print(f"total chunks:{len(chunks)}")

