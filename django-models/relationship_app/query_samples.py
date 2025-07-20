"""
Sample queries demonstrating Django ORM relationships.

This script contains sample queries for ForeignKey, ManyToMany, and OneToOne relationships
using the Author, Book, Library, and Librarian models.

To run these queries, you can either:
1. Run this script directly: python3 relationship_app/query_samples.py
2. Use Django shell:
   python3 manage.py shell
   Then import this module and run the functions:
   from relationship_app.query_samples import *
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def query_all_books_by_author(author_name):
    """
    Query all books by a specific author.
    Demonstrates ForeignKey relationship (Book -> Author).
    """
    try:
        # Get the author object
        author = Author.objects.get(name=author_name)
        
        # Query all books by this author using the reverse ForeignKey relationship
        books = Book.objects.filter(author=author)
        
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        
        return books
    
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return None


def list_all_books_in_library(library_name):
    """
    List all books in a library.
    Demonstrates ManyToMany relationship (Library <-> Book).
    """
    try:
        # Get the library object
        library = Library.objects.get(name=library_name)
        
        # Query all books in this library using ManyToMany relationship
        books = library.books.all()
        
        print(f"Books in {library_name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
        
        return books
    
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    Demonstrates OneToOne relationship (Librarian -> Library).
    """
    try:
        # Get the library object
        library = Library.objects.get(name=library_name)
        
        # Query the librarian for this library using the reverse OneToOne relationship
        librarian = library.librarian
        
        print(f"Librarian for {library_name}: {librarian.name}")
        
        return librarian
    
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}'.")
        return None


def create_sample_data():
    """
    Create sample data for testing the queries.
    """
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Jane Austen")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    book5 = Book.objects.create(title="Pride and Prejudice", author=author3)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="Community Library")
    
    # Add books to libraries (ManyToMany relationship)
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4, book5)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="Alice Johnson", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Smith", library=library2)
    
    print("Sample data created successfully!")


def run_sample_queries():
    """
    Run all sample queries with the created data.
    """
    print("=" * 50)
    print("DJANGO ORM RELATIONSHIP QUERIES DEMO")
    print("=" * 50)
    
    # Query 1: All books by a specific author (ForeignKey)
    print("\n1. Query all books by a specific author:")
    print("-" * 40)
    query_all_books_by_author("J.K. Rowling")
    
    # Query 2: List all books in a library (ManyToMany)
    print("\n2. List all books in a library:")
    print("-" * 40)
    list_all_books_in_library("Central Library")
    
    # Query 3: Retrieve the librarian for a library (OneToOne)
    print("\n3. Retrieve the librarian for a library:")
    print("-" * 40)
    retrieve_librarian_for_library("Central Library")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    # Check if sample data exists, if not create it
    if not Author.objects.exists():
        print("Creating sample data...")
        create_sample_data()
    
    # Run the sample queries
    run_sample_queries()
