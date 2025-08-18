"""
forms.py for bookshelf app
Defines ExampleForm for demonstration purposes.
"""
from django import forms

class ExampleForm(forms.Form):
    """A simple example form for demonstration."""
    name = forms.CharField(label="Your Name", max_length=100)
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(label="Message", widget=forms.Textarea)
