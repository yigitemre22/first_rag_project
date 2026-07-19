from database.db import get_connection
from llm.embedding_client import generate_embedding

def search_documents(
        query:str,
        limit:int=15,
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
                page,
                chunk_index,
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
            results= cur.fetchall()

            for row in results:
                print("="*50)
                print(f"Page:{row[2]}")
                print(row[4][:500])
                print()
            return results
            

if __name__=="__main__":
    results=search_documents("bellek nedir")

    for row in results:
        print("="*60)
        print(f"ID:       {row[0]}")
        print(f"File:     {row[1]}")
        print(f"Page:     {row[2]}")
        print(f"Chunk:    {row[3]}")
        print(f"Distance: {row[5]:.4f}")
        print()
        print(row[4][:300])
        print()