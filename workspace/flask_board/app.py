from flask import Flask, jsonify, render_template

from db.connection import db_connect

app = Flask(__name__)
# 서버에 바로 수정사항이 반영되도록 옵션을 지정
app.debug = True

@app.route("/")
def index():
    return render_template("index.html")

# 로그인 페이지
@app.route("/login")
def view_login():
    return render_template("login.html")

# 게시판 페이지
@app.route("/board")
def view_board():
    SQL = """
        SELECT id, title, update_date
        FROM tb_board
        WHERE 1=1
        ORDER BY update_date
    """
    boards = []
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL)
            boards = cur.fetchall()
    return render_template("board.html", boards=boards)

# 게시판 상세 페이지
@app.route("/board/<int:board_id>")
def view_board_detail(board_id):
    SQL = """
        SELECT 
            id, 
            title, 
            content, 
            create_date, 
            update_date
        FROM tb_board
        WHERE id = %s
    """
    board = {}
    # 실습: 댓글도 가져오세요. 방법은 아무렇게나
    # 1. 여기서 쿼리를 한번 더 해서 댓글을 가져온다.
    # 2. API 라우터를 하나 만들어서 fetch()로 가져온다.
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL, board_id)
            # fetchone : 데이터가 반드시 한 건임을 보장한다.
            board = cur.fetchone() 
    return render_template("board_detail.html", board=board)

@app.route("/api/comment/<int:board_id>")
def get_board_comments(board_id):
    SQL = """
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
            cur.execute(SQL, board_id)
            comments = cur.fetchall()
    return jsonify(comments)        

if __name__ == "__main__":
    app.run()