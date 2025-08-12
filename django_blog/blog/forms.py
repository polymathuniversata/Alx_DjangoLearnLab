from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class PostForm(forms.ModelForm):
    tags_csv = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g. django, web, tutorial)",
        label="Tags",
    )

    class Meta:
        model = Post
        fields = ("title", "content")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prefill tags_csv for edit form
        if self.instance and self.instance.pk:
            current = self.instance.tags.values_list("name", flat=True)
            self.fields["tags_csv"].initial = ", ".join(current)

    def save(self, commit=True):
        post = super().save(commit=commit)
        # Defer M2M until post is saved
        def _save_tags():
            raw = self.cleaned_data.get("tags_csv", "")
            names = [t.strip() for t in raw.split(",") if t.strip()]
            tags = []
            for name in names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            post.tags.set(tags)

        if commit:
            _save_tags()
        else:
            # If not committing, attach a save_m2m-like hook
            self._save_m2m = _save_tags  # type: ignore[attr-defined]
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your comment..."}),
        }
