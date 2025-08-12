from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.db.models import Q

from .forms import RegistrationForm, ProfileForm, PostForm, CommentForm
from .models import Post, Comment, Tag


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

    def get_queryset(self):
        qs = super().get_queryset()
        # Search by q across title/content and tags
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(tags__name__icontains=q)
            ).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "").strip()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.select_related("author").all()
        # Provide a blank comment form for authenticated users
        if self.request.user.is_authenticated:
            context["comment_form"] = CommentForm()
        return context


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


class PostByTagListView(PostListView):
    """List posts filtered by a tag name (case-insensitive)."""

    def get_queryset(self):
        tag_name = self.kwargs.get("name")
        return (
            super()
            .get_queryset()
            .filter(tags__name__iexact=tag_name)
            .distinct()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_name"] = self.kwargs.get("name")
        return context


class SearchView(PostListView):
    template_name = "blog/post_list.html"


# Comment CRUD views
class CommentAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Ensure we have the parent post
        self.post_obj = get_object_or_404(Post, pk=kwargs.get("post_pk"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        messages.success(self.request, "Comment added.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.post_obj.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, CommentAuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"
    context_object_name = "comment"

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, CommentAuthorRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"
    context_object_name = "comment"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comment deleted.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.post.get_absolute_url()
