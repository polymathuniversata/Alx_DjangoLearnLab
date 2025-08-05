from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows books to be viewed or created.
    - List: Public access (read-only)
    - Create: Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'author__id']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['title']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Optionally filter by author name or book title using query parameters.
        """
        queryset = Book.objects.select_related('author').all()
        
        # Filter by author name (case-insensitive partial match)
        author_name = self.request.query_params.get('author_name', None)
        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)
            
        # Filter by publication year range
        min_year = self.request.query_params.get('min_year', None)
        max_year = self.request.query_params.get('max_year', None)
        
        if min_year:
            queryset = queryset.filter(publication_year__gte=min_year)
        if max_year:
            queryset = queryset.filter(publication_year__lte=max_year)
            
        return queryset


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single book to be viewed, updated or deleted.
    - Retrieve: Public access (read-only)
    - Update/Delete: Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows authors to be viewed or created.
    - List: Public access (read-only)
    - Create: Requires authentication
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'book_count']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single author to be viewed, updated or deleted.
    - Retrieve: Public access (read-only)
    - Update/Delete: Requires authentication
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
