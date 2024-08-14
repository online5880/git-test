from rest_framework import serializers
from catalog.models import Book, BookInstance


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"


class BookInstanceSerialize(serializers.ModelSerializer):

    class Meta:
        mode = BookInstance
        fields = "__all__"
