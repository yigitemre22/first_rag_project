from connection import get_connection

try:
    conn=get_connection()
    print("bağlantı sağlandı")

    cur=conn.cursor()
    cur.execute("select version();")

    print(cur.fetchone())
    
    cur.close()
    conn.close()

except Exception as e:
    print(f"hata:{e}")
