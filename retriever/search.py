from database.db import get_connection
from llm.embedding_client import generate_embedding
from retriever.fusion import reciprocal_rank_fusion
import psycopg

def search_documents(query,filename=None,limit=10):

    try:

        query_embedding=generate_embedding(query)

        embedding_str="["+",".join(map(str,query_embedding))+"]"

        with get_connection() as conn:
              with conn.cursor() as cur:

                vector_results=vector_search(
                     cur,
                     embedding_str,
                     filename,
                     limit,
                )
                keyword_results=keyword_search(
                     cur,
                     query,
                     filename,
                     limit,
                )

        print("\n" + "=" * 70)
        print("VECTOR RESULTS")
        print("=" * 70)

        for r in vector_results:
            print(f"{r[1]} | Sayfa {r[2]} | Distance: {r[5]:.4f}")

        print("\n" + "=" * 70)
        print("KEYWORD RESULTS")
        print("=" * 70)

        for r in keyword_results:
            print(f"{r[1]} | Sayfa {r[2]} | Score: {r[5]:.4f}")


        results=reciprocal_rank_fusion(
                 vector_results,keyword_results
            )

        print("\n" + "=" * 70)
        print("RRF RESULTS")
        print("=" * 70)

        for r in results:
            print(f"{r[1]} | Sayfa {r[2]}")

        seen=set()
        filtered=[]

        for row in results:
             key=(row[1],row[2]) #filename+page
             if row[0] not in seen:
                  filtered.append(row)
                  seen.add(key)
                  
        return filtered[:limit]

    except psycopg.Error as e:
         print(f"[Databse Error]{e}")
         raise
    except Exception as e:
         print(f"['Search Error] {e}")
         raise
          



def vector_search(cur,embedding_str,filename,limit):

        if filename:

            cur.execute("""
                    select
                        id,
                        filename,
                        page,
                        chunk_index,
                        chunk,
                        embedding <=> %s::vector as distance
                    from documents
                    where filename=%s
                    order by embedding <=> %s::vector
                    limit %s
                """, (
                         embedding_str,
                         filename,
                         embedding_str,
                         limit,
                        ),
                )
        else:

            cur.execute("""
                    select
                        id,
                        filename,
                        page,
                        chunk_index,
                        chunk,
                        embedding <=> %s::vector as distance
                    from documents 
                    order by embedding <=> %s::vector
                    limit %s
                """,
                (
                    embedding_str,
                    embedding_str,
                    limit,
                ),
                )

        return cur.fetchall()

def keyword_search(cur,query,filename,limit):

        if filename:
             cur.execute("""
                    select
                        id,
                        filename,
                        page,
                        chunk_index,
                        chunk,
                        ts_rank(search_vector,plainto_tsquery('simple',%s)) as score
                    from documents
                    where filename=%s
                    order by score desc
                    limit %s
                    """,
                    (
                      query,
                      filename,
                      limit,   
                    ),
                )
        else:
             cur.execute("""
                    select
                        id,
                        filename,
                        page,
                        chunk_index,
                        chunk,
                        ts_rank(search_vector,plainto_tsquery('simple',%s)) as score
                    from documents
                    order by score desc
                    limit %s
                    """,
                    (
                        query,
                        limit, 
                    ),
                )

        return cur.fetchall()



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