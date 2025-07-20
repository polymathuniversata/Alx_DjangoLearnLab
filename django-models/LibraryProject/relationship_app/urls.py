"""
URL configuration for relationship_app.

This module defines URL patterns for the relationship_app views,
including both function-based and class-based views.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Function-based view for listing all books
    path('books/', views.list_books, name='list_books'),

    # Class-based view for displaying library details
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Alternative ListView for libraries
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),

    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Role-based access control URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
]
