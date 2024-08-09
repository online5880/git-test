import pymysql
import pymysql.cursors
import db.db_config as dbc


# DB 연결
def db_connect():
    conn = pymysql.connect(
        host=dbc.HOST,
        user=dbc.USER,
        passwd=dbc.PASSWORD,
        db=dbc.DB,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    return conn

