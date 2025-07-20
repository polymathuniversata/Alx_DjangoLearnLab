from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from .models import Library, Book, UserProfile

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
