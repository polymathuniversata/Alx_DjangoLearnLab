from django.test import TestCase, Client
from django.urls import reverse
from .models import Author, Book, Library


class ViewsTestCase(TestCase):
    """Test case for relationship_app views."""

    def setUp(self):
        """Set up test data."""
        # Create test authors
        self.author1 = Author.objects.create(name="Test Author 1")
        self.author2 = Author.objects.create(name="Test Author 2")

        # Create test books
        self.book1 = Book.objects.create(
            title="Test Book 1",
            author=self.author1,
            publication_year=2020
        )
        self.book2 = Book.objects.create(
            title="Test Book 2",
            author=self.author2,
            publication_year=2021
        )

        # Create test library
        self.library = Library.objects.create(name="Test Library")
        self.library.books.add(self.book1, self.book2)

        self.client = Client()

    def test_list_books_view(self):
        """Test the function-based list_books view."""
        response = self.client.get(reverse('list_books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Books Available:")
        self.assertContains(response, "Test Book 1")
        self.assertContains(response, "Test Book 2")
        self.assertContains(response, "Test Author 1")
        self.assertContains(response, "Test Author 2")

    def test_library_detail_view(self):
        """Test the class-based LibraryDetailView."""
        response = self.client.get(reverse('library_detail', args=[self.library.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Library: Test Library")
        self.assertContains(response, "Books in Library:")
        self.assertContains(response, "Test Book 1")
        self.assertContains(response, "Test Book 2")

    def test_library_list_view(self):
        """Test the class-based LibraryListView."""
        response = self.client.get(reverse('library_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Library")

    def test_url_patterns(self):
        """Test that URL patterns resolve correctly."""
        # Test list_books URL
        url = reverse('list_books')
        self.assertEqual(url, '/relationship_app/books/')

        # Test library_detail URL
        url = reverse('library_detail', args=[1])
        self.assertEqual(url, '/relationship_app/library/1/')

        # Test library_list URL
        url = reverse('library_list')
        self.assertEqual(url, '/relationship_app/libraries/')
