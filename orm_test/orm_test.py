import pymysql
from sqlalchemy import create_engine,select
from sqlalchemy.orm import Session
import db_config as dbc
from model import User

# mysql db 와 호환하기 위해 아래 함수를 호출  q
pymysql.install_as_MySQLdb()
engine = create_engine(f"mariadb+pymysql://{dbc.USER}:{dbc.PASSWORD}@{dbc.HOST}:{dbc.PORT}/{dbc.DB}?charset=utf8mb4")
session = Session(engine)

# 실제 orm 작성법
# 이 문장은 Database Statement 를 반환한다. => 쿼리정보
stmt = select(User).where(User.login_id == 'user4')    

print('a')

# fetchall() 이랑 같은 함수
users = session.scalar(stmt)
for user in users:
    print(user.id,user.login_id,user.login_password)