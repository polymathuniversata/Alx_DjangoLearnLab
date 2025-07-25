from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('example-form/', views.example_form_view, name='example_form'),
    # Add more patterns as needed
]
