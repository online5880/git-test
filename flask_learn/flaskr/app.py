from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from db.db_connection import db_connect

USERNAME = 'test'
PASSWORD = '1234'

# 플라스크 사용
app = Flask(__name__)
app.config.from_object(__name__)

# 세션 사용을 위한 암호화 키
app.secret_key  = 't743fwylede84vrcadbt7jjikvzw1sra'
app.debug = True


# 리퀘스트가 실행되기 전에 호출되는 함수
# 예를를 들어 /user 라는 요청이 왔을 때
# 데이터베이스에 미리 커넥션을 해놓는다.
@app.before_request
def before_request():
    g.conn = db_connect()
    if g.conn:
        print('DB 연결 성공')
        
    print("나 DB 연결할꺼야.")


@app.after_request
def after_request(response):
    print("나 DB 연결했다.")
    return response


# /user 에서 라우터의 함수 실행이 끝난 후(요청에 대한 응답을 보내준 후)
# 데이터베이스의 연결을 종료한다.
@app.teardown_request
def teardown_request(exception):
    print("나 DB 연결 종료한다.")
    # g.conn.close()


@app.route("/")
def show_entries():
    SQL = """
            select title, text
            from entries
            order by id desc
    """

    entries = []
    with g.conn.cursor() as cur:
        cur.execute(SQL)
        entries = cur.fetchall()

    # HTML 을 만들어서 내려주는것
    return render_template('show_entries.html', entries=entries)


# method=POST 는 POST 요청만 받는다는 뜻이다.
# session 은 서버의 임시공간인데 주로 유저 정보를 저장한다.
# abort 는 요청에 대한 거절이다.


@app.route("/add", methods=["POST"])
def add_entry():
    if not session.get("logged_in"):
        abort(401)

    SQL = """
            INSERT INTO entries(
                title, text
            ) VALUES (
                %s, %s
            )
    """
    with g.conn.cursor() as cur:
        # request 는 유저의 요청에 대한 정보를 담고 있습니다.
        # request 내부에는 데이터를 저장하고 있는 form이란 객체가 있습니다.(POST)
        cur.execute(SQL, (request.form["title"], request.form["text"]))
    g.conn.commit()

    # 메시지 띄우는 용도
    flash("New entry was successfully posted!")
    # redirect 다른 화면으로 보내는 햄수
    # url_for 는 함수 이름으로 연결된 라우터를 찾는다.
    return redirect(url_for("show_entries"))


# GET, POST : GET과 POST요청을 다 받는다.
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    # POST 요청일 경우
    if request.method == "POST":
        # 유저의 요청 안에 유저명/비밀번호 체크
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid username"
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid password"
        else:
            # 로그인에 성공했으면
            # session : 임시 저장소에 logged_in 을 넣어준다.
            session["logged_in"] = True
            flash("You were logged in")
            # 함수명에 맞는 라우터로 요청을 다시 보낸다.
            return redirect(url_for("show_entries"))

    # 로그인 html 을 보여준다.
    return render_template("login.html", error=error)


# 로그아웃
@app.route("/logout")
def logout():
    # pop() 함수는 해당 키에 있는 데이터를 제거합니다.
    session.pop("logged_in", None)
    flash("You were logged out")
    # 함수명에 맞는 라우터로 요청을 보낸다.
    return redirect(url_for("show_entries"))


if __name__ == "__main__":
    app.run()
