from database.db import get_connection
from llm.embedding_client import generate_embedding
import psycopg

def search_documents(
        query:str,
        filename:str |  None=None,
        limit:int=10,
                ):

    try:
        query_embedding=generate_embedding(query)

        embedding_str="["+",".join(map(str,query_embedding))+"]"

        with get_connection() as conn:
            with conn.cursor() as cur:
                if filename:
                    cur.execute(
                        """
                        select
                        id,
                        filename,
                        page,
                        chunk_index,
                        chunk,
                        (
                            (embedding <=> %s::vector) *0.7
                            +
                            (1- ts_rank(search_vector,plainto_tsquery('simple',%s)))*0.3 )
                            as distance
                        from documents
                        where filename =%s
                        order by distance
                        limit %s;
                        """,
                        (
                          embedding_str,
                          query,
                          filename,
                          limit,
                        ),
                    )
                else:
                    cur.execute(
                        """
                        select 
                            id,
                            filename,
                            page,
                            chunk_index,
                            chunk,
                            (

                                (embedding <=> %s::vector ) *0.7
                                +
                                (1- ts_rank(search_vector,plainto_tsquery('simple',%s)))*0.3)
                                as distance
                        from documents
                        order by distance
                        limit %s;
                        """,
                    (
                        embedding_str,
                        query,
                        limit,
                    ),
                    )
                print("Searching in:", filename)
                results= cur.fetchall()

                for row in results:
                    print(f"{row[1]} | Sayfa {row[2]} | Distance: {row[5]:.4f}")

                return results

    except psycopg.Error as e:
        print(f"[Databese Error] {e}")
        raise

    except Exception as e:
        print(f"[Search error] {e}")
        raise

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