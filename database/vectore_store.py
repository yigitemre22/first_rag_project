from typing import List
from database.db import get_connection

def insert_document(
        filename:str,
        chunk:str,
        embedding:List[float],
        )->int:
    """add a new document in database"""

    embedding_str="["+",".join(map(str,embedding))+"]"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into documents
                (filename,chunk,embedding)

                values (%s,%s,%s)

                returning id;
                """,
                (
                    filename,
                    chunk,
                    embedding_str,
                ),
            )
            document_id=cur.fetchone()[0]

        conn.commit()
    return document_id

def get_document(document_id:int):

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                select
                id,
                filename,
                chunk,
                created_at
                from documents
                where id=%s
                """,
                (document_id,),
            )
            return cur.fetchone()

def delete_document(document_id:int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        delete from documents
                        where id=%s
                        """,
                        (document_id,),
                        )
            conn.commit()

def clear_documents():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("delete from documents")
        conn.commit()


if __name__=="__main__":
    print("vector store ready")
