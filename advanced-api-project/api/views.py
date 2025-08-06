from rest_framework import generics, filters, permissions
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows books to be viewed or created.
    
    - GET: List all books (public access)
        - Query parameters:
            - search: Search in title or author name
            - author_name: Filter by author name (partial match, case-insensitive)
            - min_year/max_year: Filter by publication year range
            - ordering: Sort by any field (default: title)
    - POST: Create a new book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'publication_year', 'author', 'author__id']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['title']
    
    def get_permissions(self):
        """
        Set permissions for the view.
        - GET: Allow any user (including unauthenticated)
        - POST: Require authentication
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Enhance queryset with additional filtering options.
        """
        queryset = Book.objects.select_related('author').all()
        
        # Filter by author ID (supports both 'author' and 'author__id' parameters)
        author_id = self.request.query_params.get('author') or self.request.query_params.get('author__id')
        if author_id:
            try:
                queryset = queryset.filter(author__id=int(author_id))
            except (ValueError, TypeError):
                # If author_id is not a valid integer, return empty queryset
                return Book.objects.none()
        
        # Filter by author name (case-insensitive partial match)
        author_name = self.request.query_params.get('author_name')
        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)
            
        # Filter by publication year range
        min_year = self.request.query_params.get('min_year')
        max_year = self.request.query_params.get('max_year')
        
        if min_year:
            try:
                queryset = queryset.filter(publication_year__gte=int(min_year))
            except (ValueError, TypeError):
                pass
                
        if max_year:
            try:
                queryset = queryset.filter(publication_year__lte=int(max_year))
            except (ValueError, TypeError):
                pass
            
        return queryset


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single book to be viewed, updated or deleted.
    
    - GET: View book details (public access)
    - PUT/PATCH: Update book (requires authentication)
    - DELETE: Remove book (requires authentication)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    
    def get_permissions(self):
        """
        Set permissions for the view.
        - GET: Allow any user (including unauthenticated)
        - PUT/PATCH/DELETE: Require authentication
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
        
    def get_object(self):
        """
        Get the book object or return 404 if not found.
        """
        try:
            return super().get_object()
        except Exception as e:
            raise Http404("Book not found")


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows authors to be viewed or created.
    
    - GET: List all authors with their books (public access)
        - Query parameters:
            - search: Search in author name
            - ordering: Sort by name or book_count (default: name)
    - POST: Create a new author (requires authentication)
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'book_count']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Set permissions for the view.
        - GET: Allow any user (including unauthenticated)
        - POST: Require authentication
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
        
    def get_serializer_context(self):
        """
        Add request to serializer context for URL generation.
        """
        return {'request': self.request}


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single author to be viewed, updated or deleted.
    
    - GET: View author details with their books (public access)
    - PUT/PATCH: Update author (requires authentication)
    - DELETE: Remove author (requires authentication)
    
    Note: Deleting an author will also delete all their associated books
    due to the CASCADE relationship defined in the model.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    lookup_field = 'pk'
    
    def get_permissions(self):
        """
        Set permissions for the view.
        - GET: Allow any user (including unauthenticated)
        - PUT/PATCH/DELETE: Require authentication
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
        
    def get_object(self):
        """
        Get the author object or return 404 if not found.
        """
        try:
            return super().get_object()
        except Exception as e:
            raise Http404("Author not found")
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
