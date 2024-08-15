# 크롤러
- 웹 전체, 방대하다
- 링크, 요소, 메타데이터
- **중복제거는 필수적**
- **데이터 정제 필수**
---

# 스크랩퍼
- 특정 웹 페이지, 적은 편
- 콘텐츠가 중요
- 중복 O
- 의사결정에 사용될 수 있도록 정제
  

---
# 시험

# 웹
- 네트워크가 거미줄처럼 이어져있는 것
- 서로 연결되 네트워크 모음
- 서버, 클라이언트 관계
  - 클라 > 서버 = request
    - get, post, put, delete
    - get <-> post 의 차이
      - get -> URL : URL에 파라미터를 붙여 요청. 주로 조회할 때 사용
      - post -> body 에 넣어야함 : 데이터를 생성하거나 서버에 상태를 변경할 때 사용
  - 서버 > 클라 = response
    - status(상태 코드)
      - 200(성공), 400(유저,클라이언트), 500(서버)
      - body
        - json 또는 html 또는 텍스트
- api
- 세션
  - 유저의 상태를 담고 있는 것
  
# flask
- @ decorator: 함수에 대한 라벨, 함수를 제어하는 함수
  - app.route('/') <-- 해당 url를 받아서 실행해줌 -> render_template
- 특징
  - 가볍다. 경량
  - 확장성이 좋다.
  - 스타트업이나 새로운 기능에 많이 사용한다.
  - 경량형 웹 프레임워크
  - 장점이자 단점. -> 사수를 잘 만나야함

# django
- 기업용 웹 프레임워크 (무겁다)
- 기업용 올인원 패키지
- MVT
  - Model
    - 비지니스 로직을 가지는 
  - View
    - 모델과 템플릿을 연결해줌
    - 데이터 <----> UI 연결
  - Template
    - 실제 UI
- ORM(Object-Relational Mapping)
  - 객체(model, Object)
  - 관계(Database)
- 명령어
  - startproject
  - createapp
  - runserver
  - makemigrations
  - migrate
- 중요 파일
  - settings.py
    - 장고의 세팅값들을 입력. DB 같은거
  - urls.py
    - url을 파싱해서 뷰에 보내줌
  - views.py
    - 뷰를 연결해주는 것
  - admin.py
    - 관리자 페이지
  - templates.py
    - html 파일

# 프레임워크와 라이브러리의 차이
- 라이브러리
  - 개발자가 가져다가 써야함.
  - 초점이 코드. 내가 작성해야 함.
- 프레임워크
  - 이미 모두 설치되어있음. 확장은 가능
  - 개발 방법이 정의되어 있음
  - 초점이 이놈이다

# html, css, js
- html : 뼈
- css : 피부
- js : 움직임