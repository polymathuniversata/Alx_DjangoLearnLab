from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import RegistrationForm, ProfileForm, PostForm
from .models import Post


def home(request):
    """Simple home page view."""
    return render(request, "blog/home.html")


def register(request):
    """User registration view using an extended UserCreationForm."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created. You can now log in.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    """Profile view for viewing and updating basic user info."""
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "blog/profile.html", {"form": form})


# Post CRUD views
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url() if hasattr(self.object, "get_absolute_url") else reverse_lazy("post-detail", kwargs={"pk": self.object.pk})


class PostAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostUpdateView(LoginRequiredMixin, PostAuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url() if hasattr(self.object, "get_absolute_url") else reverse_lazy("post-detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, PostAuthorRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")
    context_object_name = "post"
