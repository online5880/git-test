from rest_framework import serializers
from catalog.models import Book, BookInstance


# class를 JSON이나 XML형태로 쉽게 변환할수 있게 해주는 기능
# Serializer가 자동으로 D.D형태로 만들어주는 것
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # Book이 가지고 있는 모든 필드를 대상으로 함
        fields = "__all__"


# BookInstance를 DD로 변환
class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = "__all__"
