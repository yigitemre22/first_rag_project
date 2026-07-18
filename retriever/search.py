from database.db import get_connection
from llm.embedding_client import generate_embedding

def search_documents(
        query:str,
        limit:int=5,
                ):
    
    query_embedding=generate_embedding(query)

    embedding_str="["+",".join(map(str,query_embedding))+"]"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select
                id,
                filename,
                chunk,
                embedding <=> %s::vector as distance

                from documents
                
                order by embedding <=> %s::vector

                limit %s;
                """,
                (
                    embedding_str,
                    embedding_str,
                    limit
                )
            )
            return cur.fetchall()

if __name__=="__main__":
    results=search_documents("bellek nedir")

    for row in results:
        print("="*50)
        print(f"ID:       {row[0]}")
        print(f"File:     {row[1]}")
        print(f"Distance: {row[3]:.4f}")
        print()
        print(row[2][:300])
        print()