from django import forms
from .models import Review
from users.forms import StyleFormMixin


class ReviewAdminForm(StyleFormMixin, forms.ModelForm):
    title = forms.CharField(max_length=180, label="Title")
    content = forms.TextInput()
    slug = forms.SlugField(max_length=40, initial="temp_slug", widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ("dog", "title", "content", "slug")