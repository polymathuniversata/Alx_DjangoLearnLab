from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': 'Welcome to the Book API',
        'endpoints': {
            'books': reverse('book-list', request=request, format=format),
            'admin': reverse('admin:index', request=request, format=format),
            'api-auth': reverse('rest_framework:login', request=request, format=format) + '?next=/' if not request.user.is_authenticated else None
        }
    })

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    For testing purposes, we're allowing unauthenticated access.
    In production, you should use proper authentication.
    """
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer
    # Temporarily allowing any access for testing
    permission_classes = [permissions.AllowAny]
