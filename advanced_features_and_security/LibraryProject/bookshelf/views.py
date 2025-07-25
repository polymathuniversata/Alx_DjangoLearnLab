"""
Views for bookshelf app. CRUD operations on Book model with permission enforcement.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm  # Import ExampleForm for demonstration

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """List all books (requires can_view permission)."""
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """Create a new book (requires can_create permission)."""
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        Book.objects.create(title=title, author=author, publication_year=publication_year)
        return redirect('book_list')
    return render(request, 'add_book.html')

# Add to urls.py:
# path('example-form/', example_form_view, name='example_form'),
@permission_required('bookshelf.can_create', raise_exception=True)
def example_form_view(request):
    """Display and process ExampleForm for demonstration."""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Normally process the data here
            return render(request, 'bookshelf/form_example.html', {
                'form': form,
                'submitted': True,
            })
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form, 'submitted': False})

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    """Edit an existing book (requires can_edit permission)."""
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        return redirect('book_list')
    return render(request, 'edit_book.html', {'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    """Delete a book (requires can_delete permission)."""
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'delete_book.html', {'book': book})
