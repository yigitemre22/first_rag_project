import os
import psycopg
from psycopg import Connection
from dotenv import load_dotenv

load_dotenv()



def get_connection()->Connection:
   """
    crate postgresql connection 
   """
   return psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )

        
if __name__=="__main__":
    try:
      with get_connection() as conn:
        print("database connection succesful")
    except Exception as e:
      print(e)