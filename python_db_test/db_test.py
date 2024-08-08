import pymysql
import pymysql.cursors


# DB 연결
def db_connect():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="test",
        password="1234",
        db="dbtest",
        charset="utf8mb4",
        # 사용시 딕셔너리로 데이터가 반환됨.
        cursorclass=pymysql.cursors.DictCursor,
    )
    return conn


# SQL 실행
SQL = "select * from tb_board"

with db_connect() as conn:
    with conn.cursor() as cur:
        cur.execute(SQL)
        result = cur.fetchall()
        print(result)
