from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # Book endpoints - separate views for each CRUD operation
    path('books/', views.ListView.as_view(), name='book-list'),  # ListView for retrieving all books
    path('books/<int:pk>/', views.DetailView.as_view(), name='book-detail'),  # DetailView for retrieving a single book by ID
    path('books/create/', views.CreateView.as_view(), name='book-create'),  # CreateView for adding a new book
    path('books/update/', views.UpdateView.as_view(), name='book-update'),  # UpdateView for modifying an existing book
    path('books/delete/', views.DeleteView.as_view(), name='book-delete'),  # DeleteView for removing a book
    
    # Author endpoints
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]

# Add support for format suffixes (e.g., .json)
urlpatterns = format_suffix_patterns(urlpatterns)
