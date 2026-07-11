import psycopg 

DB_CONFIG={
    "host":'localhost',
    "port":5432,
    "dbname":"postgres",
    "user":"yigit",
    "password":"Yigitemre1801"
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)
