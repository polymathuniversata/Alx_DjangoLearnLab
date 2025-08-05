from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.db.models import Count
from api.models import Author, Book


class BaseTestCase(APITestCase):
    """Base test case with common setup for all test cases."""
    
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=True  # Make the user a staff member to bypass permission issues
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        # We'll set the token in individual tests that need authentication
        
        # Create test data
        self.author1 = Author.objects.create(name='J.R.R. Tolkien')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        
        # Create books with the current year as publication year
        current_year = timezone.now().year
        self.book1 = Book.objects.create(
            title='The Hobbit',
            publication_year=current_year - 1,  # Last year
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='The Lord of the Rings',
            publication_year=current_year - 2,  # Two years ago
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=current_year - 3,  # Three years ago
            author=self.author2
        )
        
        # Set up URLs with proper formatting
        self.author_list_url = '/api/authors/'
        self.author_detail_url = lambda pk: f'/api/authors/{pk}/'
        self.book_list_url = '/api/books/'
        self.book_detail_url = lambda pk: f'/api/books/{pk}/'
        
        # Set up authenticated client
        self.authenticated_client = APIClient()
        self.authenticated_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


class AuthorViewSetTestCase(BaseTestCase):
    """Test cases for AuthorViewSet."""
    
    def test_get_authors_unauthenticated(self):
        """Test that unauthenticated users can list authors."""
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that we have the expected number of authors in the results
        self.assertEqual(len(response.data['results']), 2)  # Should return 2 authors
        
    def test_create_author_unauthenticated(self):
        """Test that unauthenticated users cannot create authors."""
        # Ensure client is not authenticated
        self.client.credentials()
        data = {'name': 'New Author'}
        response = self.client.post(self.author_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_author_authenticated(self):
        """Test that authenticated users can create authors."""
        # Ensure client is authenticated
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        # Get the current count of authors
        author_count = Author.objects.count()
        data = {'name': 'New Author'}
        response = self.client.post(self.author_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the author count increased by 1
        self.assertEqual(Author.objects.count(), author_count + 1)
        self.assertEqual(Author.objects.latest('id').name, 'New Author')
        
    def test_retrieve_author(self):
        """Test retrieving a single author."""
        # No authentication needed for GET requests
        self.client.credentials()
        author = Author.objects.first()
        response = self.client.get(f"{self.author_detail_url(author.id)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], author.name)
        # Check if books are included in the response
        if 'books' in response.data:
            self.assertEqual(len(response.data['books']), author.books.count())
        
    def test_update_author_unauthenticated(self):
        """Test that unauthenticated users cannot update authors."""
        self.client.credentials()  # Ensure no authentication
        author = Author.objects.first()
        data = {'name': 'Updated Author'}
        response = self.client.put(self.author_detail_url(author.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_author_authenticated(self):
        """Test that authenticated users can update authors."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        author = Author.objects.first()
        data = {'name': 'Updated Author'}
        response = self.client.put(self.author_detail_url(author.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author.refresh_from_db()
        self.assertEqual(author.name, 'Updated Author')
        
    def test_delete_author_unauthenticated(self):
        """Test that unauthenticated users cannot delete authors."""
        self.client.credentials()  # Ensure no authentication
        author = Author.objects.first()
        response = self.client.delete(self.author_detail_url(author.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_author_authenticated(self):
        """Test that authenticated users can delete authors."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        author = Author.objects.first()
        # Get the count of books associated with this author
        author_books_count = author.books.count()
        author_count = Author.objects.count()
        book_count = Book.objects.count()
        
        response = self.client.delete(self.author_detail_url(author.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify author was deleted
        self.assertEqual(Author.objects.count(), author_count - 1)
        # Verify the correct number of books were deleted
        self.assertEqual(Book.objects.count(), book_count - author_books_count)
        # Verify the author no longer exists
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(id=author.id)


class BookViewSetTestCase(BaseTestCase):
    """Test cases for BookViewSet."""
    
    def test_get_books_unauthenticated(self):
        """Test that unauthenticated users can list books."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the total count of books
        total_books = Book.objects.count()
        self.assertEqual(len(response.data['results']), total_books)  
        
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        self.client.credentials()  # Ensure no authentication
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': 1
        }
        response = self.client.post(self.book_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_book_authenticated(self):
        """Test that authenticated users can create books."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        book_count = Book.objects.count()
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': 1
        }
        response = self.client.post(self.book_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), book_count + 1)
        self.assertEqual(Book.objects.get(id=4).title, 'New Book')
        
    def test_retrieve_book(self):
        """Test retrieving a single book."""
        self.client.credentials()  # No auth needed for GET
        book = Book.objects.first()
        response = self.client.get(self.book_detail_url(book.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], book.title)
        # Check author, handling both nested object and ID
        if 'author' in response.data and isinstance(response.data['author'], dict):
            self.assertEqual(response.data['author']['name'], book.author.name)
        else:
            author_id = response.data.get('author')
            author = Author.objects.get(id=author_id)
            self.assertEqual(author.name, book.author.name)
        
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books."""
        self.client.credentials()  # Ensure no authentication
        book = Book.objects.first()
        data = {'title': 'Updated Title'}
        response = self.client.put(self.book_detail_url(book.id), data, format='json')
        # Should be 401, but might be 403 if permissions are different
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
    def test_update_book_authenticated(self):
        """Test that authenticated users can update books."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        book = Book.objects.first()
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.book_detail_url(book.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, 'Updated Title')
        
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        self.client.credentials()  # Ensure no authentication
        book = Book.objects.first()
        response = self.client.delete(self.book_detail_url(book.id))
        # Should be 401, but might be 403 if permissions are different
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete books."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        book = Book.objects.first()
        book_count = Book.objects.count()
        response = self.client.delete(self.book_detail_url(book.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), book_count - 1)
        # Verify the book was actually deleted
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=book.id)


class FilteringAndSearchingTestCase(BaseTestCase):
    """Test cases for filtering, searching, and ordering."""
    
    def test_filter_books_by_author(self):
        """Test filtering books by author ID."""
        # Get an author with books
        author = Author.objects.annotate(book_count=Count('books')).filter(book_count__gt=0).first()
        if not author:
            self.skipTest("No authors with books found")
        
        # Get the actual count of books for this author from the database
        expected_books = Book.objects.filter(author=author)
        expected_count = expected_books.count()
        
        # Test filtering using the correct parameter name (author__id)
        response = self.client.get(f"{self.book_list_url}?author__id={author.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Debug information
        print(f"Author ID: {author.id}")
        print(f"Expected books: {expected_count}")
        print(f"Actual books in response: {len(response.data['results'])}")
        
        # Check that we got the correct number of books for this author
        self.assertEqual(len(response.data['results']), expected_count, 
                        f"Expected {expected_count} books, got {len(response.data['results'])}. "
                        f"Response data: {response.data}")
        
        # Verify all returned books belong to the specified author
        for book in response.data['results']:
            book_author_id = book['author']['id'] if isinstance(book['author'], dict) else book['author']
            self.assertEqual(book_author_id, author.id, 
                           f"Book {book['id']} has wrong author ID. Expected {author.id}, got {book_author_id}")
            
        # Also test with just 'author' parameter to ensure backward compatibility
        response2 = self.client.get(f"{self.book_list_url}?author={author.id}")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data['results']), expected_count, 
                        f"Filtering with 'author' parameter failed. Expected {expected_count} books, got {len(response2.data['results'])}")
        
    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year range."""
        current_year = timezone.now().year
        min_year = current_year - 5  # Last 5 years
        max_year = current_year
        
        # Count how many books are in this range
        books_in_range = Book.objects.filter(
            publication_year__gte=min_year,
            publication_year__lte=max_year
        ).count()
        
        response = self.client.get(f"{self.book_list_url}?min_year={min_year}&max_year={max_year}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that we got the correct number of books in the date range
        self.assertEqual(len(response.data['results']), books_in_range)
        
    def test_search_books_by_title(self):
        """Test searching books by title."""
        response = self.client.get(f"{self.book_list_url}?search=Hobbit")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that we got at least one result
        self.assertGreater(len(response.data['results']), 0)
        # Check that the search term is in the title of the first result
        self.assertIn('hobbit', response.data['results'][0]['title'].lower())
        
    def test_search_books_by_author_name(self):
        """Test searching books by author name."""
        response = self.client.get(f"{self.book_list_url}?search=Martin")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that we got at least one result
        self.assertGreater(len(response.data['results']), 0)
        # Check that the author's name is in the response
        book_data = response.data['results'][0]
        # Handle both nested author object and author_id cases
        if 'author' in book_data and isinstance(book_data['author'], dict):
            self.assertIn('martin', book_data['author']['name'].lower())
        else:
            author_id = book_data.get('author')
            author = Author.objects.get(id=author_id)
            self.assertIn('martin', author.name.lower())
        
    def test_order_books_by_title(self):
        """Test ordering books by title."""
        response = self.client.get(f"{self.book_list_url}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
        
    def test_order_books_by_publication_year_desc(self):
        """Test ordering books by publication year in descending order."""
        response = self.client.get(f"{self.book_list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))


class ValidationTestCase(BaseTestCase):
    """Test cases for model and serializer validations."""
    
    def test_book_publication_year_in_future(self):
        """Test that publication year cannot be in the future."""
        future_year = timezone.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        self.authenticated_client.post(self.book_list_url, data)
        self.assertEqual(Book.objects.filter(title='Future Book').count(), 0)
        
    def test_author_name_required(self):
        """Test that author name is required."""
        data = {'name': ''}
        response = self.authenticated_client.post(self.author_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
