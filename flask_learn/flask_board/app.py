from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from db.db_connection import db_connect

# 인스턴스 생성, 초기화
app = Flask(__name__)
app.secret_key = "YTl1kmHED9CLrH9lzHkM77hEZgFbP3FM"
# 서버에 바로 수정사항이 반영되도록 옵션을 지정
app.debug = True


# 첫 페이지
@app.route("/")
def index():
    return render_template("index.html")


# 로그인 페이지
@app.route("/login", methods=["GET", "POST"])
def login():
    SQL = """
        select 
            *
        from
            tb_user
        where
            1=1
        and login_id = %s
        and login_password = %s
    """

    error_message = None

    if request.method == "POST":
        login_id = request.form["login_id"]
        login_password = request.form["login_password"]
        with db_connect() as conn:
            with conn.cursor() as cur:
                cur.execute(SQL, [login_id, login_password])
                user = cur.fetchone()
                if user != None and len(user) > 0:
                    session["user"] = user
                    return redirect(url_for("index"))
                else:
                    error_message = "유저가 존재하지 않습니다."

    return render_template("login.html", error_message=error_message)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


# 게시판 페이지
@app.route("/board")
def view_board():
    SQL = """
            select id, title, update_date
            from tb_board
            where 1=1
            order by update_date desc
    """
    boards = []
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL)
            boards = cur.fetchall()
    return render_template("board.html", boards=boards)


@app.route("/board/new", methods=["GET"])
def view_insert_board():
    return render_template("insert_board.html")


@app.route("/board/new", methods=["POST"])
def insert_board():
    SQL = """
            insert into
            tb_board(
                title, content,user_id
            )
            values (
                %s,%s,%s
            )
        """
    if not session["user"]:
        return redirect(url_for("login"))

    user_id = session["user"].get("id")
    title = request.form["title"]
    content = request.form["content"]

    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL, [title, content, user_id])
            conn.commit()
            return redirect(url_for("view_board"))


# 게시판 상세 페이지
@app.route("/board/<int:board_id>")
def view_board_detail(board_id):
    board_SQL = """
            select 
                board.id,
                board.title,
                board.content,
                board.user_id,
                board.create_date,
                board.update_date,
                user.name
            from 
                tb_board as board
            inner join tb_user user on board.user_id = user.id
            where board.id = %s
    """
    board = {}

    # 실습 : 댓글이 필요해. 단, 방법은 상관없음
    # 1. 쿼리 한 번더
    # 2. api용 라우터를 하나 만들어서 fetch()로 가져온다
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(board_SQL, (board_id, ))
            # fetchone : 데이터가 반드시 1건임을 보장한다.
            board = cur.fetchone()
    return render_template("board_detail.html", board=board)


@app.route("/board/update/<int:board_id>", methods=["GET"])
def view_update_board(board_id: int):
    SQL = f"""
            select id, title, content
            from tb_board
            where  id = {board_id}
    """
    board = []
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL)
            board = cur.fetchone()

    return render_template("update_board.html", board=board)


@app.route("/board/update", methods=["POST"])
def update_board():
    SQL = """
            update
                tb_board 
            set
                title = %s,
                content = %s,
                update_date = NOW()
            where 
                id = %s
    """
    title = request.form["title"]
    content = request.form["content"]
    board_id = request.form["board_id"]
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL, [title, content, board_id])
            conn.commit()
            return redirect(url_for("view_board_detail", board_id=board_id))


# ! ################################################################################ 댓글 추가
@app.route("/board/<int:board_id>/add_comment", methods=["POST"])
def add_comment(board_id: int):
    SQL = """
            insert into 
            tb_board_comment(
                board_id, user_id, comment, create_date, update_date
            )
            values(
                %s, %s, %s,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
            );
    """
    with db_connect() as conn:
        comment_text = request.form["comment"]
        user_id = session["user"].get("id")
        with conn.cursor() as cur:
            cur.execute(SQL, [board_id, user_id, comment_text])
            conn.commit()
            return redirect(url_for("view_board_detail", board_id=board_id))


# ! ################################################################################## 댓글 추가


@app.route("/api/board/<int:board_id>")
def delete_board(board_id: int):
    SQL = """
            delete from
                tb_board board
            where
                board.id = %s
    """
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL, board_id)

    return render_template("index.html")


@app.route("/api/comment/<int:board_id>")
def get_board_comments(board_id):
    comment_SQL = """
        SELECT 
            user.name, comment.id, 
            comment.comment, comment.update_date
        FROM 
            tb_board_comment comment
            INNER JOIN tb_user user 
                ON comment.user_id = user.id
        WHERE 1=1
            AND comment.board_id = %s

    """
    comments = []
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(comment_SQL, (board_id, ))
            comments = cur.fetchall()
    return jsonify(comments)


if __name__ == "__main__":
    app.run()
