from django.contrib import admin

from catalog.models import Author, Book, BookInstance, Genre

# Register your models here.
# 설정을 통해서 관리자 사이트에서
# 우리 모델을 관리할수 있게 해준다.
# Book, BookInstance, Author, Genre
# CRUD를 쉽게 할 수 있도록 지원

# 어드민 사이트에 등록
# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)


class BookInline(admin.TabularInline):
    model = Book


# 어드민 페이지에 대한 커스텀 화면을 제공하는 방법
class AuthorAdmin(admin.ModelAdmin):
    # 리스트 화면에서 데이터를 보여주는 방식을 결정한다.
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")

    # 상세 화면에서 데이터를 보여주는 방식을 결정한다.
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
    inlines = [BookInline]


admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


# 다음과 같이 줄여서 쓸 수도 있습니다.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ("status", "due_back")
    list_display = ("book", "status", "due_back", "id")
    # 상세 화면에서 데이터를 표시하는 방법
    # 섹션을 원하는 형태로 배치한다.
    fieldsets = (
        (None, {"fields": ("book", "imprint", "id")}),
        ("Availability", {"fields": ("status", "due_back", "borrower")}),
    )
