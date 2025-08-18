from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Handles serialization/deserialization of Book instances.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_publication_year(self, value):
        """
        Validate that the publication year is not in the future.
        """
        from django.utils import timezone
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f'Publication year cannot be in the future. Current year is {current_year}.'
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes a nested representation of the author's books.
    """
    books = BookSerializer(many=True, read_only=True)
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'book_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'book_count']

    def get_book_count(self, obj):
        """
        Get the count of books written by this author.
        """
        return obj.books.count()
