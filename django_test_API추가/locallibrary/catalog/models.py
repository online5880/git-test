from django.db import models
from django.urls import reverse
from django.conf import settings
from datetime import date

# 랜덤값을 만들어준다.
import uuid

# Create your models here.
# ORM을 위한 객체를 정의합니다.


class Genre(models.Model):
    # CharField = varchar(200)
    name = models.CharField(
        max_length=200, help_text="Enter a book genre (e.g. Science Fiction)"
    )

    # print(genre) 이렇게 했을 때
    # genre.name이 출력되도록 합니다.
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    #  ForeignKey 옵션은 외부 테이블과의 연관 관계를 나타낸다.
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book "
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
    )

    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

    # genre를 보여주기 위한 커스텀 필드
    def display_genre(self):

        # data = []
        # for genre in self.genre.all():
        #    data += genre.name

        # return ", ".join(data[:3])
        # 위 코드와 똑같습니다.
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"


class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular book across whole library",
    )
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    # AUTH_USER_MODEL > django에서 기본으로 제공하는 유저 모델
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    #  공통코드
    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    # m , o, a, r 중에 하나만 허용합니다.
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id} ({self.book.title})"

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.first_name}. {self.last_name}"
