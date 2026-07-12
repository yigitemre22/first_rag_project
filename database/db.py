import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_HOST=os.getenv("DB_HOST")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_PORT=os.getenv("DB_PORT")

def get_connection()->psycopg.Connection:
    try:
        conn=psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        return conn
    
    except Exception as e:
        print(f"database connection error: {e}")
        raise

def insert_document(
    filename:str,
    chunk:str,
    embedding:list[float]
    )->int:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    embedding_str=str(embedding)
                    cur.execute("insert into documents (filename,chunk,embedding)" \
                    " values (%s,%s,%s) Returning id;",
                    (filename,
                    chunk,
                    embedding_str))
                    doc_id=cur.fetchone()[0]
                    conn.commit()
                    return doc_id
        
        except Exception as e:
             print(f"document insert error: {e}")
             raise
        
if __name__=="__main__":
    conn = get_connection()
    print("Veritabanına başarıyla bağlanıldı.")
    conn.close()