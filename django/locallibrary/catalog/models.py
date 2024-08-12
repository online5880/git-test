from django.db import models
from django.urls import reverse
# 랜덤값을 만들어준다.
import uuid

# Create your models here.
# ORM 을 위한 객체를 정의한다.

class Genre(models.Model):
    '''
    장르에 대한 클래스
    '''
    # Charfield = varchar(100)
    
    # help text : 컬럼에 대한 설명
    name = models.CharField(max_length=200,help_text='Enter a book genre (e.g. Science Fiction)')
    
    # print(genre) 라고 하면 genre 에 대해 출력(이름)
    # genre.name이 출력되도록 한다.
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    
    # Foreign Key 옵션은 외부 테이블과의 연관 관계를 나타낸다.
    # 'Author' 처럼 스트링을 선언하면 컬럼명으로 들어간다. 
    # 안적을 경우 변수 이름이 컬럼명이 되서 들어간다.
    # 클래스는 테이블명이다.
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000,help_text='Enter a brief description of the book')
    # isbn : 국제표준도서번호 (international standard book number)
    isbn = models.CharField('ISBN',max_length=13,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])


class BookInstance(models.Model):
    # uuid4 랜덤 문자열의 길이
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique ID for this particular book across whole library')
    
    # on_delete 는 내 Book(Foreign Key) 값이 지워졌을 때 어떻게 할꺼냐
    book = models.ForeignKey('Book',on_delete=models.SET_NULL,null=True)
    imprint = models.CharField(max_length=200)
    # DB에서 datetime은 string이다.
    due_back = models.DateTimeField(null=True,blank=True)
    
    # 공통 코드
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    # choices 는 LOAN_STATUS 값만 받는다.
    # m, o, a, r 중에 하나만 허용한다.
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )
    
    class Meta:
        ordering = ['due_back']
        
    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField('Died',null=True,blank=True)
    
    class Meta:
        ordering = ['last_name','first_name']
        
    def get_absolute_url(self):
        return reverse("author-detail",args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    