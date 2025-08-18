from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Author(models.Model):
    """
    Represents an author who can write multiple books.
    """
    name = models.CharField(max_length=200, help_text="The name of the author")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Represents a book written by an author.
    """
    title = models.CharField(max_length=200, help_text="The title of the book")
    publication_year = models.IntegerField(help_text="The year the book was published")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author who wrote the book"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author.name} ({self.publication_year})"

    def clean(self):
        """
        Validate that the publication year is not in the future.
        """
        current_year = timezone.now().year
        if self.publication_year > current_year:
            raise ValidationError({
                'publication_year': f'Publication year cannot be in the future. Current year is {current_year}.'
            })

    def save(self, *args, **kwargs):
        """
        Override save to call full_clean for validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_book_author'
            )
        ]
