from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance

# Register your models here.
# 설정을 통해서 관리자 사이트에서
# 모델을 관리할 수 있게 해준다.
# Book, BookInstance, Author, Genre
# CRUD 를 쉽게 할 수 있도록 지원해준다.

# ! django 어드민이 데이터를 핸들링 할 수 있다. 췤

# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(BookInstance)
admin.site.register(Genre)


class BookInline(admin.TabularInline):
    model = Book


# 어드민 페이지에 대한 커스텀 화면을 제공하는 방법
class AuthorAdmin(admin.ModelAdmin):
    # 리스트 화면에서 데이터를 보여주는 방식을 결정한다.
    list_display = ("last_name", "first_name", "date_of_birth",
                    "date_of_death")

    # 상세 화면에서 데이터를 보여주는 방식을 결정한다.
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]

    inlines = [BookInline]


admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


# 데코레이터를 이용해 다음과 같이 줄여서 쓸 수도 있다.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "due_back", "id")

    list_filter = ("status", "due_back")

    fieldsets = (
        (None, {
            "fields": ("book", "imprint", "id")
        }),
        ("Availability", {
            "fields": ("status", "due_back", "borrow")
        }),
    )
