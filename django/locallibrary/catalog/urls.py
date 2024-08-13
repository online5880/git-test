from django.urls import path
from catalog import views

# URL 을 받아서 필요한 처리를 해주기 위해서는
# urls.py 에 반드시 urlpatterns 라는 리스트가 필요
# path에 이름을 지정하면 <a href="{% url 'index' %} 형태로
# 지정이 가능하다.
urlpatterns = [
    # /catalog/
    # 함수로 지정
    path("", views.index, name="index"),
    # /catalog/books/
    # 클래스로 생성
    path("books", views.BookListView.as_view(), name="books"),
    # /catalog/book/????
    # 클래스로 생성
    path("book/<int:pk>", views.BookDetailView.as_view(),
         name="book-detail"),  # type: ignore
    # /catalog/authors/
    path("authors", views.AuthorListView.as_view(), name="authors"),
    path("authors/<int:pk>",
         views.AuthorDetailView.as_view(),
         name="author-detail"),  # type: ignore
    path("mybooks/",
         views.LoanedBooksByUserListView.as_view(),
         name="my-borrowed"),
    
    path("book/<uuid:pk>/renew/",
         views.renew_book_librarian,
         name="renew-book-librarian"),
]
