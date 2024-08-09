import pymysql
import pymysql.cursors
from db.db_config import HOST, PORT, USER, PASSWORD 

def db_connect():
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        db="test_db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn
