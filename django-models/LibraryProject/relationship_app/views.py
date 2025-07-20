from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import Library, Book, UserProfile, Author

# Create your views here.

def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    Renders a simple list of book titles and their authors.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    listing all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


class LibraryListView(ListView):
    """
    Alternative class-based view using ListView to display libraries.
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'


# Authentication Views

class CustomLoginView(LoginView):
    """
    Custom login view using Django's built-in LoginView.
    """
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """
    Custom logout view using Django's built-in LogoutView.
    """
    template_name = 'relationship_app/logout.html'


def register(request):
    """
    Function-based view for user registration.
    Uses Django's built-in UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})


# Role-Based Access Control Views

def is_admin(user):
    """Check if user has Admin role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


def is_librarian(user):
    """Check if user has Librarian role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


def is_member(user):
    """Check if user has Member role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    """
    Admin-only view for managing the library system.
    Only users with 'Admin' role can access this view.
    """
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    """
    Librarian-only view for managing books and library operations.
    Only users with 'Librarian' role can access this view.
    """
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    """
    Member-only view for browsing books and library services.
    Only users with 'Member' role can access this view.
    """
    return render(request, 'relationship_app/member_view.html')


# Custom Permission-Protected Views for Book Operations

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    View for adding a new book.
    Requires 'can_add_book' permission.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        publication_year = request.POST.get('publication_year', 2000)

        if title and author_name:
            # Get or create author
            author, created = Author.objects.get_or_create(name=author_name)

            # Create book
            book = Book.objects.create(
                title=title,
                author=author,
                publication_year=int(publication_year)
            )

            return redirect('list_books')

    return render(request, 'relationship_app/add_book.html')


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """
    View for editing an existing book.
    Requires 'can_change_book' permission.
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        publication_year = request.POST.get('publication_year')

        if title and author_name and publication_year:
            # Get or create author
            author, created = Author.objects.get_or_create(name=author_name)

            # Update book
            book.title = title
            book.author = author
            book.publication_year = int(publication_year)
            book.save()

            return redirect('list_books')

    return render(request, 'relationship_app/edit_book.html', {'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """
    View for deleting a book.
    Requires 'can_delete_book' permission.
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect('list_books')

    return render(request, 'relationship_app/delete_book.html', {'book': book})
