from llm.embedding_client import generate_embeddings
from database.db import get_connection

def search_documents(
        query:str,
        top_k:int=5
        ) ->list[tuple[str,str]]:
    
    query_embedding=str(generate_embeddings([query])[0])
    with get_connection() as conn:
        with conn.cursor()  as cur:
            cur.execute(
                "select filename, " \
                "chunk, " \
                "embedding <=> %s::vector as distance " \
                "from documents " \
                "order by distance " \
                "limit %s",
                (query_embedding,top_k)
            )
            results=cur.fetchall()
            return results

def build_context(
        documents:list[tuple[str,str]]
                )->str:
    context=[]
    for filename,chunk in documents:
        context.append(
            f"[Source:{filename}]\n{chunk}"
        )
    return "\n\n".join(context)

if __name__=="__main__":
    results=search_documents("sanal bellek nedir")

    for result in results:
        print(result)