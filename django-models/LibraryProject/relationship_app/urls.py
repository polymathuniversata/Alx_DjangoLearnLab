"""
URL configuration for relationship_app.

This module defines URL patterns for the relationship_app views,
including both function-based and class-based views.
"""

from django.urls import path
from .views import list_books
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Function-based view for listing all books
    path('books/', views.list_books, name='list_books'),

    # Class-based view for displaying library details
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Alternative ListView for libraries
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),

    # Authentication URLs
    path('login/', LoginView.as_view(template_name='relationship_app/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Role-based access control URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),

    # Custom permission-protected URLs for book operations
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]
