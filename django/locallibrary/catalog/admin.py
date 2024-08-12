from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance
# Register your models here.
# 설정을 통해서 관리자 사이트에서
# 모델을 관리할 수 있게 해준다. 
# Book, BookInstance, Author, Genre
# CRUD 를 쉽게 할 수 있도록 지원해준다.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)