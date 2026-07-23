from typing import List
from database.db import get_connection

def insert_document(
        filename:str,
        page:int,
        chunk_index:int,
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
                (filename,page,chunk_index,chunk,embedding)

                values (%s,%s,%s,%s,%s)

                returning id;
                """,
                (
                    filename,
                    page,
                    chunk_index,
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
                page,
                chunk_index,
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


def document_exists(filename:str)->bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select exists(
                select 1 
                from documents
                where filename=%s                
                )
                """,
                (filename,),
            )
            return cur.fetchone()[0]


def get_documents():

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    select distinct filename
                    from documents
                    order by filename;
                """)

            return [row[0] for row in cur.fetchall()]

if __name__=="__main__":
    print("vector store ready")
