from flask import Flask

app = Flask(__name__)


# http://127.0.0.1:5000/ 뒤에 붙는 것
# 라우터 파라미터는 127.0.0.1:5000 뒤에 붙는 것
@app.route("/")
def index():
    return "Hello World!"


@app.route("/hello")
def hello_world2():
    return "hello 주소로 입력함"


@app.route("/hello/new")
def hello_world3():
    return "hello/new 주소로 입력함"


# 동적 라우팅
@app.route("/user/<user_name>/")
def hello_user_name(user_name):
    return f"Hello {user_name}"


# 동적 라우팅 타입 지정
# 자료형태를 정해줄 수 있다.
# 자료형태가 다르면 404(not found) 페이지로 이동함.
@app.route("/user/by_id/<int:user_id>")
def get_user_by_id(user_id: int):
    return f"유저 데이터를 받아왔습니다. {user_id}"


if __name__ == "__main__":
    app.run()
