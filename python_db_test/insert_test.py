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


# SQL - Insert 실행
SQL = "insert into \
tb_board(title, content, user_id) \
values \
(%s,%s,%s)\
"

with db_connect() as conn:
    with conn.cursor() as cur:
        board = ("이건 파이썬에서 작성한 제목이야", "이건 콘텐츠야", 3)
        cur.execute(SQL, board)
        conn.commit()
