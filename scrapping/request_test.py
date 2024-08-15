import requests
from bs4 import BeautifulSoup

BOOKS_URL = "http://127.0.0.1:8000/catalog/books"

# session 을 가져온다.
with requests.Session() as session:
    form = {}
    LOGIN_URL = "http://127.0.0.1:8000/accounts/login/"
    response = session.post(
        url=LOGIN_URL,
        data={
            "username":
            "admin",
            "password":
            "1234",
            "csrfmiddlewaretoken":
            "Dgv288A7laGdIwpvcvGyJOfz46eOLcJQbkslpWVRN1yQUcU1myI4Cb0g2eNU7Dhi",
        },
        cookies={
            "csrftoken": "Ie7trYvUC12NmQFGkdcG3xVR8iJgwBIC",
        },
    )

    response = session.get(BOOKS_URL)

    # 페이지를 가져온다.
    soup = BeautifulSoup(response.text, "html.parser")
    page = soup.select_one(".page-current > p")
    total_page = int((page.text.split("of")[1].strip()[0]))  # 2 or 3 or 5
    # 토탈 페이지 만큼 반복할 필요가 있다.

    result = []
    for i in range(1, total_page + 1):
        books_res = session.get(BOOKS_URL, params={"page": i}).text
        books_html = BeautifulSoup(books_res, "html.parser")
        li_list = books_html.select("div.col-sm-10>ul>li")
        for li in li_list:
            book_name = li.text.split('\n')[0]
            book_author = li.text.split('\n')[1]
            book = {"name": book_name, "author": book_author}
            result.append(book)

    for book in result:
        print(book)

# response = requests.get(url)

# soup = BeautifulSoup(response.text, "html.parser")
# ul = soup.select(".row>.col-sm-10>ul")[0]

# li = ul.select("li")

# for tag in li:
#     # print(tag.text)
#     pass

# print(response.text)
