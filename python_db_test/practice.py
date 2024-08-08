import pymysql
import pymysql.cursors


# DB 연결
def db_connect(db_name="dbtest"):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="test",
        password="1234",
        db=db_name,
        charset="utf8mb4",
        # 사용시 딕셔너리로 데이터가 반환됨.
        cursorclass=pymysql.cursors.DictCursor,
    )
    return conn


# SQL 실행
def exec_sql(SQL, args=None, insert=False):
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL, args)
            if insert:
                conn.commit()
                return "commit"
            result = cur.fetchall()
    return result


# select sql
select_board = "select * from tb_board"

select_user = """
            select *
            from tb_user;
"""
select_board_comment = """
                select *
                from tb_board_comment;
"""

select_id_3 = """
                select user_id, name, title, content
                from tb_board as board
                left join tb_user as user on user.id = board.user_id
                where user_id = 3;
"""

def get_user_by_id(id: int):
    pass

insert_post = """
                insert into 
                tb_board(title, content, user_id)
                values
                (%s, %s, %s)
                
"""

insert_post_gpt_comment = """
                insert into 
                tb_board_comment(board_id, user_id, COMMENT)
                values
                (%s, %s, %s)
                
"""

create_board = """
                create table 
                tb_python(
                    id bigint(20) not null auto_increment primary key,
                    title varchar(20) not null,
                    content varchar(200) not null,
                    user_id bigint(20) not null,
                    foreign key (user_id) references tb_user(id);
                )
"""
def update_board(title: str, content: str,id: int):
    pass


delete_board = """
                drop table
                tb_python;
"""


# 1. 유저 목록을 가져오는 프로그램을 작성해봅시다.
# result = exec_sql(select_user)

# 2. 게시판 데이터를 출력해봅시다.
# result = exec_sql(select_board_comment)

# 3. 유저의 식별자가 3인 데이터의 아이디, 이름, 작성한 게시판명, 내용을 출력해봅시다.
# result = exec_sql(select_id_3)

# 4. 2번 유저로 실제로 게시판에 글을 등록해봅시다.
user_count_sql = """
        SELECT
        count(u.id) AS user_count
        FROM
        tb_user u;
"""
# count = exec_sql(user_count_sql)
# user_count = count[0]["user_count"]
# import random as rd

# for i in range(1, 10000):
#     random_user = rd.randint(1, user_count)
#     random_board = rd.randint(1, 2)
#     random_comment = rd.randint(1, 100)
#     exec_sql(
#         insert_post_gpt_comment,
#         (random_board, random_user, f"이건 {random_comment}번째 댓글이다."),
#         insert=True,
#     )

result = exec_sql(insert_post, ("이건 999번문제 제목", "나는 내용999!", 2), insert=True)

# 5. 임의의 게시판 하나를 수정해봅시다.
# result = exec_sql(create_board)

# 6. 임의의 게시판 하나를 삭제해봅시다.
# result = exec_sql(delete_board)

# print(result)
